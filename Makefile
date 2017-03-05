# Copyright © 2016 Absolute Performance Inc <csteam@absolute-performance.com>.
# All rights reserved.
# This is proprietary software.
# No warranty, explicit or implicit, provided.

.PHONY: all wheel tag clean test

all: clean wheel

wheel: setup.py
	PYTHONPATH="$(shell pwd)" ./setup.py bdist_wheel

test:
	PYTHONPATH="$(shell pwd)" python3 -m unittest discover ./test
	PYTHONPATH="$(shell pwd)" python2 -m unittest discover ./test

tag:
	git tag -s '$(shell PYTHONPATH="$(pwd)" python -c 'import texttables; print(texttables.__version__)')'

clean:
	git clean -xfd
