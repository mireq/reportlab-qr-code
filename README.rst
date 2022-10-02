=========================================
QR code plugin for reportlab RML language
=========================================

|codecov| |version| |downloads| |license|

Install
-------

.. code:: bash

	pip install reportlab_qr_code_generator

Why is this better than x?
--------------------------

**Including image to PDF**

Images are blurry.

**reportlab-qrcode**

Reportlab qrcode is vector QR code generator for reportlab. My project is better
in some aspects:

Images can be directly added to Reportlab RML code.

Better rendering:

.. image:: https://raw.github.com/wiki/mireq/reportlab-qr-code/rendering.png?v2022-10-02

This library merges adjacent blocks to single area whihch produces image without
gaps in every situation.

Smaller output

Hello world using reportlab-qrcode produces vector image with size 9 239 bytes.
My code with produces only 1 984 bytes (78.5 reduction in size).

Customizable colors

Usage
-----

This package allows insert QR codes to reportlab document.

This package can be used directly from reportlab RML file or from python code.

RML
^^^

To insert QR code from rml file use this code:

.. code:: xml

	<plugInGraphic module="reportlab_qr_code" function="qr">parameters;format;contents</plugInGraphic>


Parameters is key=value list delimited using ',' character, e.g.
``size=10cm,padding=1cm``.

Format is either 'text' or 'base64' for simple text and base64 encoding. QR code
contents is after second semicolon.

Complete example:

.. code:: xml

	<illustration height="5cm" width="5cm" align="center">
		<plugInGraphic module="reportlab_qr_code" function="qr">size=5cm,padding=0.5cm;text;Simple text</plugInGraphic>
	</illustration>

Python API
^^^^^^^^^^

QR code can be inserted to canvas using ``qr_draw(canvas, contents, **params)`` function.

.. code:: python

	from reportlab.pdfgen import canvas
	from reportlab_qr_code import qr_draw

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

Python examle:

.. code:: python

	from reportlab.pdfgen import canvas
	from reportlab_qr_code import qr_draw

	def main():
		c = canvas.Canvas("py.pdf")
		qr_draw(c, "Hello world", x="1cm", y="1cm", size="19cm", bg="#eeeeee")
		c.showPage()
		c.save()

	if __name__ == "__main__":
		main()

RML document example:

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
	<document filename="test.pdf" invariant="1" compression="1">
	<template>
		<pageTemplate id="main" pagesize="17cm,25cm">
			<frame id="main" x1="0.5cm" y1="0.0cm" width="5cm" height="25cm"/>
			<frame id="main" x1="6cm" y1="0.0cm" width="5cm" height="25cm"/>
			<frame id="main" x1="11.5cm" y1="0.0cm" width="5cm" height="25cm"/>
		</pageTemplate>
	</template>
	<stylesheet>
		<paraStyle name="Normal" fontSize="12" leading="16" spaceBefore="16" />
	</stylesheet>
	<story>
		<para style="Normal">Simple text </para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="reportlab_qr_code" function="qr">;text;Simple text</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Custom size</para>
		<illustration height="3cm" width="3cm" align="center">
			<plugInGraphic module="reportlab_qr_code" function="qr">size=3cm;text;Custom size</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines3;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Base 64 encoded</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="reportlab_qr_code" function="qr">;base64;QmFzZSA2NCBlbmNvZGVk</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Custom colors</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="reportlab_qr_code" function="qr">bg=#eeeeee,fg=#a00000;text;Custom colors</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Padding 20%</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="reportlab_qr_code" function="qr">padding=20%;text;Padding 20%</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Padding 1cm</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="reportlab_qr_code" function="qr">padding=1cm;text;Padding 1cm</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Padding 1 pixel</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="reportlab_qr_code" function="qr">padding=1;text;Padding 1 pixel</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Error correction M</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="reportlab_qr_code" function="qr">error_correction=M;text;Error correction</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Error correction L</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="reportlab_qr_code" function="qr">error_correction=L;text;Error correction</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<condPageBreak height="7cm"/>
	
		<para>Version 10</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic module="reportlab_qr_code" function="qr">version=10;text;Version 10</plugInGraphic>
			<lineMode width="0.5" /><lines>&lines5;</lines>
		</illustration>
	
		<!--
		<condPageBreak height="7cm"/>
	
		<para>Inverted</para>
		<illustration height="5cm" width="5cm" align="center">
			<plugInGraphic baseDir="." module="utils" function="gradient" />
			<plugInGraphic module="reportlab_qr_code" function="qr">padding=0,fg=#ffffff,invert=1;text;Inverted</plugInGraphic>
			<lineMode width="2" />
			<stroke color="#ffffff" />
			<rect x="0" y="0" width="5cm" height="5cm" fill="0" stroke="1" strokeColor="red" />
		</illustration>
		-->
	</story>
	</document>


Output:

.. image:: https://raw.github.com/wiki/mireq/reportlab-qr-code/codes.png?v2022-10-02


.. |codecov| image:: https://codecov.io/gh/mireq/reportlab-qr-code/branch/master/graph/badge.svg?token=QGY5B5X0F3
	:target: https://codecov.io/gh/mireq/reportlab-qr-code

.. |version| image:: https://badge.fury.io/py/reportlab-qr-code-generator.svg
	:target: https://pypi.python.org/pypi/reportlab-qr-code-generator/

.. |downloads| image:: https://img.shields.io/pypi/dw/reportlab-qr-code-generator.svg
	:target: https://pypi.python.org/pypi/reportlab-qr-code-generator/

.. |license| image:: https://img.shields.io/pypi/l/reportlab-qr-code-generator.svg
	:target: https://pypi.python.org/pypi/reportlab-qr-code-generator/
