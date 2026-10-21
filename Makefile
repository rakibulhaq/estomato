PACKAGE := Estomato
PYTHON  ?= python3
RELEASE := $(PYTHON) scripts/release.py
DIST    := dist

.DEFAULT_GOAL := help
.PHONY: help test lint version build bump-patch bump-minor bump-major message release push clean

help: ## Show this help
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "} {printf "  %-12s %s\n", $$1, $$2}'

test: ## Run the unit tests
	$(PYTHON) -m unittest -v

lint: ## Byte-compile all Python files
	$(PYTHON) -m py_compile *.py scripts/*.py

version: ## Print the latest released version (from git tags)
	@$(RELEASE) current

build: test ## Build dist/Estomato.sublime-package from HEAD
	@mkdir -p $(DIST)
	git archive --format=zip -o $(DIST)/$(PACKAGE).sublime-package HEAD
	@unzip -l $(DIST)/$(PACKAGE).sublime-package

bump-patch: ## Start a patch release (x.y.Z) and its update message
	@$(MAKE) --no-print-directory message VERSION=$$($(RELEASE) next patch)

bump-minor: ## Start a minor release (x.Y.0) and its update message
	@$(MAKE) --no-print-directory message VERSION=$$($(RELEASE) next minor)

bump-major: ## Start a major release (X.0.0) and its update message
	@$(MAKE) --no-print-directory message VERSION=$$($(RELEASE) next major)

message: ## Create/register messages/VERSION.txt (make message VERSION=x.y.z)
	@test -n "$(VERSION)" || { echo "usage: make message VERSION=x.y.z"; exit 1; }
	@$(RELEASE) message $(VERSION)
	@echo "Edit messages/$(VERSION).txt, commit, then run make release on main."

release: test ## Tag the pending version on main (does not push)
	@test "$$(git branch --show-current)" = main || { echo "error: release from main"; exit 1; }
	@version=$$($(RELEASE) check) && \
	git tag -a "v$$version" -m "v$$version" && \
	echo "Tagged v$$version. Run make push to publish it to Package Control."

push: ## Push main and tags (publishes the release)
	git push origin main
	git push origin --tags

clean: ## Remove build output and caches
	rm -rf $(DIST) __pycache__ scripts/__pycache__
	find . -name "*.pyc" -delete
