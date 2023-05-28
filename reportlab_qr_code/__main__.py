# -*- coding: utf-8 -*-
import argparse
import sys
from base64 import b64decode
from copy import deepcopy

from reportlab.pdfgen import canvas

from . import DEFAULT_PARAMS, clean_params, build_qrcode


def generate(text, c, **args):
	params = DEFAULT_PARAMS.copy()
	if args['version'] is not None:
		params['version'] = args['version']
	if args['error_correction'] is not None:
		params['error_correction'] = args['error_correction']
	params['size'] = args['size']
	params['padding'] = args['padding']
	if args['fg'] is not None:
		params['fg'] = args['fg']
	if args['bg'] is not None:
		params['bg'] = args['bg']
	params['invert'] = bool(args['invert'])
	params['negative'] = bool(args['negative'])
	params['radius'] = args['radius']
	if args['hole']:
		params['hole'] = args['hole']
	if args['enhanced_path'] is not None:
		params['enhanced_path'] = args['enhanced_path']
	if args['gradient']:
		params['mask'] = True
	if args['draw'] is not None:
		params['draw_parts'] = [{'draw': args['draw']}]
	clean_params(params)

	if isinstance(text, str):
		text = text.encode('utf-8')
	qr = build_qrcode(params, text)

	c.setPageSize((qr.size, qr.size))
	qr.save(c)

	if args['gradient']:
		gradient_type, coords, colors, positions = args['gradient']
		if len(colors) == 1:
			c.setFillColor(colors[0][1])
			c.rect(0, 0, qr.size, qr.size, fill=1, stroke=0)
		else:
			if gradient_type == 'linear':
				coords = [
					coords[0] * qr.size, (1.0 - coords[1]) * qr.size,
					coords[2] * qr.size, (1.0 - coords[3]) * qr.size,
				]
				c.linearGradient(*coords, colors=colors, positions=positions)
			else:
				coords = [
					coords[0] * qr.size, (1.0 - coords[1]) * qr.size,
					coords[2] * qr.size,
				]
				c.radialGradient(*coords, colors=colors, positions=positions)


def parse_gradient(val):
	try:
		steps = []

		val = val.split()
		if len(val) == 0:
			raise ValueError("Invalid format")
		gradient_type = val[0]
		coords = []
		if gradient_type == 'linear':
			if len(gradient_type) < 5:
				raise ValueError("Invalid format")
			coords = val[1:5]
			val = val[5:]
		elif gradient_type == 'radial':
			if len(gradient_type) < 4:
				raise ValueError("Invalid format")
			coords = val[1:4]
			val = val[4:]
		else:
			raise ValueError("Invalid format")
		coords = [float(pos) for pos in coords]

		# Interate over positions and colors
		position = None
		for color in val:
			if color[:1] == '#':
				steps.append([position, color])
				position = None
			else:
				position = float(color)

		if len(steps) < 1:
			raise ValueError("Invalid format")

		# Set first and last step if is not set
		if steps[-1][0] is None:
			steps[-1][0] = 1
		if steps[0][0] is None:
			steps[0][0] = 0

		# Fill gaps
		last_position = steps[0][0]
		gap = 0
		for i, step in enumerate(steps):
			position = step[0]
			if position is None:
				gap += 1
			elif gap:
				distance = position - last_position
				for index in range(i - gap, i):
					position = last_position + (index - i + gap + 1) * distance / (gap + 1)
					steps[index][0] = position
				gap = 0
			if position is not None:
				last_position = position

		return (gradient_type, coords, [step[1] for step in steps], [step[0] for step in steps])
	except Exception as e:
		sys.stdout.write(str(e))
		sys.stdout.write('\n')
		raise


def main():
	gradient_help = """
Either "linear x1 y1 x2 y2 colors" or "radial x y radius colors" Dimensions are
in range [0, 1], position (0, 0) is top left corner, (1, 1) is bottom right
corner.
Colors is list "[position] color" e.g. "0.0 #ffffff 1.0 #000000". Position is
optional. Without position argument, distances are calculated automatically.
Example: --gradient "linear 0.0 0.0 0.1 1.0 0.5 \#1050c0 0.3 \#1050c0 0.7 \#e0e000"
	"""
	area_help = """
Coordinates in form x:y:w:h. Allowed are absolute length units, relative units (%%)
and pixels (without unit suffix).
"""
	draw_help = """
Select area to draw. Possuble values are: 'all', 'eye[1-3]', 'eyes',
'eyepupil[1-3]', 'eyepupils', 'eyeball[1-3]', 'eyeballs', 'align',
'alignpupils', 'alignballs'. It's possible to combine operations with +/-
symbol e.g. all-eyes-align. To show only eye1 and eye3 without pupil it's
possible to write something like eye1+eye3-eyepupil3. Arguments passed before
first draw are globally set. Arguments after draw are specific for preceding
draw call.
"""

	parser = argparse.ArgumentParser(description="Generate qr code")
	parser.add_argument('text', nargs='?', type=str, help="Input text or stdin if omitted")
	parser.add_argument('--outfile', nargs='?', help="Output file or stdout if omitted")
	parser.add_argument('--base64', action='store_true', help="Base64 encoded text")
	parser.add_argument('--compress', action='store_true', help="PDF compression (default enabled)")
	parser.add_argument('--no-compress', dest='compress', action='store_false')
	parser.add_argument('--version', type=int, help="QR code version")
	parser.add_argument('--error_correction', type=str, choices=['L', 'M', 'Q', 'H'], help="Error correction strength")
	parser.add_argument('--size', type=str, default='5cm', help="Code size")
	parser.add_argument('--padding', type=str, default='2.5', help="Padding")
	parser.add_argument('--fg', type=str, help="Foreground color")
	parser.add_argument('--bg', type=str, help="Background color")
	parser.add_argument('--invert', action='store_true', help="Invert")
	parser.add_argument('--negative', action='store_true', help="Render negative")
	parser.add_argument('--radius', type=float, help="Round code (radius)", default=0.0)
	parser.add_argument('--enhanced-path', action='store_true', help="Enhanced path rendering")
	parser.add_argument('--no-enhanced-path', dest='enhanced_path', action='store_false')
	parser.add_argument('--gradient', type=parse_gradient, help=gradient_help)
	parser.add_argument('--hole', type=str, help=area_help)
	parser.add_argument('--draw', type=str, help=draw_help)
	parser.set_defaults(compress=True)
	parser.set_defaults(enhanced_path=None)

	# split arguments with draw command
	arg_list = []
	arg_lists = [arg_list]
	for arg in sys.argv[1:]:
		if arg == '--draw' or arg.startswith('--draw='):
			arg_list = ['--draw']
			arg_lists.append(arg_list)
			if arg.startswith('--draw='):
				arg_list.append(arg[7:])
		else:
			arg_list.append(arg)

	base_args = vars(parser.parse_args(arg_lists[0]))
	text = base_args.pop('text')
	if text is None:
		text = sys.stdin.read()
	if base_args['base64']:
		text = b64decode(text)

	if not base_args['outfile'] or base_args['outfile'] == '-':
		output = sys.stdout.buffer
	else:
		output = open(base_args['outfile'], 'wb')

	c = canvas.Canvas(
		output,
		pageCompression=1 if base_args['compress'] else 0
	)

	try:
		if len(arg_lists) == 1:
			generate(text, c, **base_args)
		else:
			for arg_list in arg_lists[1:]:
				arguments = vars(parser.parse_args(arg_list))
				arguments.pop('text')
				args = deepcopy(base_args)
				args.update(arguments)
				generate(text, c, **args)
		c.showPage()
		c.save()
	finally:
		if output is not sys.stdout.buffer:
			output.close()


if __name__ == "__main__":
	main()
