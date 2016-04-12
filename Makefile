TARGET       = /usr/bin/gpm
NAME         = gpm
PACKAGE_PATH = /usr/lib/python2.7/site-package
PROJECT_FILE = $(wildcard ./gpm/*/*.py)
TEST_FILE    = $(wildcard ./test/*.py)
TEST_TARGET  = test.out
PROJECT_TEST = gpm.test
PYPATH      := $(shell echo $$PYTHONPATH)

export PYTHONPATH=$(PYPATH):./test:.

install:
	pip install requirements.txt
	cp -r $(NAME) $(PACKAGE_PATH)
	chmod 751 $(PACKAGE_PATH)/gpm/gom.py
	ln -s $(PACKAGE_PATH)/gpm/gom.py $(TARGET)

.PHONY: test
test: $(PROJECT_FILE) $(TEST_FILE)
	chmod 751 test/test.py
	chmod 751 src/gpm.py
	ln -s test/test.py $(TEST_TARGET)
	ln -s ./gpm/src/gpm.py $(PROJECT_TEST)
	./$(TEST_TARGET)

.PHONY: clean
clean:
	-rm -f ./$(TEST_TARGET) ./$(PROJECT_TEST)