# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from rml_qrcode import qr_draw


def main():
	c = canvas.Canvas("py.pdf")
	qr_draw(c, "Hello world", "1cm", "1cm", size="19cm", bg="#eeeeee")
	c.showPage()
	c.save()


if __name__ == "__main__":
	main()
