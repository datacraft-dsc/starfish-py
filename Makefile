.PHONY: clean clean-pyc clean-build lint flake8 isort test docs

# all: clean lint test docs

PACKAGE_FOLDERS = starfish

FLAKE8_PARAMETERS = --max-line-length=132 --statistics $(PACKAGE_FOLDERS)

ISORT_PARAMETERS = --use-parentheses  --ignore-whitespace --check-only --multi-line=3 --diff --recursive $(PACKAGE_FOLDERS)

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +


lint: flake8 isort

flake8:
	flake8 $(FLAKE8_PARAMETERS)

isort:
	isort $(ISORT_PARAMETERS)

test:
	pytest tests


docs: ## generate Sphinx HTML documentation, including API docs
	cd docs; $(MAKE) clean
	cd docs; $(MAKE) html

