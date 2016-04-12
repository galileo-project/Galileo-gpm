TARGET       = /usr/bin/gpm
NAME         = gpm
PACKAGE_PATH = /usr/lib/python2.7/site-package
PROJECT_FILE = $(wildcard ./gpm/*/*.py)
TEST_FILE    = $(wildcard ./test/*.py)
TEST_TARGET  = test.out
PROJECT_TEST = gpm.test
PYPATH      := $(shell echo $$PYTHONPATH)

$(shell export PYTHONPATH=$(PYPATH):./test:.)

install:
	rm -rf $(PACKAGE_PATH)/gpm
	rm -f $(TARGET)
	pip install -r requirements.txt
	cp -r $(NAME) $(PACKAGE_PATH)
	chmod 751 $(PACKAGE_PATH)/gpm/main.py
	ln -s $(PACKAGE_PATH)/gpm/main.py $(TARGET)

.PHONY: test
test: $(PROJECT_FILE) $(TEST_FILE)
	chmod 751 test/test.py
	chmod 751 ./gpm/main.py
	ln -s test/test.py $(TEST_TARGET)
	ln -s ./gpm/main.py $(PROJECT_TEST)
	./$(TEST_TARGET)
	./$(PROJECT_TEST) -v

.PHONY: clean
clean:
	-rm -f ./$(TEST_TARGET) ./$(PROJECT_TEST)