import os
import Game
from ContextConverter import *
import neat
#import neat.visualize

def run_game(genomes, config):
    nets = []
    games = []

    for id, g in genomes:
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
            if not mctx._Running:
                continue

            # convert context to get valid inputs
            inputs, score = convertContext(mctx)
            
            # input into NEAT
            output = net.activate(inputs)

            # TODO: give shivam output to convert to smi
            # smi = convertSMI(output)
            smi = []

            # run game with bot's input
            mctx = game.runTick(smi)

            # convert context to get valid score
            inputs, score = convertContext(mctx)

            # update score
            genome[1].fitness = score

            if not mctx._Running:
                alive_games -= 1

            game.smi = []
            
def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(run_game, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    return
    '''
    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    for xi, xo in zip(xor_inputs, xor_outputs):
        output = winner_net.activate(xi)
        print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

    node_names = {-1:'A', -2: 'B', 0:'A XOR B'}
    #visualize.draw_net(config, winner, True, node_names=node_names)
    #visualize.plot_stats(stats, ylog=False, view=True)
    #visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(eval_genomes, 10)
    '''

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)