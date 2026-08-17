---
title: audio mixer matrix
author: Giovanni Marelli
date: 2019-07-02
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: audio_mixer_matrix
category: #tech
roam_refs: audio_mixed_matrix
roam_aliases: ["audio mixer matrix"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---
# audio mixer matrix

Audio mixers come from a really straight idea. You have multiple inputs and a stereo output. Stereo outputs are meant for headsets and nowadays they dont even suit to home audio where you at least add a subwoofer. 
Each loudspeaker has multiple cones which means that the frequencies need to be split inside the box and given the high current the components are pretty expensive.
So overall the system is not efficient at all, what is the meaning of mixing all the frequencies to then use high power components to split and route the sound across all cones. 
Plus instruments have different dynamics, wooden bow instruments dont sound like any vibrating cones and sound looses its spatial dimension. 
Why then mix all sources into L/R output? 

An ideal mixer should be able to work in a matrix fashion where you can route the different frequencies depending on the output you want to render. 

The first idea to build this mixer is digital. We should have good ADC/DAC converters (24bit) and processors to build the matrix. The control should be midi so we can run the mix remotely.

