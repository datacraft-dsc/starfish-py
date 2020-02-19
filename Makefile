.PHONY: clean lint test docs

all: clean

MODULE_NAME = starfish

FLAKE8_PARAMETERS = --max-line-length=132 $(MODULE_NAME)

ISORT_PARAMETERS = --check-only --diff --ignore-whitespace --settings-path ./ --recursive $(MODULE_NAME)

clean:
	rm -rf *egg-info dist .eggs

lint:
	flake8 $(FLAKE8_PARAMETERS)

isort:
	isort $(ISORT_PARAMETERS)

test:
	pytest tests


docs: ## generate Sphinx HTML documentation, including API docs
	cd docs; $(MAKE) clean
	cd docs; $(MAKE) html

