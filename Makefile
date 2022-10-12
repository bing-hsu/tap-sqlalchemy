.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "make [target]"

build_out = dist/ build/ *.egg-info/
.PHONY: clean
clean:
	@rm -rf $(build_out)

.PHONY: build
build:
	@python -m build -w

.PHONY: unittest
unittest:
	@echo '==== Unit Test ===='
	@PYTHONPATH=. python -m unittest discover -p '*_test.py' --verbose
	@echo ''

.PHONY: test
test: unittest
	@echo '==== Integration Test ===='
	@bash test/command_test.sh
	@echo ''
