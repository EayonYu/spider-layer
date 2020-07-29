ifndef action
	action=pull
endif

default:
	echo "idle"

protocol:
	[ ! $(action) == "pull" ] || python .grpc.py --pull
	[ ! $(action) == "clean" ] || python .grpc.py --clean
	[ ! $(action) == "compile" ] || python .grpc.py --compile
	[ ! $(action) == "push" ] || python .grpc.py --push
