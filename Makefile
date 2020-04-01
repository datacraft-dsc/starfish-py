.PHONY: clean clean-pyc clean-build  \
	install install-dev install-test install-docs \
	lint flake8 isort \
	tests test-unit test-integration docs

# all: clean lint test docs

IGNORE_VENV ?= FALSE

PACKAGE_FOLDERS = starfish tools

FLAKE8_PARAMETERS = --max-line-length=132 --statistics $(PACKAGE_FOLDERS)

ISORT_PARAMETERS = --use-parentheses  --ignore-whitespace --check-only --multi-line=3 --force-grid-wrap=2 --line-width=132 --diff --recursive $(PACKAGE_FOLDERS)

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

install: virtualvenv
	pip install -e ".[dev]" -e ".[test]" -e ".[docs]"

install-dev: virtualvenv
	pip install -e ".[dev]"

install-test: virtualvenv
	pip install -e ".[test]"

install-docs: virtualvenv
	pip install -e ".[docs]"


virtualvenv:
ifeq ($(IGNORE_VENV),FALSE)
ifeq ($(VIRTUAL_ENV),)
		@echo "you are about to install this module when you are not in a virtual environment"
		exit 1
endif
endif


lint: flake8 isort

flake8:
	flake8 $(FLAKE8_PARAMETERS)

isort:
	isort $(ISORT_PARAMETERS)

tests:
	pytest tests

test-unit:
	pytest tests/unit

test-integration:
	pytest tests/integration

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

