#!/usr/bin/env python2
# coding=utf-8
 
"""
draw shapes and fill shap with transparent color and overlap them.
"""
 
from PIL import Image, ImageDraw
from random import randint as _r

rpoint = _r(0,800)
rcolor = _r(0,255) 
 
def main():
    im = Image.new("RGBA", (800, 800), color=(255,255,255))
    draw = ImageDraw.Draw(im)
    #final = im

    for i in range(0,1000):
        draw.line((rpoint,rpoint,rpoint,rpoint), fill=(rcolor,rcolor,rcolor))
    
'''
    draw.line((rpint, 0, 200, 200), fill=(255, 0, 0))
    #_draw.rectangle((0, 0, 200, 200), fill=(255, 255, 255, 128))
    #final = Image.alpha_composite(im, final)
    draw.line((100, 100, 300, 300), fill=(0, 255, 0))
    #_draw.rectangle((100, 100, 300, 300), fill=(255, 255, 255, 128))
    final = Image.alpha_composite(im, final)


    draw.line((200, 200, 400, 400), fill=(0, 0, 255))
    #_draw.rectangle((200, 200, 400, 400), fill=(255, 255, 255, 128))
    #final = Image.alpha_composite(im, final)
    draw.line((300, 300, 500, 500), fill=(200, 100, 50))
    #_draw.rectangle((300, 300, 500, 500), fill=(255, 255, 255, 128))
    #final = Image.alpha_composite(im, final)

'''
    im.save('/im2.png')

 
if __name__ == '__main__':
    main()