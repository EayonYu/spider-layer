ifndef action
	action=pull
endif

default:
	echo "idle"

protocol:
	[ ! $(action) == "pull" ] || python .protocol.py -p
	[ ! $(action) == "clean" ] || python .protocol.py -c
