---
title: piezo buffer
author: Giovanni Marelli
date: 2019-09-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: piezo_buffer
category: #tech
roam_refs: piezo_buffer
roam_aliases: ["piezo buffer"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# piezo buffer

Acoustic instruments can be amplified by using piezoelectric disks which are cheap and cover a good spectrum of frequencies, especially if you use two of different diameters.
The piezo has high impedance and doesn't sound good with most pedals and music gears. It is important to build a preamplifier which acts as a voltage follower, it isolates the two loops and change the overall impedance to a more standard line in input. 
Piezo microphones have impedance from 3 to 10 mega Ohms which causes the signal distort. 
In this video we test different configurations for piezo preamp and we come with a stand alone preamp powered by usb-c supply. 
Compared to the previous preamp we use this time a dual powered preamplifier which compared to the previous one using a resistor partitor sounds much better. 
The violin is used to create a soundtrack with zoom g1 four effect pedal and novation circuit for the base.

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/B5DMflQo4Xw?si=6kRuyeYZYa_ZYe_D" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## circuit

Using Using [circuitlab](https://www.circuitlab.com/) or [kicad](https://www.kicad.org/)


# piezo buffer for impedance match

I've been working at piezo preamps for many years and I always struggled to find a good sounding result.
At the beginning I've been using the knowledge of nucler physics to build custom preamps to improve the signal to noise ratio.
The material I got required complex computation and, even worse, components that are not available on the market any longer. Originally I started working with JFet but they are really hard to find and I had few in stock. I needed a solution which can last longer. I moved to op-amp starting initially with LM387 but I was really unsatisfied with the result.
The big change was not to find the best schematics but better components. The big change was to use NE532 supplied by a step-up with dual voltage from 5V USB.

### Circuit

Circuit selection, trials and modifications

![ciruit](../../viudi/f/19-buffer/piezo_buffer_opamp.png "piezo buffer")
_We try every circuit on the protoboard before wiring_

![ciruit](../../viudi/f/19-buffer/piezo_buffer_case.jpg "piezo buffer")
_We use small cases to include the buffer, even small loudspeakers have enough sound definition_

![ciruit](../../viudi/f/19-buffer/piezo_preamp_opamp_stepup_detail01.png "piezo buffer")
_voltage follower_

The principle here is a voltage follower, we use a double op amp per channel, both stage on the inverting pin. The feedback loop is 1 since we don't need to amplify but rather decrease the total voltage caused by the piezo. [kicad project](../../viudi/f/19-buffer/piezo_preamp.zip) 

![opamp](../../viudi/f/19-buffer/piezo_preamp_opamp_stepup_detail02.png "detail opamp")
_Since most of the violins have two different piezo I use two channels._


![power supply](../../viudi/f/19-buffer/piezo_preamp_opamp_stepup_detail03.png "power supply")
_Power supply_

What makes this preamp superior to the others is the step-up. I convert the 5V usb power supply into a double +/- 12V which correctly amplifies the signal. Previously I was using dual power supply (really hard to carry) or 9V batteries with a partitor resistor creating +/- 4V5 creating a lot of noise.


![proto circuit](../../viudi/f/19-buffer/proto_circuit.jpg "proto circuit")
_proto circuit_
We test all the circuits on the breadboard before soldering the components. We use a simple speaker to test the results.


![amps opamp](../../viudi/f/19-buffer/piezo_amps_opamp.jpg "amp opamp")
_amp opamp_

We minimize the circuit size on the board. The bulkiest components are the plugs and the stereo potentiometer. We can add multiple inputs so the buffer acts as a mixer. 


![case](../../viudi/f/19-buffer/piezo_buffer_case.jpg "case")
_preamp case_

We use small aluminium cases for the em isolation
