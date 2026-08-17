---
title: coiler
author: Giovanni Marelli
date: 2019-07-02
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: coiler
category: #tech
roam_refs: coiler
roam_aliases: ["coiler"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---
# coiler

This project describes the creation of a coiler which is a device to wind a thin copper wire around magnets to create pickups and exciters for e-bows.

# hardware

The coiler needs one arduino, a servo motor and a DC motor.
The magnet is attached to the DC motor and a thin copper wire is attached to its bottom. 
While the DC motor spins the servo motor moves the wire up and down to allow a regular distribution across the magnet.
An MCU:

* [[Arduino R4 - IoT Sensor Controller]]

A coiled winds copper wire around a magnet to create a pickup and a sustainer.

![coiler](../../viudi/f/19-coiler/bottom.jpg "coiler")
_structure of the coiler_


![wiring](../../viudi/f/19-coiler/wiring.jpg "wiring")
_wiring the magnet_



![coiler](../../viudi/f/19-coiler/bottom.jpg "coiler")
_coiler_

we connect almost all free pins to an arduino micro.


![tuning](../../viudi/f/19-coiler/tuning.jpg "tuning the coiler")
_tuning_

We tune the range of the servo motor, the speed of the dc motor 

![inline](../../viudi/f/19-coiler/inline.jpg "inline")
_inline_

We put the copper coil, the tension control, the servo motor and the dc spin motor in line.
