#!/usr/bin/env python
import time, sys, os, glob, subprocess 
from luma.core.sprite_system import framerate_regulator
from time import sleep
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
brite=50
#----------------------------LUMA SETUP-----------------------------------------
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106

botserial = i2c(port=1, address=0x3D)
# substitute ssd1331(...) or sh1106(...) below if using that device
disp = sh1106(botserial)
topserial = i2c(port=1, address=0x3C)
disptop = sh1106(topserial)
#----------------------------------------------

# Raspberry Pi pin configuration:
RST = None 
line1 = str()
#------------------------------- PI INPUTS ---------------------------------
# pull up GPIO23-25 (tact switches)
up = 0
down = 0
select = 0
a = 1
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#-----------------------------------------------------------------------
def filedisp(filename, filepath, filenum, listsize):
    global files
 #   disp.clear()
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    padding = -2
    top = padding
    bottom = height-padding
    x = 0
    font = ImageFont.load_default()
    font1 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Bold.ttf",12)    
    font2 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Light.ttf",13)
    font3 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Bold.ttf",45)
    font4 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Light.ttf",10)
    font5 = ImageFont.truetype("/home/pi/terminal_tedium/tt-fonts/Roboto-Regular.ttf",14)
    draw.rectangle((0,0,127,35), outline=brite, fill=brite)
    draw.rectangle((1,top+3,117,34), outline=0, fill=brite)
    draw.rectangle((126,top+3,119,34), outline=0, fill=0)
    sliderwidth = 34 // listsize
    sliderbottom = (listsize-filenum) * sliderwidth + 1
    slidertop = (listsize-filenum-1) * (sliderwidth) + 1    
    draw.rectangle((126,slidertop,119,sliderbottom), outline=0, fill=brite)
#    draw.rectangle((126,top+12,119,18), outline=0, fill=brite)   
#    draw.rectangle((126,top+30,119,34), outline=0, fill=brite)
    draw.text((12, top+12), filepath , font=font5, fill=0)
#    draw.text((5, top+10), filename , font=font2, fill=0)  
    draw.text((14, top+45), "Buttons 1 & 2 to scroll", font=font4, fill=brite) 
    draw.text((14, top+55), "LED button to load", font=font4, fill=brite)        
#    disp.image(image)
    with regulator:
        disp.display(image)

#-------------------------------------------------------------------
regulator = framerate_regulator(fps=20)  # Unlimited
path = '/home/pi/terminal_tedium/patches/' #tt dir
pathlength = len(path)
searchpath = path+'**/TT-*.pd'
files = glob.glob(searchpath)
listsize = len(files)
x=0            
done = 0 
print("START",x, files[x]) 
# display first file name
filenm = files[x][files[x].find('TT-'):99]
filepath = files[x][0:files[x].find('TT-')]
subpath = files[x][pathlength:files[x].find('TT-')]            
#---------- put TT title on top display ------------------------
disptop.clear()
width = disptop.width
height = disptop.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()
font1 = ImageFont.truetype("/home/pi/Roboto-Light.ttf",11)
font2 = ImageFont.truetype("/home/pi/Roboto-Bold.ttf",14)
font3 = ImageFont.truetype("/home/pi/Roboto-Bold.ttf",48)
draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.rectangle((0,63,127,0), outline=brite, fill=0)
draw.text((34, 4), "TT", font=font3, fill=brite) 
draw.text((25, 2), "terminal tedium", font=font1, fill=brite)
draw.text((39, 50), "mxmxmx", font=font1, fill=brite)    
disptop.display(image)
filedisp(subpath,filenm,x,listsize)    
    
while not done==1:
    sleep (.04)
    up = not GPIO.input(23) # these things are inverted, so I inverted them again
    down = not GPIO.input(25)
    select = not GPIO.input(24)
    if up == 1 or down == 1 or select == 1:
        if up == 1:
            x += 1
            x = x % (listsize)            
            print ("+ ",x,files[x])
            sleep(.2)
            up = 0
            filenm = files[x][files[x].find('TT-'):99]
            filepath = files[x][0:files[x].find('TT-')]
            subpath = files[x][pathlength:files[x].find('TT-')]            
            filedisp(subpath,filenm,x,listsize)
        elif down == 1:
            x -= 1
#            x = abs(x)
            x = x % (listsize)            
            print ("- ",x,files[x])
            sleep(.2)
            down = 0
            filenm = files[x][files[x].find('TT-'):99]
            filepath = files[x][0:files[x].find('TT-')]
            subpath = files[x][pathlength:files[x].find('TT-')]            
            filedisp(subpath,filenm,x,listsize)
        elif select == 1:    
            print("selected",x, files[x])
            sleep(.2)
            select = 0
            filenm = files[x][files[x].find('TT-'):99]
            filepath = files[x][0:files[x].find('TT-')]
            subpath = files[x][pathlength:files[x].find('TT-')]
            filedisp(subpath,filenm,x,listsize)
            oledfilepath = filepath+'tt-OLED.py'
#            exestring = '/home/pi/pd-0.46-7/bin/pd ' + '-nogui '+ '-rt '+ files[x]+ ' 2>&1 '+ '| python '+ oledfilepath
            exestring = '/home/pi/pd-0.46-7/bin/pd -nogui -rt -midiindev 2 '+ files[x]+ ' 2>&1 | python '+ oledfilepath
            print exestring
            os.system(exestring) 
            break
#        print filepath, filenm
#sudo rm list2.txt && echo 'rec.wav' >> list2.txt && ls >> list2.txt

#create a list of .wav files that are located in subdirectory /loops/
#exestring = "sudo rm /loops/list2.txt && echo 'rec.wav' >> /loops/list2.txt && ls /loops/ >> list2.txt"
#os.system(exestring)
#


