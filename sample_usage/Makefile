.PHONY: all


all: test.pdf py.pdf


test.pdf: test.rml ../rml_qrcode/__init__.py
	python3 -m z3c.rml.rml2pdf test.rml

py.pdf: test.py ../rml_qrcode/__init__.py
	python test.py
