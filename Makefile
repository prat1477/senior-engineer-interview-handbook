.PHONY: help install serve build clean

help:
	@echo "  install  pip install -r requirements.txt"
	@echo "  serve    mkdocs serve"
	@echo "  build    mkdocs build --clean --strict"
	@echo "  clean    rm -rf site"

install:
	pip install -r requirements.txt

serve:
	mkdocs serve

build:
	mkdocs build --clean --strict

clean:
	rm -rf site
