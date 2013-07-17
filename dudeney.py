#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import division

import math
import cairo

OUTPUT_WIDTH = 400
OUTPUT_HEIGHT = 300

VIEWPORT_X = -0.6
VIEWPORT_Y = -0.55
VIEWPORT_WIDTH = 2
VIEWPORT_HEIGHT = (OUTPUT_HEIGHT/OUTPUT_WIDTH) * VIEWPORT_WIDTH

FRAMES = 48

FILL = cairo.SolidPattern(0x44/0xFF, 0x85/0xFF, 0xB6/0xFF)
STROKE = cairo.SolidPattern(1, 1, 1)

root_3 = math.sqrt(3)
p = (3 - math.sqrt(4*root_3 - 3))/4
np = 3/4 - p
i = ( (1/4 - p) * np + 3/16 ) / ( np*np + 3/16 )
e = ( p + i*np, i * root_3/4 )
j = ( (1/2) * np ) / ( np*np + 3/16 )
c = ( p + j*np, j * root_3/4 )

def polygon(*points, **kwargs):
    cx.save()
    cx.new_path()
    cx.translate(points[0][0], points[0][1])
    if "rotate" in kwargs:
        cx.rotate(kwargs["rotate"]*math.pi/180)
    cx.move_to(0, 0)
    for point in points[1:]:
        cx.line_to(point[0]-points[0][0], point[1]-points[0][1])
    cx.close_path()
    cx.set_source(FILL)
    cx.fill_preserve()
    cx.set_source(STROKE)
    cx.stroke()
    
    if "callback" in kwargs:
        cx.translate(-points[0][0], -points[0][1])
        kwargs["callback"]()
    cx.restore()

def draw_frame(t):
    cx.save()
    cx.translate(
        -0.1 + 0.12*t,
        -0.15 + -0.25*t + 0.3*math.sin((7*t/4 - 3*t*t/4)*math.pi)**2
    )
    
    cx.translate(+0.5, +0.5)
    cx.rotate(49*t*math.pi/180)
    cx.translate(-0.5, -0.5)
    
    polygon((1/2, root_3/2), (3/4, root_3/4), e, (1/4, root_3/4))
    polygon((1/4, root_3/4), e, (p, 0), (0, 0), rotate=-180*t,
        callback=lambda: polygon((p, 0), c, (p+1/2, 0), rotate=-180*t))
    polygon((3/4, root_3/4), (1, 0), (p+1/2, 0), c, rotate=180*t)
    cx.restore()

def easing(t):
    s = math.sin(math.pi*t/2)
    return s*s

for i in range(FRAMES):
    surface = cairo.ImageSurface(
        cairo.FORMAT_ARGB32,
        OUTPUT_WIDTH,
        OUTPUT_HEIGHT,
    )
    cx = cairo.Context(surface)
    
    cx.set_source_rgb(1,1,1)
    cx.rectangle(0, 0, OUTPUT_WIDTH, OUTPUT_HEIGHT)
    cx.fill()
    
    cx.scale(OUTPUT_WIDTH / VIEWPORT_WIDTH, OUTPUT_HEIGHT / VIEWPORT_HEIGHT)
    cx.translate(-VIEWPORT_X, -VIEWPORT_Y)
    cx.set_line_width(0.01)
    
    draw_frame(easing(i / (FRAMES - 1)))
    
    surface.write_to_png("out%02d.png" % (i+1))
    surface.finish()
