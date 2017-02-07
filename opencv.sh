#! /bin/sh


case "$1" in
  start|"")
	/home/ubuntu/RustyCommsVision/Python/identifyTargets.py &
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

