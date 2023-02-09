# Introduction

This repo is to document my attempts to reverse engineer the Haswing Cayman series of [trolling motor](https://www.amazon.ca/AQUOS-Haswing-Electric-Trolling-Inflatable/dp/B08WYXFVRQ/). The end goal is tie this into a raspberry pi to enable functionality like spot lock. This project was inspired by [Vanchor](https://github.com/AlexAsplund/Vanchor)

# Hardware

The 12 volt version came with a foot pedal, wireless remote and motor unit itself. The factory control of the unit suffers from a handful of annoying flaws but is otherwise a well built and robust trolling motor for the price. There are two approaches you could take to control it, one would be reverse engineering the wireless protocol that the remote uses, the other is the foot pedal which is wired to the unit with a 4 pin waterproof connector. I opted for the wired approach for reliablity. The wireless remote seemed to suffer some dropouts that would result in the motor not receiving the stop commands and would often oversteer.

## RS-485

The 4-pin waterproof connector was found to be RS-485 using an oscilloscope while inspecting the traffic sent by the footpedal to the unit. RS-485 uses differental pair signaling on two of the pins. The other 2 pins are for 3.3v output +/-. The 3.3v output seems to provide very little current (10s of mAs) before triggering a series of beeps from the motor and shutting off the supply. The pedal that comes with the unit just uses a small monochrome LCD display and appears to draw very little power.

![Connector](/images/connector.png?raw=true)

## Protocol
The code defines a class `Haswing` which communicates with the trolling motor over a serial port using an RS-485 hat.

A command is sent to the motor by calling the method `_send_command` and passing it the command. The `_send_command` method builds a bytearray consisting of the start bit, device ID, command and stop bit. This bytearray is then written to the serial port. The motor will respond with a 6 byte response which is read by the `_send_command` method. The `_parse_response` method is then called to parse the response and update the status of the motor (stored in `_motor_status`), the motor speed (stored in `_motor_speed`), and the battery level (stored in `_battery_level`).


The start bit is `0x23` and the stop bit is `0x80`. The device ID is `0x54`. I havent done extensive testing, but seems anything is accepted for the deviceID. 


### Command
Start Bit | Device ID | Command | Stop Bit
----------|-----------|---------|---------
0x23      | 0x54      | 0x52    | 0x80


### Reponse
Start Bit | Command | Motor Status | Motor Speed | Battery Level | Stop Bit
----------|---------|-------------|------------|--------------|---------
0x23      | 0x52    | 0x00        | 0x0a       | 0x03         | 0x80


### Supported Commands
Command | Hex Value
--- | ---
RIGHT_TURN | 0x52
LEFT_TURN | 0x4c
INCREASE_SPEED | 0x55
DECREASE_SPEED | 0x44
TOGGLE_MOTOR | 0x53
DONE | 0x4e



