import os
import Game
from ContextConverter import *
import neat
import visualize
import argparse
import pickle

mode = 0

def run_games(genomes, config):
    global mode
    nets = []
    games = []

    for _,g in genomes:
        # create feed forward network for this genome
        net = neat.nn.FeedForwardNetwork.create(g, config)
        # save network
        nets.append(net)
        # set initial fitness to zero
        g.fitness = 0
        # create game for this genome
        games.append(Game.Game(**{'render': False}))

    max_iter = 200
    i = 0
    alive_games = len(games)
    #run games until all genomes are dead (or max iteration hit)
    while alive_games > 0 and i < max_iter:
        i += 1
        for genome, net, game in zip(genomes, nets, games):
            # get machine context
            mctx = game.stateMachine.MachineContext()
            #if game over, don't try and continue running this genome
            if not mctx._Running:
                continue
            # convert context to get valid inputs
            inputs, score = convertContext(mode, mctx)
            # input into NEAT
            output = net.activate(inputs)
            # convert bot output to game state machine input
            smi = convertOutput(output, mctx)
            # run game with bot's input
            mctx = game.runTick(smi)
            # convert context to get valid score
            inputs, score = convertContext(mode, mctx)
            # update score
            genome[1].fitness = score[0]
            # update remaining games
            if not mctx._Running:
                alive_games -= 1
            
def run(generations, foutDirName):
    global mode
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config-feedforward_{}'.format(mode))
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100))

    # Run for up to 2000 generations.
    winner = p.run(run_games, generations)

    #create results dir based on mode
    foutDir = os.path.join(local_dir, foutDirName)
    if not os.path.exists(foutDir):
        os.makedirs(foutDir)

    # Save the winning genome
    with open(os.path.join(foutDir, "winner.pkl"), "wb") as f:
        pickle.dump(winner, f)


    # Show output of the most fit genome against training data.
    visualize.draw_net(config, winner, filename=os.path.join(foutDir, 'net'))
    visualize.plot_stats(stats, filename=os.path.join(foutDir, 'avg_fitness.svg'))
    visualize.plot_species(stats, filename=os.path.join(foutDir, 'speciation.svg'))

def main(generations, fout, m=0):
    global mode
    mode = m
    run(generations, fout)
    
def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mode', dest='m', type=int)
    parser.add_argument('-fout', dest='fout', type=int)
    parser.add_argument('-generations', dest='generations', type=int)
    args = parser.parse_args()    

    if args.generations == None:
        args.generations = 1
    if args.m == None:
        args.m = 3
    elif args.m < 0 or args.m > 3:
        print('Error, mode must be between 0 and 3')
        return
        
    if args.fout == None:
        args.fout = str(args.m)

    main(**vars(args))

if __name__ == "__main__":
    cli()
    