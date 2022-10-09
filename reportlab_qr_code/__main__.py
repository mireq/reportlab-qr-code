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
	c.showPage()
	c.save()


def main():
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
	parser.set_defaults(enhanced_path=None)
	args = parser.parse_args()
	generate(args)


if __name__ == "__main__":
	main()
