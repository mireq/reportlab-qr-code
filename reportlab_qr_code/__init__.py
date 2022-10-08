# -*- coding: utf-8 -*-
import array
import operator
from base64 import b64decode
from reportlab.pdfgen.canvas import FILL_EVEN_ODD

import qrcode
from reportlab.lib.units import toLength


DEFAULT_PARAMS = {
	'size': '5cm',
	'padding': '2.5',
	'fg': '#000000',
	'bg': None,
	'version': None,
	'error_correction': 'L',
	'x': 0,
	'y': 0,
	'invert': False
}
FALSE_VALUES = {'off', 'false', 'False', '0', False, 0, None}
GENERATOR_PARAMS = {'size', 'padding', 'fg', 'bg', 'x', 'y', 'invert'}
QR_PARAMS = {'version', 'error_correction'}
QR_ERROR_CORRECTIONS = {
	'L': qrcode.ERROR_CORRECT_L,
	'M': qrcode.ERROR_CORRECT_M,
	'Q': qrcode.ERROR_CORRECT_Q,
	'H': qrcode.ERROR_CORRECT_H,
}
DIRECTION = (
	( 1,  0), # right
	( 0,  1), # down
	(-1,  0), # left
	( 0, -1), # up
)
# left, straight, right
DIRECTION_TURNS_CHECKS = (
	(( 0, -1), ( 0,  0), (-1,  0)), # right
	(( 0,  0), (-1,  0), (-1, -1)), # down
	((-1,  0), (-1, -1), ( 0, -1)), # left
	((-1, -1), ( 0, -1), ( 0,  0)), # up
)


class Vector(tuple):
	def __add__(self, other):
		return self.__class__(map(operator.add, self, other))


class ReportlabImageBase(qrcode.image.base.BaseImage):
	size = None
	padding = None
	bg = None
	fg = None
	bitmap = None
	x = 0
	y = 0
	invert = False

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.invert = self.invert not in FALSE_VALUES
		self.bitmap = array.array('B', [1 if self.invert else 0] * self.width * self.width)
		self.size = toLength(self.size) if isinstance(self.size, str) else float(self.size)
		if isinstance(self.padding, str) and '%' in self.padding:
			self.padding = float(self.padding[:-1]) * self.size / 100
		else:
			try:
				self.padding = float(self.padding)
				self.padding = (self.size / (self.width + self.padding * 2)) * self.padding
			except ValueError:
				self.padding = toLength(self.padding) if isinstance(self.padding, str) else float(self.padding)
		self.x = toLength(self.x) if isinstance(self.x, str) else float(self.x)
		self.y = toLength(self.y) if isinstance(self.y, str) else float(self.y)

	def drawrect(self, row, col):
		self.bitmap_set((col, row), 0 if self.invert else 1)

	def save(self, stream, kind=None):
		stream.saveState()

		try:
			# Move to start
			stream.translate(self.x, self.y + self.size)
			stream.scale(1, -1)

			self.draw_background(stream)

			# Set foreground
			stream.setFillColor(self.fg)

			# Set transform matrix
			stream.translate(self.padding, self.padding)
			scale = (self.size - (self.padding * 2)) / self.width
			stream.scale(scale, scale)

			#self.draw_code(stream)
			self.draw_rounded_code(stream)
		finally:
			stream.restoreState()

	def draw_background(self, stream):
		"""
		Draw rectangle on background if is not transparent
		"""
		if self.bg is not None:
			stream.setFillColor(self.bg)
			stream.rect(0, 0, self.size, self.size, fill=1, stroke=0)

	def draw_code(self, stream):
		"""
		Draw QR code
		"""
		p = stream.beginPath()
		for segment in self.get_segments():
			p.moveTo(segment[0][0], segment[0][1])
			for coords in segment[1:-1]:
				p.lineTo(coords[0], coords[1])
			p.close()
		stream.drawPath(p, stroke=0, fill=1, fillMode=FILL_EVEN_ODD)

	def draw_rounded_code(self, stream):
		"""
		Draw QR code using rounded paths
		"""
		radius = 3.5
		p = stream.beginPath()
		for segment in self.get_segments():
			segment = segment[:-1]
			for i in range(0, len(segment)):
				coords = segment[i]
				prev_coords = segment[i - 1]
				next_coords = segment[(i + 1) % len(segment)]
				prev_dir = self.__calc_round_direction(prev_coords, coords, radius)
				next_dir = self.__calc_round_direction(next_coords, coords, radius)
				if i == 0:
					p.moveTo(coords[0] + prev_dir[0], coords[1] + prev_dir[1])
				else:
					p.lineTo(coords[0] + prev_dir[0], coords[1] + prev_dir[1])
				c = 0.45 # 1 - (4/3)*tan(pi/8)
				p.curveTo(
					coords[0] + prev_dir[0] * c, coords[1] + prev_dir[1] * c,
					coords[0] + next_dir[0] * c, coords[1] + next_dir[1] * c,
					coords[0] + next_dir[0], coords[1] + next_dir[1],
				)
			p.close()
		stream.drawPath(p, stroke=0, fill=1, fillMode=FILL_EVEN_ODD)

	def addr(self, coords):
		"""
		Get index to bitmap
		"""
		col, row = coords
		if row < 0 or col < 0 or row >= self.width or col >= self.width:
			return None
		return row * self.width + col

	def coord(self, addr):
		"""
		Returns bitmap coordinates from address
		"""
		return Vector((addr % self.width, addr // self.width))

	def bitmap_get(self, coords):
		"""
		Returns pixel value of bitmap
		"""
		addr = self.addr(coords)
		return 0 if addr is None else self.bitmap[addr]

	def bitmap_set(self, coords, value):
		"""
		Set pixel value of bitmap
		"""
		addr = self.addr(coords)
		self.bitmap[addr] = value

	def bitmap_invert(self, coords):
		"""
		Invert value of pixel
		"""
		addr = self.addr(coords)
		self.bitmap[addr] = 0 if self.bitmap[addr] else 1

	def get_segments(self):
		"""
		Return list of segments (vector shapes)
		"""
		segments = []
		segment = self.__consume_segment()
		while segment:
			segments.append(segment)
			segment = self.__consume_segment()
		return segments

	def __consume_segment(self):
		"""
		Returns segment of qr image as path (pairs of x, y coordinates)
		"""

		line_intersections = [[] for __ in range(self.width)]

		try:
			# Find first pixel
			coords = self.coord(self.bitmap.index(1))
		except ValueError:
			# Or no pixels left
			return

		# Accumulated path
		path = []
		# Begin of line
		path.append(tuple(coords))
		# Default direction to right
		direction = 0

		def move():
			nonlocal coords
			step = DIRECTION[direction]

			# Record intersection
			if step[1]: # Vertical move
				line = coords[1]
				if step[1] == -1:
					line -= 1
				line_intersections[line].append(coords[0])

			# Step
			coords += step

		# Move to right
		move()

		# From shape begin to end
		while coords != path[0]:
			# Trun left
			val = self.bitmap_get(coords + DIRECTION_TURNS_CHECKS[direction][0])
			if val:
				path.append(tuple(coords))
				direction = (direction - 1) % 4
				move()
				continue

			# Straight
			val = self.bitmap_get(coords + DIRECTION_TURNS_CHECKS[direction][1])
			if val:
				move()
				continue

			# Trun right
			path.append(tuple(coords))
			direction = (direction + 1) % 4
			move()

		path.append(tuple(coords))

		# Remove shape from bitmap
		for row, line in enumerate(line_intersections):
			line = sorted(line)
			for start, end in zip(line[::2], line[1::2]):
				for col in range(start, end):
					self.bitmap_invert((col, row))

		return path

	def __calc_round_direction(self, src, dst, radius):
		return [min(max((s - d) * 0.5, -radius), radius) for s, d in zip(src, dst)]



def reportlab_image_factory(**kwargs):
	"""
	Returns ReportlabImage class for qrcode image_factory
	"""
	return type('ReportlabImage', (ReportlabImageBase,), kwargs)


def clean_params(params):
	"""
	Validate and clean parameters
	"""

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

	clean_params(params)

	text = text.encode('utf-8')
	if fmt == 'base64':
		try:
			text = b64decode(text)
		except Exception as e:
			raise ValueError("Wrong base64 '%s': %s" % (text.decode('utf-8'), e))

	return params, text


def build_qrcode(params, text):
	factory_kwargs = {key: value for key, value in params.items() if key in GENERATOR_PARAMS}
	qr_kwargs = {key: value for key, value in params.items() if key in QR_PARAMS}
	return qrcode.make(text, image_factory=reportlab_image_factory(**factory_kwargs), border=0, **qr_kwargs)


def qr_factory(params):
	params, text = parse_graphic_params(params)
	return build_qrcode(params, text)


def qr_draw(canvas, text, **kwargs):
	params = DEFAULT_PARAMS.copy()
	params.update(**kwargs)
	clean_params(params)
	if isinstance(text, str):
		text = text.encode('utf-8')
	build_qrcode(params, text).save(canvas)


def qr(canvas, params=None):
	"""
	Generate QR code using plugInGraphic or plugInFlowable

	Example RML code:

	<illustration height="5cm" width="5cm" align="center">
		<plugInGraphic module="reportlab_qrcode" function="qr">size=5cm;text;Simple text</plugInGraphic>
	</illustration>
	"""
	build_qrcode(*parse_graphic_params(params)).save(canvas)
