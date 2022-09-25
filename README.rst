=========================================
QR code plugin for reportlab RML language
=========================================

|codecov| |version| |downloads| |license|

Install
-------

.. code:: bash

	pip install rml_qrcode

Usage
-----

This package allows insert QR codes to reportlab document.

This package can be used directly from reportlab RML file or from python code.

RML
^^^

To insert QR code from rml file use this code:

.. code:: xml

	<plugInGraphic module="rml_qrcode" function="qr">parameters;format;contents</plugInGraphic>


Parameters is key=value list delimited using ',' character, e.g.
``size=10cm,padding=1cm``.

Format is either 'text' or 'base64' for simple text and base64 encoding. QR code
contents is after second semicolon.

Complete example:

.. code:: xml

	<illustration height="5cm" width="5cm" align="center">
		<plugInGraphic module="rml_qrcode" function="qr">size=5cm,padding=0.5cm;text;Simple text</plugInGraphic>
	</illustration>

Python API
^^^^^^^^^^

QR code can be inserted to canvas using ``qr_draw(canvas, contents, **params)`` function.

.. code:: python

	from reportlab.pdfgen import canvas
	from rml_qrcode import qr_draw

	c = canvas.Canvas("out.pdf")
	qr_draw(c, "Hello world", x="1cm", y="1cm", size="10cm")

Parameter list
^^^^^^^^^^^^^^

.. list-table:: Parameters
	:header-rows: 1

	* - Name
	  - Default
	  - Description
	* - ``size``
	  - 5cm
	  - size of code
	* - ``padding``
	  - 2.5
	  - padding size, without any unit this meanss 2.5 QR code pixels, it can be
	    absolute value (like 1cm) or relative value (10%)
	* - ``fg``
	  - black
	  - foreground color
	* - ``bg``
	  - transparent
	  - background color
	* - ``version``
	  - 1
	  - version passed to qr code library
	* - ``error_correction``
	  - 'L'
	  - error_correction passed to qr code library (can be L, M, Q or H)
	* - ``x``
	  - 0
	  - x offset
	* - ``y``
	  - 0
	  - y offset

Examples
--------

RML code:

.. code:: xml

	<!DOCTYPE document SYSTEM "rml_1_0.dtd" [
	<!ENTITY lines5 "
		0cm 0cm 0cm 0.5cm
		0cm 0cm 0.5cm 0cm
		5cm 0cm 4.5cm 0cm
		5cm 0cm 5cm 0.5cm
		0cm 5cm 0.5cm 5cm
		0cm 5cm 0cm 4.5cm
		5cm 5cm 5cm 4.5cm
		5cm 5cm 4.5cm 5cm
	">
	<!ENTITY lines3 "
		0cm 0cm 0cm 0.5cm
		0cm 0cm 0.5cm 0cm
		3cm 0cm 2.5cm 0cm
		3cm 0cm 3cm 0.5cm
		0cm 3cm 0.5cm 3cm
		0cm 3cm 0cm 2.5cm
		3cm 3cm 3cm 2.5cm
		3cm 3cm 2.5cm 3cm
	">
	]>
	<document filename="test.pdf" invariant="1">
	<template pagesize="21cm,29.7cm">
		<pageTemplate id="main" pagesize="21cm,29.7cm">
			<frame id="main" x1="1cm" y1="1cm" width="19cm" height="27.7cm"/>
		</pageTemplate>
	</template>
	<stylesheet>
		<paraStyle name="Normal" fontSize="12" leading="20" spaceBefore="40" />
	</stylesheet>
	<story>
		<para style="Normal">Simple text </para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="rml_qrcode" function="qr">;text;Simple text</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Custom size</para>
		<illustration height="3cm" width="3cm" align="center">
			<plugInGraphic module="rml_qrcode" function="qr">size=3cm;text;Custom size</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines3;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Base 64 encoded</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="rml_qrcode" function="qr">;base64;QmFzZSA2NCBlbmNvZGVk</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Custom colors</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="rml_qrcode" function="qr">bg=#eeeeee,fg=#a00000;text;Custom colors</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Padding 20%</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="rml_qrcode" function="qr">padding=20%;text;Padding 20%</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Padding 1cm</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="rml_qrcode" function="qr">padding=1cm;text;Padding 1cm</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Padding 1 pixel</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="rml_qrcode" function="qr">padding=1;text;Padding 1 pixel</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Error correction M</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="rml_qrcode" function="qr">error_correction=M;text;Error correction</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Error correction L</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="rml_qrcode" function="qr">error_correction=L;text;Error correction</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<para>Version 10</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="rml_qrcode" function="qr">version=10;text;Version 10</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	</story>
	</document>

Output:

.. image:: https://raw.github.com/wiki/mireq/Reportlab-RML-qrcode/codes.png?v2022-09-17


Python code:

.. code:: python

	from reportlab.pdfgen import canvas
	from rml_qrcode import qr_draw

	def main():
		c = canvas.Canvas("py.pdf")
		qr_draw(c, "Hello world", "1cm", "1cm", size="19cm", bg="#eeeeee")
		c.showPage()
		c.save()

	if __name__ == "__main__":
		main()


.. |codecov| image:: https://codecov.io/gh/mireq/Reportlab-RML-qrcode/branch/master/graph/badge.svg?token=QGY5B5X0F3
	:target: https://codecov.io/gh/mireq/Reportlab-RML-qrcode

.. |version| image:: https://badge.fury.io/py/rml-qrcode.svg
	:target: https://pypi.python.org/pypi/rml-qrcode/

.. |downloads| image:: https://img.shields.io/pypi/dw/rml-qrcode.svg
	:target: https://pypi.python.org/pypi/rml-qrcode/

.. |license| image:: https://img.shields.io/pypi/l/rml-qrcode.svg
	:target: https://pypi.python.org/pypi/rml-qrcode/
