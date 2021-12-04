#!/bin/bash

#3000 generations

/usr/bin/time -v -o bot_3000_generations_converter_0.time python3 bot.py -mode 0 -generations 3000 -fout converter0_3000_generations > bot_3000_generations_converter0.out 2> bot_3000_generations_converter0.err &

/usr/bin/time -v -o bot_3000_generations_converter_1.time python3 bot.py -mode 1 -generations 3000 -fout converter1_3000_generations > bot_3000_generations_converter1.out 2> bot_3000_generations_converter1.err &

/usr/bin/time -v -o bot_3000_generations_converter_2.time python3 bot.py -mode 2 -generations 3000 -fout converter2_3000_generations > bot_3000_generations_converter2.out 2> bot_3000_generations_converter2.err &

/usr/bin/time -v -o bot_3000_generations_converter_3.time python3 bot.py -mode 3 -generations 3000 -fout converter3_3000_generations > bot_3000_generations_converter3.out 2> bot_3000_generations_converter3.err &

#5000 generations

/usr/bin/time -v -o bot_5000_generations_converter_0.time python3 bot.py -mode 0 -generations 5000 -fout converter0_5000_generations > bot_5000_generations_converter0.out 2> bot_5000_generations_converter0.err &

/usr/bin/time -v -o bot_5000_generations_converter_1.time python3 bot.py -mode 1 -generations 5000 -fout converter1_5000_generations > bot_5000_generations_converter1.out 2> bot_5000_generations_converter1.err &

/usr/bin/time -v -o bot_5000_generations_converter_2.time python3 bot.py -mode 2 -generations 5000 -fout converter2_5000_generations > bot_5000_generations_converter2.out 2> bot_5000_generations_converter2.err &

/usr/bin/time -v -o bot_5000_generations_converter_3.time python3 bot.py -mode 3 -generations 5000 -fout converter3_5000_generations > bot_5000_generations_converter3.out 2> bot_5000_generations_converter3.err &

#10000 generations

/usr/bin/time -v -o bot_10000_generations_converter_0.time python3 bot.py -mode 0 -generations 10000 -fout converter0_10000_generations > bot_10000_generations_converter0.out 2> bot_10000_generations_converter0.err &

/usr/bin/time -v -o bot_10000_generations_converter_1.time python3 bot.py -mode 1 -generations 10000 -fout converter1_10000_generations > bot_10000_generations_converter1.out 2> bot_10000_generations_converter1.err &

/usr/bin/time -v -o bot_10000_generations_converter_2.time python3 bot.py -mode 2 -generations 10000 -fout converter2_10000_generations > bot_10000_generations_converter2.out 2> bot_10000_generations_converter2.err &

/usr/bin/time -v -o bot_10000_generations_converter_3.time python3 bot.py -mode 3 -generations 10000 -fout converter3_10000_generations > bot_10000_generations_converter3.out 2> bot_10000_generations_converter3.err &

#20000 generations

/usr/bin/time -v -o bot_20000_generations_converter_0.time python3 bot.py -mode 0 -generations 20000 -fout converter0_20000_generations > bot_20000_generations_converter0.out 2> bot_20000_generations_converter0.err &

/usr/bin/time -v -o bot_20000_generations_converter_1.time python3 bot.py -mode 1 -generations 20000 -fout converter1_20000_generations > bot_20000_generations_converter1.out 2> bot_20000_generations_converter1.err &

/usr/bin/time -v -o bot_20000_generations_converter_2.time python3 bot.py -mode 2 -generations 20000 -fout converter2_20000_generations > bot_20000_generations_converter2.out 2> bot_20000_generations_converter2.err &

/usr/bin/time -v -o bot_20000_generations_converter_3.time python3 bot.py -mode 3 -generations 20000 -fout converter3_20000_generations > bot_20000_generations_converter3.out 2> bot_20000_generations_converter3.err &
