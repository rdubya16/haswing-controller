# Introduction

This repo is to document my attempts to reverse engineer the Haswing Cayman series of [trolling motor](https://www.amazon.ca/AQUOS-Haswing-Electric-Trolling-Inflatable/dp/B08WYXFVRQ/). The end goal is tie this into a raspberry pi to enable functionality like spot lock. This project was inspired by [Vanchor](https://github.com/AlexAsplund/Vanchor)

# Hardware

The 12 volt version I have, came with a foot pedal, wireless remote and motor unit itself. The factory control of the unit suffers from a handful of annoying flaws but is otherwise a well built and robust trolling motor for the price. There are two approaches you could take to control it, one would be reverse engineering the wireless protocol that the remote uses, the other is the foot pedal which is wired to the unit with a 4 pin waterproof connector. I opted for the wired approach for reliablity. The wireless remote seemed to suffer some dropouts that would result in the motor not receiving the stop commands and would often oversteer.

## RS-485


