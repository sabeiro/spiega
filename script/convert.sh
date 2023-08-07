cd markdown
for i in *md;
do
	outF=../../../siti/spiega/${i/md/html}
	titN=${i/.md/}
	echo $outF
	cat ../template/header.html | sed 's/title_name/'"$titN"'/' > $outF
#        pandoc -f markdown --filter pandoc-citeproc $i >> $outF
        pandoc -f markdown+pipe_tables $i >> $outF
        cat ../template/footer.html  >> $outF
done

outF=../../../siti/spiega/index.html
cat ../template/header_index.html > $outF
pandoc -f markdown+pipe_tables index.md >> $outF
cat ../template/footer_index.html  >> $outF



#outF="motorway.html"
#if [ -z "$1" ]; then outF=$1; fi
#cat header.html > $outF
#./Markdown.pl motorway.md >> motorway.html
#markdown ${outF/html/md} >> $outF
#echo -e  '</body></html>' >> $outF
#:	markdown $i >> $outF
#       md2html $i >> $outF
#	markdown_py $i >> $outF
#	python3 -m markdown $i >> $outF

