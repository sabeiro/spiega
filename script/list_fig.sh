cDir=$1
for i in $cDir/*
do
	desc=${i/.png/}
	desc=${desc/"$cDir"\//}
	desc=${desc/_/ }
	echo "!["$desc"]("$i '"'$desc'")'
	echo '_'$desc'_'
done
