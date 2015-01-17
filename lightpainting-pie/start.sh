#!/bin/bash

while true; do

	echo "Press key 1-9 to start radio, or + - for volume"
	# wir speichern die gedrückte taste in der variable $KEY

	read -n1 KEY 

	MPC="python start-painting.py "

	volume="70"
	commnd=""

	dummy=""

	# change volume
	if [ "$KEY" == "+" ];  then	
		echo "plus "

	elif [ "$KEY" == "-" ];  then	
		echo "minus  "

	else 

		# print image
		if [ "$KEY" -ge 0  ] && [ "$KEY" -le 9  ];  then	
			read -n1 -t1 TKEY

			re='^[0-9]+$'
			if [[ "$TKEY" =~ $re ]]; then
				KEY=$((10*KEY+TKEY))
			fi

			commnd="$MPC $KEY"

		fi


#		if [ "$KEY" == "0" ];  then
#			commnd="$MPC"
#		fi


		# execute command
		if [ "$commnd" != "" ]; then 
			retrn=`eval ${commnd}` 
#			nam=`echo "$KEY ${retrn}" | sed -n 1p | grep -Poh "^[\w\d\s]+"`
#			echo "$nam"
#			echo $nam | espeak -a 90 -p30 -s120

		fi
	fi

done

