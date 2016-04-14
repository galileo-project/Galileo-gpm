TARGET_DIR   = /usr/bin
TARGET       = $(TARGET_DIR)/gpm
PACKAGE      = gpm
PACKAGE_PATH = /usr/lib/python*/site-package
PROJECT_FILE = $(wildcard ./gpm/*/*.py)
TEST_FILE    = $(wildcard ./test/*.py)
TEST_TARGET  = test.out
PROJECT_TEST = gpm.test
PYPATH      := $(shell echo $$PYTHONPATH)
SCRIPTS      = $(wildcard ./gpm/script/*)
$(shell export PYTHONPATH=$(PYPATH):./test:.)

install: uninstall
	pip install -r requirements.txt
	cp -r $(PACKAGE) $(PACKAGE_PATH)
	chmod 751 $(PACKAGE_PATH)/gpm/script/*
	cp $(PACKAGE_PATH)/gpm/script/* $(TARGET_DIR)

.PHONY: test
test: $(PROJECT_FILE) $(TEST_FILE) clean
	chmod 751 test/test.py
	chmod 751 ./gpm/script/*
	ln -s test/test.py $(TEST_TARGET)
	ln -s ./gpm/script/gpm $(PROJECT_TEST)
	./$(TEST_TARGET)
	./$(PROJECT_TEST) -v

.PHONY: uninstall
uninstall:
	rm -rf $(PACKAGE_PATH)/$(PACKAGE)
	rm -f $(TARGET)

.PHONY: clean
clean:
	-rm -f ./$(TEST_TARGET) ./$(PROJECT_TEST)