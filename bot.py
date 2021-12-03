import os
import Game
from ContextConverter import *
import neat
import visualize

mode = 1

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
        games.append(Game.Game(**{'render': False, 'bot': True}))

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
            
def run():
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir, 'config-feedforward')
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(100))

    # Run for up to 2000 generations.
    winner = p.run(run_games, 1)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    #p.run(run_games, 10)


if __name__ == '__main__':
    mode = 0
    run()