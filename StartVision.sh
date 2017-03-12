#! /bin/bash


case "$1" in
  start|"")
	while [ 1 = 1 ]
	do
		cd /home/frc6201/RustyCommsVision/Python/
	
		res="1"
	#	echo "$res"
		while [ "$res" != "0" ]
		do
			ping -c 1 10.62.1.11
			res="$?"
	#		echo "$res"
	
		done

		echo "starting vision"

		./identifyTargets.py &
	done
	;;
  restart|reload|force-reload)
	echo "Error: argument '$1' not supported" >&2s
	exit 3
	;;
  stop)
	# No-op
	;;
  status)
	exit 
	;;
  *)
	echo "Usage: hostname.sh [start|stop]" >&2
	exit 3
	;;
esac

