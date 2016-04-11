TARGET       = /usr/bin/gpm
NAME         = gpm
PACKAGE_PATH = /usr/lib/python2.7/site-package
PROJECT_FILE = $(wildcard ./gpm/*/*.py)
TEST_FILE    = $(wildcard ./test/*.py)
PYPATH      := $(shell echo $$PYTHONPATH)

export PYTHONPATH=$(PYPATH):./test:.

install:
	cp -r $(NAME) $(PACKAGE_PATH)
	ln -s $(PACKAGE_PATH)/gpm/gom.py $(TARGET)

.PHONY: test
test: $(PROJECT_FILE) $(TEST_FILE)
	chmod 751 test/test.py
	ln -s test/test.py test.out
	./test.out
	rm -f ./test.out
