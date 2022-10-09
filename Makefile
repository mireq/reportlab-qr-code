.PHONY: help test

help:
	@echo "Subcommands: test"

test:
	coverage erase
	coverage run --source=reportlab_qr_code --branch -m pytest .
	coverage report -m
	coverage html
