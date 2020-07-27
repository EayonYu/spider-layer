ifndef version
	version=latest
endif

all: pull-proto

pull-proto:
	[ ! $(lan) ] || aws s3 sync --delete s3://protocols/gaia/mirror/$(version)/$(lan) ./layer/protocol/mirror
	cd ./layer/protocol/mirror; touch __init__.py

.PHONY: pull-proto