# -*- coding: utf-8 -*-
from base64 import b64decode
from reportlab.lib.units import toLength
import qrcode


DEFAULT_PARAMS = {
	'size': '5cm',
	'padding': '2.5',
	'fg': '#000000',
	'bg': '#ffffff',
	'version': None,
	'error_correction': 'L',
}
GENERATOR_PARAMS = {'size', 'padding', 'fg', 'bg'}
QR_PARAMS = {'version', 'error_correction'}
QR_ERROR_CORRECTIONS = {
	'L': qrcode.ERROR_CORRECT_L,
	'M': qrcode.ERROR_CORRECT_M,
	'Q': qrcode.ERROR_CORRECT_Q,
	'H': qrcode.ERROR_CORRECT_H,
}


class ReportlabImageBase(qrcode.image.base.BaseImage):
	size = None
	padding = None
	bg = None
	fg = None
	rects = []

	def __init__(self, *args, **kwargs):
		self.rects = []
		super().__init__(*args, **kwargs)
		self.size = toLength(self.size)
		if '%' in self.padding:
			self.padding = float(self.padding[:-1]) * self.size / 100
		else:
			try:
				self.padding = float(self.padding)
				self.padding = (self.size / (self.width + self.padding * 2)) * self.padding
			except ValueError:
				self.padding = toLength(self.padding)

	def drawrect(self, row, col):
		self.rects.append((row, col))

	def save(self, stream, kind=None):
		stream.saveState()
		try:
			stream.setFillColor(self.bg)
			stream.rect(0, 0, self.size, self.size, fill=1, stroke=0)
			pixel_size = (self.size - self.padding * 2) / (self.width)
			stream.setFillColor(self.fg)
			for row, col in self.rects:
				stream.rect(col * pixel_size + self.padding, (self.width - row - 1) * pixel_size + self.padding, pixel_size, pixel_size, fill=1, stroke=0)
		finally:
			stream.restoreState()


def reportlab_image_factory(**kwargs):
	"""
	Returns ReportlabImage class for qrcode image_factory
	"""
	return type('ReportlabImage', (ReportlabImageBase,), kwargs)


def parse_graphic_params(params):
	"""
	Parses params string in form:

	key=value,key2=value2;(text|base64);content

	For example:

	size=5cm,fg=#ff0000,bg=#ffffff,version=1,error_correction=M,padding=5%;text;text to encode
	"""
	try:
		parsed_params, fmt, text = params.split(';', 2)
	except ValueError:
		raise ValueError("Wrong format, expected parametrs;format;content")
	if fmt not in ('text', 'base64'):
		raise ValueError("Unknown format '%s', supprted are text or base64" % fmt)

	params = DEFAULT_PARAMS.copy()
	if parsed_params:
		try:
			params.update(dict(item.split("=") for item in parsed_params.split(",")))
		except ValueError:
			raise ValueError("Wrong format of parameters '%s', expected key=value pairs delimited by ',' character" % parsed_params)

	for key, __ in params.items():
		if key not in GENERATOR_PARAMS and key not in QR_PARAMS:
			raise ValueError("Unknown attribute '%s'" % key)

	if params['version'] is not None:
		try:
			params['version'] = int(params['version'])
		except ValueError:
			raise ValueError("Version '%s' is not a number" % params['version'])

	if params['error_correction'] in QR_ERROR_CORRECTIONS:
		params['error_correction'] = QR_ERROR_CORRECTIONS[params['error_correction']]
	else:
		raise ValueError("Unknown error correction '%s', expected one of %s" % (params['error_correction'], ', '.join(QR_ERROR_CORRECTIONS.keys())))

	text = text.encode('utf-8')
	if fmt == 'base64':
		try:
			text = b64decode(text)
		except Exception as e:
			raise ValueError("Wrong base64 '%s': %s" % (text.decode('utf-8'), e))

	return params, text


def qr(canvas, params):
	"""
	Generate QR code using plugInGraphic or plugInFlowable

	Example RML code:

	<illustration height="5cm" width="5cm" align="center">
		<plugInGraphic module="reportlab_qrcode" function="qr">size=5cm;text;Simple text</plugInGraphic>
	</illustration>
	"""
	params, text = parse_graphic_params(params)
	factory_kwargs = {key: value for key, value in params.items() if key in GENERATOR_PARAMS}
	qr_kwargs = {key: value for key, value in params.items() if key in QR_PARAMS}
	img = qrcode.make(text, image_factory=reportlab_image_factory(**factory_kwargs), border=0, **qr_kwargs)
	img.save(canvas)
