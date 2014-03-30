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

env: requirements.pip
	test -d env || virtualenv env
	env/bin/pip install -r requirements.pip

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

env/bin/flake8: env
	env/bin/pip install flake8

lint: env/bin/flake8
	env/bin/flake8 colorific tests

test: env
	env/bin/python setup.py test

env/bin/tox: env
	env/bin/pip install tox

test-all: env/bin/tox
	env/bin/tox

env/bin/coverage: env
	env/bin/pip install coverage

coverage: env/bin/coverage
	env/bin/coverage run --source colorific setup.py test
	env/bin/coverage report -m
	env/bin/coverage html
	open htmlcov/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist
