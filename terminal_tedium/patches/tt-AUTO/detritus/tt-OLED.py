# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time, math
import sys, os, datetime
import Adafruit_GPIO.SPI as SPI
#import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
brite = 200
knob1 = 0
knob2 = 0
knob3 = 0
knob4 = 0
knob5 = 0
knob6 = 0
L = 0
R = 0
prevL = 0
prevR = 0
#then = time.time()
#print then
line1 = str()
line2 = str()
line3 = str()
line4 = str()
data = str()
knobnames = list()
knobnames = ['k1','k2','k3','k4','k5','k6']
header = 11
#data = "0: 16 15 15 16 16 15 16 15 16 16 15 16"
#data = data[3: ]
plotdata = list()
#plotdata = [int(x) for x in data.split(" ")]
#print data
#print plotdata
#----------------------------LUMA SETUP-----------------------------------------
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core.sprite_system import framerate_regulator
from luma.oled.device import sh1106
from luma.core.render import canvas

topserial = i2c(port=1, address=0x3C)
botserial = i2c(port=1, address=0x3D)
regulator = framerate_regulator(fps=20)  # 0 =unlimited
disptop = sh1106(topserial)
dispbot = sh1106(botserial)
#----------------------------------------------
import datetime
from datetime import timedelta
start_time = datetime.datetime.now()

#    time.sleep(0.01)
#----------------------------
# 128x64 display with hardware I2C:
#disptop = Adafruit_SSD1306.SSD1306_128_64B(rst=RST)
# Initialize library.
#disptop.begin()
#dispbot = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
#dispbot.begin()
# Clear display.
disptop.clear()
#disptop.display()
dispbot.clear()
#dispbot.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disptop.width
height = disptop.height
image_top = Image.new('1', (width, height))
image_bot = Image.new('1', (width, height))
# Get drawing object to draw on image.
drawtop = ImageDraw.Draw(image_top)
drawbot = ImageDraw.Draw(image_bot)

# Draw a black filled box to clear the image.
drawtop.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)
font1 = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Light.ttf",12)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Light.ttf",14)
font3 = ImageFont.truetype("/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf",24)

drawtop.rectangle((0,0,width,height), outline=0, fill=brite)
drawtop.text((x, top+16),"   tt-AUTO",  font=font3, fill=0)
disptop.display(image_top)
#time.sleep(1)

sys.stdin.flush()
TT = sys.stdin.readline()
TT.strip()
drawbot.rectangle((0,0,width,height), outline=0, fill=0)   
today_last_time = "Unknown"      

while True:
    sys.stdin.flush()
    TT = sys.stdin.readline()
    TT.strip()
    if (TT[0:6] == 'OLED Q'):# long press down button   
        drawtop.rectangle((0,0,width,height), outline=0, fill=brite)
        drawtop.text((x, top+1),"SHUTDOWN",  font=font2, fill=0)
        disptop.display(image_top)
        exestring = "sudo shutdown -h now"
        print (exestring)
        disptop.cleanum
        os.system(exestring)
    elif (TT[0:6] == 'OLED q'):# long press up button   
        drawtop.rectangle((0,0,width,height), outline=0, fill=brite)
        drawtop.text((x, top+1),"PATCHLOADER",  font=font2, fill=0)
        disptop.display(image_top)
        time.sleep(1)
        exestring = "sudo killall -9 pd python ; sudo python /home/pi/terminal_tedium/tt-loader.py"
        print (exestring)
        os.system(exestring)        
#OLED labels: LD1 LD2 FdBk RD1 RD2 BPM
#012345678901    
    elif (TT[0:10] == 'knobnames:'):
        data = TT[11: ]
        data.rstrip("\n\r")
        data = data.split(' ')
        knobnames = [str(k) for k in data]
# bottom OLED display - with knob setting bar chart
#OLED E: 120 0 0 0.833333 1.16667 0.75 0.5 1.6 0 120
#01234567
    elif (TT[0:11] == 'screendata:'):
        drawbot.rectangle((0,0,width,height), outline=0, fill=0)
        data = TT[12: ]
#        print data
        data = data.split(' ')
        plotdata = [float(k) for k in data]
        K1=plotdata[0]
        K2=plotdata[1]
        K3=plotdata[2]
        K4=plotdata[3]
        K5=plotdata[4]
        K6=plotdata[5] 
        K7=plotdata[6]
        K8=plotdata[7]         
        K9=plotdata[8]
        K10=plotdata[9]         
#        drawtop
        drawtop.rectangle((0,0,width,height), outline=brite, fill=brite)
        drawtop.rectangle((0,top+17,width,47), outline=0, fill=0)
        drawtop.text((x+2, top+18), str('{:01.2f}'.format(K1)),  font=font1, fill=brite)
        drawtop.text((x+2, top-1), knobnames[0], font=font2, fill=0)            
        drawtop.text((46, top+18), str('{:01.2f}'.format(K2)),  font=font1, fill=brite)
        drawtop.text((46, top-1), knobnames[1], font=font2, fill=0)            
        drawtop.text((88, top+18), str('{:01.2f}'.format(K3)),  font=font1, fill=brite)
        drawtop.text((88, top-1), knobnames[2], font=font2, fill=0)            
        drawtop.text((x+2, top+33), str('{:01.2f}'.format(K4)),  font=font1, fill=brite)
        drawtop.text((x+2, top+48), knobnames[3], font=font2, fill=0)            
        drawtop.text((46, top+33), str('{:01.2f}'.format(K5)),  font=font1, fill=brite)
        drawtop.text((46, top+48), knobnames[4],  font=font2, fill=0)            
        drawtop.text((88, top+33), str('{:01.2f}'.format(K6)),  font=font1, fill=brite)
        drawtop.text((88, top+48), knobnames[5],  font=font2, fill=0)            
        drawtop.rectangle((117,48,118,(48-K9)),outline=brite, fill=brite)
        drawtop.rectangle((120,48,121,(48-K10)),outline=brite, fill=brite)
        drawtop.rectangle((123,48,124,(48-K7)),outline=brite, fill=brite)
        drawtop.rectangle((126,48,127,(48-K8)),outline=brite, fill=brite)        
        
#    elif (TT[0:6] == 'scope:'):
#        data = TT[12: ]
#        data = data.split(' ')
#        plotdata = [float(k) for k in data]        
        with canvas(dispbot) as draw:
            i = header+1 
            plotdata[header]= 16            
            while (i < 128+header):
                draw.line((i-header-1,plotdata[i-1],(i-header),plotdata[i]), fill=255)
                i += 1
#            i+=1
            plotdata[128+header+1]=48
            while (i < 256+header):
                draw.line((i-(128+header+1),plotdata[i-1],i-(128+header),plotdata[i]), fill=255)
                i += 1
            
    with regulator:
        disptop.display(image_top)
#        dispbot.display(image_bot)
#        disco(warp)
