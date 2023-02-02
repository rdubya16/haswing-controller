# Introduction

This repo is to document my attempts to reverse engineer the Haswing Cayman series of [trolling motor](https://www.amazon.ca/AQUOS-Haswing-Electric-Trolling-Inflatable/dp/B08WYXFVRQ/). The end goal is tie this into a raspberry pi to enable functionality like spot lock. This project was inspired by [Vanchor](https://github.com/AlexAsplund/Vanchor)

# Hardware

The 12 volt version came with a foot pedal, wireless remote and motor unit itself. The factory control of the unit suffers from a handful of annoying flaws but is otherwise a well built and robust trolling motor for the price. There are two approaches you could take to control it, one would be reverse engineering the wireless protocol that the remote uses, the other is the foot pedal which is wired to the unit with a 4 pin waterproof connector. I opted for the wired approach for reliablity. The wireless remote seemed to suffer some dropouts that would result in the motor not receiving the stop commands and would often oversteer.

## RS-485

The 4-pin waterproof connector was found to be RS-485 using an oscilloscope while inspect the traffic sent by the footpedal to the unit. RS-485 uses differental pair signaling on two of the pins. The other 2 pins are for 3.3v output +/-. The 3.3v output seems to provide very little current (10s of mAs) before triggering a series of beeps from the motor and shutting off the supply. The pedal that comes with the unit just uses a small monochrome LCD display and appears to draw very little power.

![Connector](/images/connector.png?raw=true)
