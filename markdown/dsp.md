---
title: DSP programming
author: Giovanni Marelli
date: 2019-09-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: dsp_programming
category: #tech
roam_refs: dsp_programming
roam_aliases: ["dsp_programming"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# DSP 

Digital signal processing means the creation of sound effects via digital processing.

It requires: 

* MCU: a microcontroller like arduino or ESP32
* DAC/ADC: digital to analog and analog to digital, at least 12bits
* control: 
  * analog: GPIO
  * midi: with opto-cuopler 
  

# axoloti

Axoloti is a DSP programmable board.

We build an axoloti pedal and program the effect bank.


![axoloti](../../viudi/f/19-axo/axoloti_wooder.jpg "axoloti")
_Pedal_

Axoloti connected to a button pedal via ethernet cable

![axoloti](../../viudi/f/19-axo/axoloti_mixing.jpg "axoloti mixing")

![axoloti](../../viudi/f/19-axo/axoloti_screen.jpg "axoloti screen")

We put a display, buttons and poti in the case

We build an axoloti controller pedal plus controls in the case. We program the effect bank.

![axoloti](../../viudi/f/19-axo/axoloti_wiring.jpg "axoloti wiring" )

We connect two buttons, two potis, a display and two ethernet ports for the pedals

![axoloti](../../viudi/f/19-axo/axoloti_oscilloscope.jpg "axoloti oscilloscope" )

![axoloti](../../viudi/f/19-axo/expression_pedal.jpg "aoloti expression" )

We build a pedal with 6 buttons and an expression (from a gaming joystick)

![axoloti](../../viudi/f/19-axo/axoloti_programming.jpg "axoloti programming" )

We program the effect bank and push it to <a href="https://github.com/sabeiro/viudi-axoloti">github></a> 

![axoloti](../../viudi/f/19-axo/axoloti_wooder.jpg "axoloti wooder" )
We connect the pedal to the axoloti and the music box.
