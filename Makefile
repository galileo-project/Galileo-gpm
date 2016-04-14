TARGET_DIR   = /usr/bin
TARGET       = $(TARGET_DIR)/gpm
PACKAGE      = gpm
PACKAGE_PATH = /usr/lib/python*/site-packages
PROJECT_FILE = $(wildcard ./gpm/*/*.py)
TEST_FILE    = $(wildcard ./test/*.py)
TEST_TARGET  = test.out
PROJECT_TEST = gpm.test
SCRIPTS      = $(wildcard ./gpm/script/*)

install: $(PROJECT_FILE) uninstall
	pip install -r requirements.txt
	python setup.py install
	chmod 751 script/*
	cp script/* $(TARGET_DIR)

.PHONY: test
test: unitTest installTest clean

.PHONY: unitTest
unitTest: $(PROJECT_FILE) $(TEST_FILE) clean
	chmod 751 test/test.py
	ln -s test/test.py $(TEST_TARGET)
	./$(TEST_TARGET)

.PHONY: installTest
installTest: install
	gpm -v

.PHONY: uninstall
uninstall:
	rm -rf $(PACKAGE_PATH)/$(PACKAGE)
	rm -f $(TARGET)

.PHONY: clean
clean:
	-rm -f ./$(TEST_TARGET) ./$(PROJECT_TEST)