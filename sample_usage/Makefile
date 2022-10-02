.PHONY: all


all: test.pdf py.pdf


test.pdf: test.rml ../reportlab_qr_code/__init__.py
	python3 -m z3c.rml.rml2pdf test.rml

py.pdf: test.py ../reportlab_qr_code/__init__.py
	python test.py
