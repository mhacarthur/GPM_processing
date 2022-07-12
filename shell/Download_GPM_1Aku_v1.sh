#!/bin/bash

clear

echo " "
echo "GOES16 GLM descarga"

ANO=2019

USER='arturo66cta@gmail.com'
PASS='Mazamorra2328'

n=1

touch .netrc
echo "machine urs.earthdata.nasa.gov login $USER password $PASS" >> .netrc
chmod 0600 .netrc

for x in $(cat ../list/download/GPM_2Aku_2019_01_2019_12.txt);do

	NAME1=$(echo $x | cut -d"/" -f9)
	NAME2=$(echo $NAME1 | cut -d"?" -f1)
	NAME3="../data/$ANO/$NAME2"

	echo $NAME2
	echo $NAME3
	
	if [ \( $n -eq 0 \) -o \( $n -eq 1 \) ]
	then
		echo "Cabezales"
	else
		echo $n,$NAME2
		if [ -f $NAME3 ]
		then
			echo "Archivo existe"
		else
			echo "Descargando"
			wget --user $USER --password $PASS $x -O $NAME3
			#wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --user $USER --password $PASS $x -O $NAME3
		fi
	fi
	echo ""
	n=$((n+1))
	
done
