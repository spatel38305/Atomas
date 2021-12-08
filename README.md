# Atomas
Fall 2021 AI Final Project

James Hammer, Shivam Patel

# Overview of Files
- bot.py - contains the code for running the bots on the game
- cli.py - parsing of debug commands
- ContextConverter.py - holds the 4 context converters discussed in the paper.
- config-feedforward_x files are configuration files required for the NEAT to run.
- Game.py - the main game rendering loop for interactive playin
- RandomActins.py - 1 million randomly played games for control
- Renderer.py - the pygame rendering logic
- requirements.txt - python requirements
- run-all-converters.sh - shell script for running everything at once
- StateMachine.py - contains the state machine of the game
- testMerge.py - a unit test to verify correct game behavior
- utils.py - utility functions used throughout the code
- visualize.py - visualizes the genomes metrics over time and saves them as svg images to disk
- results - directory containing all the images, best models, stdout, stderr, etc. from our runs of the bot.

# Installation Requirements
    python -m pip install -r requirements.txt 
(when pwd is in the root directory of the project), 
    
In addtion to installing all of the required python packages for visualizations to be created, https://graphviz.org/download/ must also be installed and added to the system's PATH. 

# Running the Code
the code can be ran from 2 seperate locations, depending on if you want to play the game yourself, or have the bot train on the game.
For playing the game yourself, follow instructions for Game.py.
For the bot training, follow the instructions for bot.py.

### Game.py
python Game.py [-render true|false] [-interactive true|false] [-debug true|false]
    Render enables rendering.
    Interactive makes pygame listen for user input.
    Both render and interactive must be set to true for the game to be human playable. True is the default value.
    debug enables debug mode, where you can change the state of the game at will using the commands defined in cli.py. False is the default value.

### bot.py
python bot.py -mode n -fout filePath -generations x

- mode: which context converter to run. mode n corresponds to contextConverter-n,
    which in turn also runs with config-feeedforward_n config file.
- fout: which directory should be created to hold the output files
- generations: how many generatinos to run the NEAT for. All arguments have suitable default values.