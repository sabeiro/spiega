#!/bin/bash

for i in static_html/img/*svg;
do
    	titN1=${i%.svg}
    	titN=${titN1##*/}
    	outF=static_html/img/path/$titN.svg
	python3 script/text2svg.py $i
	mv output.svg $outF
done
