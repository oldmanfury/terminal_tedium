# Copyright (c) 2017 Adafruit Industries
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

import time
import sys, os
#import Adafruit_GPIO.SPI as SPI
#import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

#create a list of .wav files that are located in subdirectory /loops/
#exestring = "cd ./pdpatch/EBS/loops && sudo rm -f list.txt && sudo echo 'rec.wav' >> list.txt && sudo chmod 777 list.txt && sudo ls *.{[wW][aA][vV],[aA][iI][fF]} >> list.txt"
#os.system(exestring)
#
# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
knob1 = 0
knob2 = 0
knob3 = 0
knob4 = 0
knob5 = 0
fx1 = 0
fx2 = 0
fx3 = 0
fx4 = 0
#then = time.time()
#print then
line1 = str()
line2 = str()
data = str()
#data = "0: 16 15 15 16 16 15 16 15 16 16 15 16"
#data = data[3: ]
plotdata = list()
#plotdata = [int(x) for x in data.split(" ")]
#print data
#print plotdata
#----------------------------LUMA SETUP-----------------------------------------
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import sh1106
from luma.core.sprite_system import framerate_regulator
topserial = i2c(port=1, address=0x3C)
botserial = i2c(port=1, address=0x3D)
# substitute ssd1331(...) or sh1106(...) below if using that device
disptop = sh1106(topserial)
dispbot = sh1106(botserial)
#----------------------------------------------
# 128x64 display with hardware I2C:
#disptop = Adafruit_SSD1306.SSD1306_128_64B(rst=RST)
# Initialize library.
#disptop.begin()
#dispbot = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
#dispbot.begin()
regulator = framerate_regulator(fps=30)  # Unlimited
# Clear display.
disptop.clear()
#disptop.display()
dispbot.clear()
#dispbot.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disptop.width
height = disptop.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

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
# font = ImageFont.truetype('/home/pi/Roboto-Bold.ttf', 8)
font1 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Light.ttf",11)
font2 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Light.ttf",13)
font3 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Bold.ttf",20)
font4 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Bold.ttf",14)
font5 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Light.ttf",10)
font6 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Light.ttf",12)

draw.rectangle((0,0,width,height), outline=0, fill=255)
draw.text((x, top+15)," tt-EBS",  font=font3, fill=0)
draw.text((x, top+35),"  Euclidian Beat Slicer",  font=font2, fill=0)
#disptop.image(image)
disptop.display(image)

time.sleep(2)

sys.stdin.flush()
TT = sys.stdin.readline()
TT.strip()

while True:
    sys.stdin.flush()
    TT = sys.stdin.readline()
    TT.strip()
    if (TT[0:8] == "print: 1"):
        line1 = TT[8: ]
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top), "-------- SELECT LOOP --------", font=font6, fill=255)
        draw.rectangle((0,13,127,38), outline=255, fill=255)
        draw.rectangle((1,top+16,117,37), outline=0, fill=255)
	draw.text((x, top+22),str(line1),  font=font1, fill=0) 
        draw.rectangle((126,top+16,119,37), outline=0, fill=0) 
        draw.rectangle((126,top+16,119,21), outline=0, fill=255) 
	draw.text((x, top+45), "Buttons 1 & 2 to scroll", font=font5, fill=255) 
        draw.text((x, top+55), "LED button to load", font=font5, fill=255)      
        disptop.display(image)
    elif (TT[0:8] == "print: 2"):
        line2 = TT[8: ]
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top+1),    str(line2),  font=font2, fill=255)
        disptop.display(image)
    elif (TT[0:8] == 'print: Q'):#long press down button
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top+15),"Shutting Down Pi",  font=font2, fill=255)
	draw.text((x, top+35),"Please wait a few seconds",  font=font5, fill=255)
	draw.text((x, top+45),"before turning eurorack off.",  font=font5, fill=255)
        disptop.display(image)
        time.sleep(3)
        exestring = "sudo shutdown -h now"
        print (exestring)
        disptop.cleanum
        os.system(exestring)
    elif (TT[0:8] == 'print: q'):#long press up button

        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.rectangle((1,0,127,63), outline=1, fill=0)
        draw.text((5, top+20),"Launching Patch Loader",  font=font1, fill=255)
        disptop.display(image)
        time.sleep(1)
        exestring = "sudo killall -9 pd python ; sudo python /home/pi/terminal_tedium/tt-loader.py"
        os.system(exestring)        
# bottom OLED display - with knob setting bar chart
    elif (TT[0:8] == 'print: X'):
        draw.rectangle((0,0,width,height), outline=0, fill=0)
	#draw.text((x, top+2)," tt-EBS",  font=font1, fill=255)
        data = TT[10: ]
        data = data.split(' ')
        plotdata = [int(k) for k in data]
        i = 1
        while (i < 127):
            if (i < 99):
                draw.point((i,plotdata[i]), fill=255)
            elif (i == 100):
                knob1=63-plotdata[i]
                draw.rectangle((101,63,102,knob1), outline=1, fill=255)
            elif (i == 101):
                knob2=63-plotdata[i]
                draw.rectangle((106,63,107,knob2), outline=1, fill=255)                
            elif (i == 102):
                knob3=63-plotdata[i]
                draw.rectangle((111,63,112,knob3), outline=1, fill=255)                
            elif (i == 103):
                knob4=63-plotdata[i]
                draw.rectangle((116,63,117,knob4), outline=1, fill=255)                
            elif (i == 104):
                knob5=63-plotdata[i]
                draw.rectangle((121,63,122,knob5), outline=1, fill=255)                
            elif ((i == 105) and (plotdata[i]==1)):
                draw.rectangle((126,60,127,50), outline=1, fill=255)
            elif ((i == 106) and (plotdata[i]==1)):
                draw.rectangle((126,44,127,34), outline=1, fill=255)
            elif ((i == 107) and (plotdata[i])==1):
                draw.rectangle((126,30,127,20), outline=1, fill=255)
            elif ((i == 108) and (plotdata[i])==1):
                draw.rectangle((126,14,127,4), outline=1, fill=255)
            i = i + 1
#        dispbot.image(image)
        with regulator:
            dispbot.display(image)
    elif (TT[0:8] == 'print: Z'):
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        data = TT[10: ]
        data = data.split(' ')
        plotdata = [int(k) for k in data]
        plotdata[0]=32
        i = 1
        while (i < 127):
            if (i<99):
                draw.line((i-1,plotdata[i-1],i,plotdata[i]), fill=255)
            elif (i == 110):
                VUL = 63-plotdata[i]
                draw.rectangle((101,63,105,VUL), outline=1, fill=255)
            elif (i == 111):
                VUR = 63-plotdata[i]
                draw.rectangle((108,63,112,VUR), outline=1, fill=255)
            i = i + 1
#        disptop.image(image)
        with regulator:
            disptop.display(image)
#    time.sleep(.010)