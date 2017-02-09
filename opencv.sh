#! /bin/sh
### BEGIN INIT INFO
# Provides:          StartVisionFRC6201
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: FRC 6201 autostarts vision code on boot.
# Description:       See https://www.github.com/TheHighlanders/RustyCommsVision for more details.
### END INIT INFO

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

