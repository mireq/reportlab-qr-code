# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab_qr_code import qr_draw


def main():
	c = canvas.Canvas("py.pdf", pageCompression=0)
	#qr_draw(c, "Hello world", x="1cm", y="1cm", size="19cm", bg="#eeeeee")
	qr_draw(c, "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum rhoncus auctor purus nec pellentesque. Donec porta consectetur nisl, ut mattis felis tincidunt id. Phasellus vehicula placerat nulla sit amet efficitur. Sed in aliquam justo, at convallis nisi. Vivamus interdum felis eget hendrerit iaculis. Morbi vel odio congue, ultrices dolor id, tincidunt sapien. Suspendisse eu venenatis erat, ut luctus turpis. Nullam ac ligula lacinia leo blandit varius. Maecenas accumsan condimentum quam. Nullam laoreet ipsum eget arcu finibus, et dictum arcu pulvinar. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec facilisis massa felis, id blandit sapien pharetra sollicitudin. Vivamus hendrerit gravida varius.", x="1cm", y="1cm", size="19cm", error_correction='L')
	c.showPage()
	c.save()


if __name__ == "__main__":
	main()
