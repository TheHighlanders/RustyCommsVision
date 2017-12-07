#! /bin/bash


case "$1" in
  start|"")
<<<<<<< HEAD
	cd /home/ubuntu/RustyCommsVision/Python/GRIP/
	
	res="1"
#	echo "$res"
	while [ "$res" != "0" ]
=======
	while [ 1 = 1 ]
>>>>>>> 49cfb5019f49c949a483728ccd998c211e932688
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

<<<<<<< HEAD
	./identifyTargets.py &
=======
		./identifyTargets.py
	done
>>>>>>> 49cfb5019f49c949a483728ccd998c211e932688
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

