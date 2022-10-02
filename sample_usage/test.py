# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab_qr_code import qr_draw


def main():
	c = canvas.Canvas("py.pdf")
	qr_draw(c, "Hello world", x="1cm", y="1cm", size="19cm", bg="#eeeeee")
	c.showPage()
	c.save()


if __name__ == "__main__":
	main()
