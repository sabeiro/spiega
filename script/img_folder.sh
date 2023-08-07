for i in markdown/*md
do
	sed 's/f_/\.\.\/f\/f_/' $i > tmp.md
	mv tmp.md  $i
done
