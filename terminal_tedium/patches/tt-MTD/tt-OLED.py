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
import Adafruit_GPIO.SPI as SPI
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
brite = 55
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

topserial = i2c(port=1, address=0x3C)
botserial = i2c(port=1, address=0x3D)
regulator = framerate_regulator(fps=40)  # 0 =unlimited
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
font1 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Light.ttf",11)
font2 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Light.ttf",13)
font3 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Bold.ttf",20)
font4 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Bold.ttf",14)
font5 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Light.ttf",10)

drawtop.rectangle((0,0,width,height), outline=0, fill=brite)
drawtop.text((x, top+15)," tt-MTD",  font=font3, fill=0)
drawtop.text((x, top+35),"  Multi-Tap Delay",  font=font2, fill=0)
disptop.display(image_top)

time.sleep(2)

sys.stdin.flush()
TT = sys.stdin.readline()
TT.strip()
drawbot.rectangle((0,0,width,height), outline=0, fill=0)        
while True:
    sys.stdin.flush()
    TT = sys.stdin.readline()
    TT.strip()
    if (TT[0:6] == 'OLED Q'):# long press down button   
        drawtop.rectangle((0,0,width,height), outline=0, fill=0)
        drawtop.text((x, top+15),"Shutting Down Pi",  font=font2, fill=255)
        drawtop.text((x, top+35),"Please wait a few seconds",  font=font5, fill=255)
        drawtop.text((x, top+45),"before turning eurorack off.",  font=font5, fill=255)
        disptop.display(image_top)
        time.sleep(3)
        exestring = "sudo shutdown -h now"
        print (exestring)
        disptop.cleanum
        os.system(exestring)
    elif (TT[0:6] == 'OLED q'):# long press up button   
        
        drawtop.rectangle((0,0,width,height), outline=0, fill=0)
        drawtop.rectangle((1,0,127,63), outline=1, fill=0)
        drawtop.text((5, top+20),"Launching Patch Loader",  font=font1, fill=255)
        disptop.display(image_top)
        time.sleep(1)
        exestring = "sudo killall -9 pd python ; sudo python /home/pi/terminal_tedium/tt-loader.py"
        print (exestring)
        os.system(exestring)        
#OLED labels: LD1 LD2 FdBk RD1 RD2 BPM
#012345678901    
    elif (TT[0:11] == 'OLED labels'):
        data = TT[12: ]
        data.rstrip("\n\r")
        data = data.split(' ')
        knobnames = [str(k) for k in data]
# bottom OLED display - with knob setting bar chart
#OLED E: 120 0 0 0.833333 1.16667 0.75 0.5 1.6 0 120
#01234567
    elif (TT[0:6] == 'OLED E'):
#        print TT[0:6]
        data = TT[8: ]
#        print data
        data = data.split(' ')
        plotdata = [float(k) for k in data]
        X=int(plotdata[0])
        if (X==0):
            drawbot.rectangle((0,0,width,height), outline=0, fill=0)        
        prev_L=L
        L=int(32-plotdata[1]*.0315)
        prev_R=R
        R=int(63-plotdata[2]*.0315)
        K1=plotdata[3]
        K2=plotdata[4]
        K3=plotdata[5]
        K4=plotdata[6]
        K5=plotdata[7]
        K6=plotdata[8]
        if (X%5 ==0):
            drawtop
            drawtop.rectangle((0,0,width,height), outline=brite, fill=brite)
            drawtop.rectangle((0,top+15,width,51), outline=0, fill=0)
            drawtop.text((x+2, top+17), str('{:01.2f}'.format(K1)),  font=font2, fill=brite)
            drawtop.text((x+2, top+2), knobnames[1],  font=font1, fill=0)            
            drawtop.text((50, top+17), str('{:01.2f}'.format(K2)),  font=font2, fill=brite)
            drawtop.text((50, top+2), knobnames[2],  font=font1, fill=0)            
            drawtop.text((98, top+17), str('{:01.2f}'.format(K3)),  font=font2, fill=brite)
            drawtop.text((98, top+2), knobnames[3],  font=font1, fill=0)            
            drawtop.text((x+2, top+37), str('{:01.2f}'.format(K4)),  font=font2, fill=brite)
            drawtop.text((x+2, top+54), knobnames[4],  font=font1, fill=0)            
            drawtop.text((50, top+37), str('{:01.2f}'.format(K5)),  font=font2, fill=brite)
            drawtop.text((50, top+54), knobnames[5],  font=font1, fill=0)            
            drawtop.text((98, top+37), str('{:01.1f}'.format(K6)),  font=font2, fill=brite)
            drawtop.text((98, top+54), knobnames[6],  font=font1, fill=0)            
#            drawtop.text((x, top+41), str('{:01.2f}'.format(BPM)),  font=font2, fill=brite)
#            disptop.image(image_top)
#----            disptop.display(image_top)        
        drawbot
#        draw.point((X,L), fill=brite)
        drawbot.line ((X-1,prev_R,X,R),fill = brite)
#        draw.line((i-1,plotdata[i-1],i,plotdata[i]), fill=brite)        
#        draw.point((X,R), fill=brite)        
        drawbot.line ((X-1,prev_L,X,L),fill = brite)
#        dispbot.image(image_bot)
        with regulator:
            if (X%5 ==0):
                disptop.display(image_top)
                dispbot.display(image_bot)
            else:
                dispbot.display(image_bot)        
 #       time.sleep(.025)
        #----dispbot.display(image_bot)

 #   elif (TT[0:6] == 'OLED Z'):
 #       draw.rectangle((0,0,width,height), outline=0, fill=0)
 #       data = TT[10: ]
 #       data = data.split(' ')
 #       plotdata = [int(k) for k in data]
 #       i = 1
 #       while (i < 127):
 #           if (i<99):
 #               draw.line((i-1,plotdata[i-1],i,plotdata[i]), fill=brite)
 #           elif (i == 110):
 #               VUL = 63-plotdata[i]
 #               draw.rectangle((101,63,105,VUL), outline=1, fill=brite)
 #           elif (i == 111):
 #               VUR = 63-plotdata[i]
  #              draw.rectangle((108,63,112,VUR), outline=1, fill=brite)
  #          i = i + 1
#        disptop.image(image)
 #       disptop.display(image)
