.PHONY: all test_pdf py_pdf


all: test_pdf py_pdf


test_pdf: test.rml ../reportlab_qr_code/__init__.py
	python3 -m z3c.rml.rml2pdf test.rml

py_pdf: test.py ../reportlab_qr_code/__init__.py
	python test.py
