for i in *md;
do
	outF=../../www/${i/md/html}
	titN=${i/.md/}
	echo $outF
	cat header.html | sed 's/title_name/'"$titN"'/' > $outF
#:	markdown $i >> $outF
#       md2html $i >> $outF
#	markdown_py $i >> $outF
#	python3 -m markdown $i >> $outF
#        pandoc -f markdown --filter pandoc-citeproc $i >> $outF
        pandoc -f markdown+pipe_tables $i >> $outF
	echo -e  '</body></html>' >> $outF
done
cp index.html ../../www/

#outF="motorway.html"
#if [ -z "$1" ]; then outF=$1; fi
#cat header.html > $outF
#./Markdown.pl motorway.md >> motorway.html
#markdown ${outF/html/md} >> $outF
#echo -e  '</body></html>' >> $outF

