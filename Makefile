UV ?= uv
DOCS_PORT ?= 8000

default: help

-include tasks/Makefile.*

## Check required developer tools are installed
deps:
	@which $(UV)

## Install project dependencies (including dev)
install: deps
	$(UV) sync --all-extras --dev

## Format source code
fmt: deps
	$(UV) run ruff format .

## Lint source code
lint: deps
	$(UV) run ruff check .

## Build project artifacts
build: entangled/tangle

## Run all checks
all: lint

## This help screen
help:
	@printf "Available targets:\n\n"
	@awk '/^[a-zA-Z\-_0-9%:\\/]+/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = $$1; \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			gsub("\\\\", "", helpCommand); \
			gsub(":+$$", "", helpCommand); \
			printf "  \x1b[32;01m%-35s\x1b[0m %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort -u
	@printf "\n"
