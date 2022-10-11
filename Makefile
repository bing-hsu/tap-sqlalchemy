.DEFAULT_GOAL := help

.PHONY : help
help :
	@echo "make [target]"

build_out = dist/ build/ *.egg-info/
.PHONY : clean
clean :
	@rm -rf $(build_out)

.PHONY : build
build :
	@python -m build -w
