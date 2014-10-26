#
#  Makefile
#

help:
	@echo "Helper commands for working with the colorific codebase:"
	@echo
	@echo "clean-build    remove build artifacts"
	@echo "clean-pyc      remove Python file artifacts"
	@echo "lint           check style with flake8"
	@echo "test           run tests quickly with the default Python"
	@echo "test-all       run tests on every Python version with tox"
	@echo "coverage       check code coverage quickly with the default Python"
	@echo "docs           generate Sphinx HTML documentation, including API docs"
	@echo "release        package and upload a release"
	@echo "sdist          package"
	@echo

ENV = /tmp/virtualenv/colorific
PY = $(ENV)/bin/python
PIP = $(ENV)/bin/pip

env:
	test -d $(ENV) || virtualenv $(ENV)
	$(PY) setup.py develop

clean: clean-build clean-pyc
	rm -fr htmlcov/

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

$(ENV)/bin/flake8: env
	$(PIP) install flake8

lint: $(ENV)/bin/flake8
	$(ENV)/bin/flake8 colorific tests

test: env
	$(PY) setup.py test

$(ENV)/bin/tox: env
	$(ENV)/bin/pip install tox

test-all: $(ENV)/bin/tox
	$(ENV)/bin/tox

$(ENV)/bin/coverage: env
	$(ENV)/bin/pip install coverage

coverage: $(ENV)/bin/coverage
	$(ENV)/bin/coverage run --source colorific setup.py test
	$(ENV)/bin/coverage report -m
	$(ENV)/bin/coverage html
	open htmlcov/index.html

release: clean
	$(PY) setup.py sdist upload
	$(PY) setup.py bdist_wheel upload

dist: clean
	$(PY) setup.py sdist
	$(PY) setup.py bdist_wheel
	ls -l dist

.PHONY: env test coverage release dist clean clean-build clean-pyc
