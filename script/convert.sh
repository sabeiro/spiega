#!/bin/bash
cd ~/lav/src/spiega/
cp -r $HOME/lav/src/spiega/css/* $HOME/lav/siti/spiega/css/
cp -r $HOME/lav/src/spiega/js/* $HOME/lav/siti/spiega/js/

convert_markdown(){
    srcD=$1
    outD=$2
    for i in $srcD/*md;
    do
	titN1=${i%.md}
	titN=${titN1##*/}
	outF=$outD/a/$titN.html
	if ! [[ $i -nt $outF ]]; then
	    continue
	fi
	cat ./template/header_$template.html | sed 's/title_name/'"$titN"'/g' > $outF
	cat $i | sed -E 's/```mermaid/\n<pre class="mermaid">\n/g; s/```/\n<\/pre>\n/g' > tmp.md
	python3 script/md2html.py tmp.md >> $outF
	cat ./template/footer_$template.html  >> $outF
	echo $outF
    done
}
convert_org(){
    srcD=$1
    outD=$2
    for i in $srcD/*.org;
    do
	titN1=${i%.org}
	titN=${titN1##*/}
	outF=$outD/a/$titN.html
	if ! [[ $i -nt $outF ]]; then
	    continue
	fi
	echo "###       " $i
	cat $i > tmp.org
	emacs tmp.org --batch --load script/html-export-conf.el -f org-html-export-to-html --kill > tmp.boh.txt
	sed 's/\.md/\.html/g' tmp.html > tmp1.html
	cp tmp1.html tmp.html
	python3 ./script/body_only.py tmp.html || { echo '### empty' $i ; exit 1; }
	sed "s/title_name/$titN/g" ./template/header_$template.html > $outF
	cat tmp.html >> $outF
	cat ./template/footer_$template.html >> $outF
	outF=$outD/slide/$titN.html
	emacs tmp.org --batch --load script/html-export-reveal.el -f org-reveal-export-to-html --kill > tmp.boh.txt
	cat tmp.html > $outF
    done
}
###----------------------convert-org-md--------------------------
cd ~/lav/src/spiega/
template="md"
convert_markdown ~/lav/src/spiega/blender_twin_doc/  ~/lav/siti/blender_twin/ 
convert_markdown ~/lav/src/spiega/markdown/ ~/lav/siti/spiega/
template="scritti"
convert_markdown ~/lav/src/spiega/scritti/ ~/lav/siti/scritti/
template="org"
convert_org ~/lav/src/spiega/markdown/ ~/lav/siti/spiega/
convert_org ~/lav/src/spiega/blender_twin/ ~/lav/siti/blender_twin/
template="storia"
convert_org ~/lav/src/spiega/storia/ ~/lav/siti/storia/
template="storie"
convert_org ~/lav/src/spiega/storie/ ~/lav/siti/storie/
####-----------------------spiega-index-------------------------------
outF=$HOME/lav/siti/spiega/index.html
cd ~/lav/src/spiega/
cat ./template/header_index.html > $outF
pandoc -f markdown+pipe_tables ./markdown/index.md >> $outF
cat ./template/footer_index.html  >> $outF
####------------------------replace-.md-links--------------------------
cd ~/lav/siti/spiega/a/
for i in *.html;
do
    cp $i tmp.html
    sed 's/\.md/\.html/g' tmp.html > $i
done
rm tmp.html
cd ~/lav/siti/spiega/slide/
for i in *.html;
do
    cp $i tmp.html
    sed 's/\.md/\.html/g' tmp.html > $i
done
rm tmp.html

rm tmp*
cp ./html/*html $HOME/lav/siti/spiega/a/
cp css/reveal_custom.css ~/lav/siti/spiega/reveal/css/
cp css/* -r ~/lav/siti/blender_twin/css/
cp js/* -r ~/lav/siti/blender_twin/js/

# for i in *md;
# do
#     sed 's/..\/f\//..\/..\/f\//g' $i > ../$i
# done
