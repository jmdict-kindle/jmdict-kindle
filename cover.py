# !/usr/bin/env python3

#
# Copyright 2014 Jose Fonseca
# All Rights Reserved.
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
#


import cairo
 

w, h = 768, 1024

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
ctx = cairo.Context(surface)
 
# paint gray background
ctx.set_source_rgb(0.75, 0.75, 0.75)
ctx.rectangle(0, 0, w, h)
ctx.fill()
 
# draw centered text
def draw_text(ctx, x, y, t):
    x_bearing, y_bearing, width, height, x_advance, y_advance = ctx.text_extents(t)

    x -= 0.5*width
    y -= 0.5*height
        
    ctx.move_to(x, y)
    ctx.show_text(t)

# draw text
ctx.select_font_face('Sans')
ctx.set_source_rgb(0.00, 0.00, 0.00) # black

ctx.set_font_size(90*h/800)
draw_text(ctx, 0.5*w, 0.5*h, 'JMDICT')

ctx.set_font_size(30*h/800)
draw_text(ctx, 0.5*w, 0.75*h, 'Japanese-English Dictionary')
 
# finish
ctx.stroke()


surface.write_to_png('JMdict-cover.png')

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
ctx = cairo.Context(surface)
 
# paint gray background
ctx.set_source_rgb(0.75, 0.75, 0.75)
ctx.rectangle(0, 0, w, h)
ctx.fill()
 
# draw centered text
def draw_text(ctx, x, y, t):
    x_bearing, y_bearing, width, height, x_advance, y_advance = ctx.text_extents(t)

    x -= 0.5*width
    y -= 0.5*height
        
    ctx.move_to(x, y)
    ctx.show_text(t)

# draw text
ctx.select_font_face('Sans')
ctx.set_source_rgb(0.00, 0.00, 0.00) # black

ctx.set_font_size(90*h/800)
draw_text(ctx, 0.5*w, 0.5*h, 'JMNEDICT')

ctx.set_font_size(30*h/800)
draw_text(ctx, 0.5*w, 0.75*h, 'Japanese Names')
 
# finish
ctx.stroke()


surface.write_to_png('JMnedict-cover.png')

# Convert to grayscale JPEG
# XXX: Kindle does not show thumbnails for PNG covers
from PIL import Image
im = Image.open('JMdict-cover.png')
im = im.convert('L')
im.save('JMdict-cover.jpg')

im = Image.open('JMnedict-cover.png')
im = im.convert('L')
im.save('JMnedict-cover.jpg')
