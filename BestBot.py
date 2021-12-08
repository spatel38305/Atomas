import neat
import pickle
from ContextConverter import *
import Game

mode = 0

def run_game(genomes, config):
    '''
    The genome running callback function. This function is responsible for creating a neural network, 
    running 150 iterations, converting input from the statemachine to the bot, running the bot on the input,
    converting the output of the bot into input into the statemachine, updating the fitness function, and running the
    game for up to 200 iterations.
    '''
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
        games.append(Game.Game(**{'render': True}))

    alive_games = len(games)
    #run games until all genomes are dead (or max iteration hit)
    while alive_games > 0:
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

def replay_genome(config_path, genome_path="winner.pkl"):
    '''
    loads the best performing NET model specified and runs the bot using that model.
    '''

    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    run_game(genomes, config)

def main():
    global mode
    mode = 0

if __name__ == '__main__':
    main()