TARGET       = /usr/bin/gpm
PACKAGE_PATH = /usr/lib/pathon2.7/site-package
PROJECT_FILE = $(wildcard gpm/*/*.py)
TEST_FILE    = $(wildcard test/*.py)

install:
	cp -r bpm $(PACKAGE_PATH)
	ln -s $(PACKAGE_PATH)/gpm/gom.py $(TARGET)

.PHYON: test
test: $(PROJECT_FILE) $(TEST_FILE)
	export PYTHONPATH=$PYTHONPATH:./test:.
	python test/test.py
