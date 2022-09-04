# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from rml_qrcode import qr
import pytest


def get_canvas():
	return canvas.Canvas("hello.pdf")


def test_simple():
	c = get_canvas()
	qr(c, ';text;Text')


def test_wrong_format():
	c = get_canvas()
	with pytest.raises(ValueError, match=r"Wrong format, .*"):
		qr(c, ';')

def test_wrong_params_format():
	c = get_canvas()
	with pytest.raises(ValueError, match=r"Wrong format of parameters .*"):
		qr(c, 'xx;text;Text')


def test_wrong_params():
	c = get_canvas()
	with pytest.raises(ValueError, match=r"Unknown attribute .*"):
		qr(c, 'xx=yy;text;Text')


def test_unknown_format():
	c = get_canvas()
	with pytest.raises(ValueError, match=r"Unknown format .*"):
		qr(c, ';wrong;Text')


def test_base64():
	c = get_canvas()
	qr(c, ';base64;QmFzZSA2NCBlbmNvZGVk')


def test_wrong_base64_padding():
	c = get_canvas()
	with pytest.raises(ValueError, match=r"Wrong base64 .*"):
		qr(c, ';base64;ze')


def test_custom_size():
	c = get_canvas()
	qr(c, 'size=3cm;text;Custom size')


def test_custom_colors():
	c = get_canvas()
	qr(c, 'bg=#eeeeee,fg=#a00000;text;Custom colors')


def test_custom_percentage_padding():
	c = get_canvas()
	qr(c, 'padding=20%;text;Padding 20%')


def test_custom_absolute_padding():
	c = get_canvas()
	qr(c, 'padding=1cm;text;Padding 1cm')


def test_custom_pixel_padding():
	c = get_canvas()
	qr(c, 'padding=1;text;Padding 1 pixel')


def test_custom_error_correction():
	c = get_canvas()
	qr(c, 'error_correction=M;text;Error correction')


def test_unknown_error_correction():
	c = get_canvas()
	with pytest.raises(ValueError, match=r"Unknown error correction .*"):
		qr(c, 'error_correction=X;text;Error correction')


def test_custom_version():
	c = get_canvas()
	qr(c, 'version=10;text;Version 10')


def test_not_number_version():
	c = get_canvas()
	with pytest.raises(ValueError, match=r"Version .* is not a number"):
		qr(c, 'version=xx;text;Text')
