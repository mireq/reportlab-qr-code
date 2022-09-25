# -*- coding: utf-8 -*-
import array
import math

import pytest
from reportlab.pdfgen import canvas
from reportlab.lib.units import toLength

from rml_qrcode import qr, qr_factory, qr_draw, reportlab_image_factory, DEFAULT_PARAMS


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
	qr(get_canvas(), 'size=3cm;text;Custom size') # check generator errors
	img = qr_factory('size=3cm;text;Custom size')
	assert img.size == toLength("3cm")


def test_custom_colors():
	c = get_canvas()
	qr(c, 'bg=#eeeeee,fg=#a00000;text;Custom colors')


def test_custom_percentage_padding():
	qr(get_canvas(), 'padding=20%;text;Padding 20%')
	img = qr_factory('size=100,padding=20%;text;Padding 20%')
	assert img.padding == 20.


def test_custom_absolute_padding():
	qr(get_canvas(), 'padding=1cm;text;Padding 1cm')
	img = qr_factory('padding=1cm;text;Padding 1cm')
	assert img.padding == pytest.approx(toLength('1cm'), 0.01)


def test_custom_pixel_padding():
	qr(get_canvas(), 'padding=1;text;Padding 1 pixel')
	img = qr_factory('padding=1;text;Padding 1 pixel')
	padding_size = img.padding
	pixel_size = img.size / (img.width + 2.0)
	assert padding_size == pytest.approx(pixel_size, 0.01)


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


def draw_image(bitmap):
	width = int(math.sqrt(len(bitmap)))
	img = reportlab_image_factory(**DEFAULT_PARAMS)(border=0, width=width, box_size=1)
	for address, val in enumerate(bitmap):
		if val:
			img.drawrect(address // width, address % width)
	return img


def test_simple_path():
	# single square
	bitmap = array.array('B', [
		1,
	])

	img = draw_image(bitmap)
	# Outline
	assert img.get_segments() == [[(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]]


def test_complex_path():
	bitmap = array.array('B', [
		1, 1,
		1, 0,
	])

	img = draw_image(bitmap)
	assert img.get_segments() == [[(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2), (0, 0)]]


def test_multiple_intersections():
	bitmap = array.array('B', [
		1, 1, 1, 1, 1,
		0, 0, 1, 1, 1,
		0, 0, 1, 0, 1,
		0, 0, 0, 0, 1,
		0, 0, 0, 0, 1,
	])
	img = draw_image(bitmap)
	assert img.get_segments() == [[(0, 0), (5, 0), (5, 5), (4, 5), (4, 2), (3, 2), (3, 3), (2, 3), (2, 1), (0, 1), (0, 0)]]


def test_two_segments():
	bitmap = array.array('B', [
		1, 1, 0, 0, 0,
		1, 1, 0, 0, 0,
		0, 0, 0, 0, 0,
		0, 0, 0, 1, 1,
		0, 0, 0, 1, 1,
	])
	img = draw_image(bitmap)
	assert img.get_segments() == [
		[(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)],
		[(3, 3), (5, 3), (5, 5), (3, 5), (3, 3)],
	]


def test_segment_inside():
	bitmap = array.array('B', [
		1, 1, 1, 1, 1,
		1, 0, 0, 0, 1,
		1, 0, 1, 0, 1,
		1, 0, 0, 0, 1,
		1, 1, 1, 1, 1,
	])
	img = draw_image(bitmap)
	assert img.get_segments() == [
		[(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)],
		[(1, 1), (4, 1), (4, 4), (1, 4), (1, 1)],
		[(2, 2), (3, 2), (3, 3), (2, 3), (2, 2)],
	]


def test_python_api():
	c = get_canvas()
	qr_draw(c, "Text")


def test_python_api_binary_data():
	c = get_canvas()
	qr_draw(c, b"Binary")


def test_python_api_offset():
	c = get_canvas()
	qr_draw(c, "Text", x="1cm", y="1cm", size=5, padding=5)
