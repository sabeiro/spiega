---
title: midi hub
author: Giovanni Marelli
date: 2019-09-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: midi_hub
category: #tech
roam_refs: midi hub
roam_aliases: ["midi hub"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---

# midi hub

Synths have nice sounds but often lacks good capability to be played with expression especially if you don't have a dedicated player on each instrument. Current midi sequencers, despite some being generative, they like a nice touch. Arpeggios sounds repetitive and melodies trivial.

A midi hub is a device that can receive simple inputs (a chord sequence) and generates multiples outputs (drums, melody, harmony). The sequence is sent across multiple channels with consistency.

The midi output:

* TRS jack
* Midi BLE

The input is midi via TRS jack and we add an optocoupler to avoid to mix currents.

The hardware is:
* ESP32: for cheap MCU with WiFi module
* M5Stack: for ESP32 with built in battery and touch screen

![MCU](../../viudi/f/26-controller/MCU_09.jpg "MCU")
_overview of MCU controllers_


![MCU](../../viudi/f/26-controller/MCU_ESP32.jpg "MCU ESP-32")
_different ESP32 microcontrollers_
