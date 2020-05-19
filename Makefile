# Directory for documentation
pydoc_dir = docs

# Python code locations
app_code = bluepill/*.py
test_code = tests/*.py
package_name = "bluepill"

# Manage the location of pip-tools requirements
prod_reqs_in = setup.py
prod_reqs = requirements.txt
dev_reqs_in = dev-requirements.in
dev_reqs = dev-requirements.txt

all: clean test build

build: clean # Build the package
	@printf "\n\n\033[0;32m** Packaging (dist) **\n\n\033[0m"
	python setup.py sdist
	pip install -e .

test: clean codelint seclint unittest

# Unit test with pytest and minimum 80% coverage with coverage.py
unittest: dev-deps
	@printf "\n\n\033[0;32m** Unit testing (pytest) **\n\n\033[0m"
	python setup.py test

# Static analysis with prospector for Python code
codelint: dev-deps
	@printf "\n\n\033[0;32m** Static code analysis (prospector) **\n\n\033[0m"
	prospector

# Static security analysis for Python code
seclint: dev-deps
	@printf "\n\n\033[0;32m** Static code security analysis (bandit) **\n\n\033[0m"
	bandit $(app_code)

# apply yapf formatting
yapf: dev-deps
	@printf "\n\n\033[0;32m** Formatting (yapf) **\n\n\033[0m"
	yapf -i $(app_code) $(test_code)

# Run yapf formatting then prospector. Use this for local dev.
dev-lint: dev-deps yapf
	prospector $(app_code) $(test_code)

# Generate documentation (WIP)
docs: *.py dev-deps
	mkdir -p $(pydoc_dir) && \
	cd $(pydoc_dir) && \
	pydocmd simple topograph+

# clean artifacts between runs
clean:
	rm -rf __pycache__
	rm -rf .eggs
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf dist
	rm -rf .pytest_cache
	rm -rf .coverage
	pip uninstall $(package_name)
	@CRAWLER_LOC=`which crawler` && rm -f $$CRAWLER_LOC && echo "Cleaned local install." || echo "No local install to clean."

# This section manages environment dependencies using pip-tools

# sync the prod dependecies if they changed
prod-deps: compile-prod-reqs
	pip-sync $(prod_reqs)

# sync the dev dependencies if they changed
dev-deps: compile-dev-deps
	pip-sync $(prod_reqs) $(dev_reqs)

# compile the prod dependecies from setup.py
compile-prod-reqs:
	pip-compile

# compile the dev dependencies
compile-dev-deps: compile-prod-reqs
	pip-compile $(dev_reqs_in) --output-file ./$(dev_reqs)