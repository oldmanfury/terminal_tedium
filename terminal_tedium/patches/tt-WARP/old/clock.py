#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
An analog clockface with date & time.

Ported from:
https://gist.github.com/TheRayTracer/dd12c498e3ecb9b8b47f#file-clock-py
"""

import math
import time

from luma.core.render import canvas
#----------------------------LUMA SETUP-----------------------------------------
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator
from luma.oled.device import sh1106

topserial = i2c(port=1, address=0x3C)
botserial = i2c(port=1, address=0x3D)
regulator = framerate_regulator(fps=40)  # 0 =unlimited
disptop = sh1106(topserial)
dispbot = sh1106(botserial)
#----------------------------------------------
import datetime
from datetime import timedelta
start_time = datetime.datetime.now()

def posn(angle, arm_length):
    dx = int(math.cos(math.radians(angle)) * arm_length)
    dy = int(math.sin(math.radians(angle)) * arm_length)
    return (dx, dy)
#--------------------------------
# returns the elapsed milliseconds since the start of the program
def millis():
   dt = datetime.datetime.now() - start_time
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms
#----------------------------
amplitude = 10
def disco(amplitude):
    with canvas(dispbot) as draw:
        margin = 4
        cx = 99
        cy = min(dispbot.height, 64) / 2

        left = cx - cy
        right = cx + cy

        sec_angle = 270 + (360* millis()/1800)
        warble = amplitude*math.cos(math.radians(sec_angle))
        secs = posn(sec_angle, cy - margin - 2 - warble)

        draw.ellipse((left + margin, margin, right - margin, min(dispbot.height, 64) - margin), outline="white")
        draw.line((cx, cy, cx + secs[0], cy + secs[1]), fill="red")
        draw.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=255, outline=255)
        draw.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=0, outline=0)                

    time.sleep(0.01)
while (True):
    disco(10)
