---
title: no key board
author: Giovanni Marelli
date: 2019-09-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: no-key-board
category: #tech
roam_refs: no-key-board
roam_aliases: ["no-key-board"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---


# no-key-board

No keyboard is a openframeworks project to be able to play a keyboard without quantization. 
The project was mainly developed in 2014 and was running on a laptop. Back then the implementation of openframeworks for ARM (raspberry pi) was pretty poor. 

![[no key board](../../viudi/f/14_no_key_board/NoKeyMano.JPG "no-key-board")
_no-key-board instrument_

The project was inspired by [react table](https://www.youtube.com/watch?v=Mgy1S8qymx0&pp=ygURcmVhY3QgdGFibGUgdHVyaW4%3D) and included as well the presence of a projector to indicate the playable region.

![[no key board](../../viudi/f/14_no_key_board/Programma.png "no-key-board")
_no-key-board software_

A led strip illuminates the upper part of a mated plexyglass. A camera behind reads the finger position and translates x-y and size into pitches.


![[no key board](../../viudi/f/14_no_key_board/SquareWave.png "no-key-board")
_no-key-board synth_

There is a selection of wave forms to pick.

The output is:

* midi: but pitch bend is channel wide so need to use quantization
* osc: which is difficult to integrate in other engines
* synth: own wave forms
* MPE: not available at the time, need to integrate


![[no key board](../../viudi/f/14_no_key_board/NoKeyMano2.JPG "no-key-board")
_no-key-board instrument_
