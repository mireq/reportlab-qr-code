# -*- coding: utf-8 -*-
import argparse
import sys
from base64 import b64decode

from reportlab.pdfgen import canvas

from . import DEFAULT_PARAMS, clean_params, build_qrcode


def generate(args):
	text = args.text
	if text is None:
		text = sys.stdin.read()
	if args.base64:
		text = b64decode(text)

	params = DEFAULT_PARAMS.copy()
	if args.version is not None:
		params['version'] = args.version
	if args.error_correction is not None:
		params['error_correction'] = args.error_correction
	params['size'] = args.size
	params['padding'] = args.padding
	if args.fg is not None:
		params['fg'] = args.fg
	if args.bg is not None:
		params['bg'] = args.bg
	params['invert'] = bool(args.invert)
	params['radius'] = args.radius
	if args.enhanced_path is not None:
		params['enhanced_path'] = args.enhanced_path
	if args.gradient:
		params['mask'] = True
	clean_params(params)

	if isinstance(text, str):
		text = text.encode('utf-8')
	qr = build_qrcode(params, text)

	c = canvas.Canvas(
		args.outfile,
		pagesize=(qr.size, qr.size),
		pageCompression=1 if args.compress else 0
	)
	qr.save(c)

	if args.gradient:
		gradient_type, coords, colors, positions = args.gradient
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

	c.showPage()
	c.save()


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

	parser = argparse.ArgumentParser(description="Generate qr code")
	parser.add_argument('text', nargs='?', type=str, help="Input text or stdin if omitted")
	parser.add_argument('--outfile', nargs='?', type=argparse.FileType('wb'), default=sys.stdout.buffer, help="Output file or stdout if omitted")
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
	parser.add_argument('--radius', type=float, help="Round code (radius)", default=0.0)
	parser.add_argument('--enhanced-path', action='store_true', help="Enhanced path rendering")
	parser.add_argument('--no-enhanced-path', dest='enhanced_path', action='store_false')
	parser.add_argument('--gradient', type=parse_gradient, help=gradient_help)
	parser.set_defaults(compress=True)
	parser.set_defaults(enhanced_path=None)
	args = parser.parse_args()
	generate(args)


if __name__ == "__main__":
	main()
