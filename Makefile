export PROJECTNAME=$(shell basename "$(PWD)")

.SILENT: ;               # no need for @

release: ## Step to prepare a new release
	echo "Instructions to prepare release"
	echo "Repo: one-page: Increment version in app/__init__.py"
	echo "Repo: one-page: Increment version in .travis.yml"
	echo "Commit - Preparing Release x.x.x"
	echo "Repo: one-page-osx: Increment version in .travis.yml"
	echo "Commit - Release x.x.x - MacOS"
	echo "Repo: one-page-win: Increment version in .appveyor.yml"
	echo "Commit - Release x.x.x - Windows"
	echo "Repo: one-page: Update Download Links in README.md"
	echo "Repo: deskriders.dev: Update Project Page with Download Links"

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean: clean-pyc ## Clean package
	rm -rf build dist

black: ## Runs black for code formatting
	black app --exclude generated

lint: black ## Runs Flake8 for linting
	flake8 app

setup: clean ## Re-initiates virtualenv
	rm -rf venv
	python3 -m venv venv
	./venv/bin/python3 -m pip install -r requirements/dev.txt
	echo "Now you can 'make run' to run the application"

deps: ## Reinstalls dependencies
	./venv/bin/python3 -m pip install -r requirements/dev.txt

package: clean ## Packages app
	./venv/bin/python3 -m pip install -r requirements/build.txt
	export PYTHONPATH=`pwd`:$PYTHONPATH && ./venv/bin/python3 setup.py bdist_app

uic: ## Converts ui files to python
	for i in `ls resources/views/*.ui`; do FNAME=`basename $${i} ".ui"`; ./venv/bin/pyuic6 $${i} > "app/generated/$${FNAME}_ui.py"; done

run: ## Runs the application
	export PYTHONPATH=`pwd`:$PYTHONPATH && ./venv/bin/python3 app/__main__.py

install-macosx: package ## Installs application in users Application folder
	./scripts/install-macosx.sh OnePage.app

icns: ## Generates icon files from svg
	echo "Run ./mk-icns.sh resources/icons/app.svg app"

.PHONY: help
.DEFAULT_GOAL := help

help: Makefile
	echo
	echo " Choose a command run in "$(PROJECTNAME)":"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo