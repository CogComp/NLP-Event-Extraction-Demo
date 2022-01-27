while true
do
	python EVENTS_demo_backend.py 0.0.0.0 4021

	read -rsn1 input

	if [ "$input" = "s" ]; then
		sleep 0.05
	fi
	# if [ "$input" = "q" ]; then
	# 	break
	# fi

done

