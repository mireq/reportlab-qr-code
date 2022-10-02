# -*- coding: utf-8 -*-
from reportlab.lib.units import toLength


def gradient(canvas, params): # pylint: disable=unused-argument
	canvas.saveState()
	clip = canvas.beginPath()
	clip.rect(0, 0, toLength("5cm"), toLength("5cm"))
	canvas.clipPath(clip, stroke=0)
	canvas.linearGradient(0, 0, toLength("5cm"), toLength("5cm"), ('#ee0000', '#0033dd'))
	canvas.restoreState()
