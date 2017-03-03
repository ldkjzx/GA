#!/usr/bin/env python2
# coding=utf-8
 
"""
draw shapes and fill shap with transparent color and overlap them.
"""
 
from PIL import Image, ImageDraw
from random import randint as _r

rpoint = _r(0,400)
rcolor = _r(0,255) 
 
def main():
    im = Image.new("RGBA", (400, 400), color=(255,255,255))
    draw = ImageDraw.Draw(im)
    #final = im

    for i in range(500):
        #draw.line((_r(0,400),_r(0,400),_r(0,400),_r(0,400)), fill=(_r(0,255),_r(0,255),_r(0,255)))
        draw.polygon([(_r(0,400),_r(0,400)),(_r(0,400),_r(0,400)),(_r(0,400),_r(0,400))], fill=(_r(0,255),_r(0,255),_r(0,255)))
      
    
    
    im.save('/im2.png')

 
if __name__ == '__main__':
    main()