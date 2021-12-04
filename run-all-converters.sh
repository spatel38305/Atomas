#!/bin/bash

/usr/bin/time -v -o bot_3000_generations_converter_0.time python3 bot.py -mode 0 -generations 3000 -fout converter0 > bot_3000_generations_converter0.out 2> bot_3000_generations_converter0.err &

/usr/bin/time -v -o bot_3000_generations_converter_1.time python3 bot.py -mode 1 -generations 3000 -fout converter1 > bot_3000_generations_converter1.out 2> bot_3000_generations_converter1.err &

/usr/bin/time -v -o bot_500_generations_converter_2.time python3 bot.py -mode 2 -generations 500 -fout converter2 > bot_500_generations_converter2.out 2> bot_500_generations_converter2.err &

/usr/bin/time -v -o bot_3000_generations_converter_3.time python3 bot.py -mode 3 -generations 3000 -fout converter3 > bot_3000_generations_converter3.out 2> bot_3000_generations_converter3.err &

