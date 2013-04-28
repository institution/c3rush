#!/usr/bin/python
# coding: utf-8

# foundation
import pygame
from pygame import * 

# svg
import cairo
import rsvg

# math 
import array
import math
from vector2 import Vector2 as vec
from vector2 import Vector2 as v

# utils
import time
import sys, os
#from base import *

from log import log
import itertools


def glc(r,g,b):
    return (r*255.0, g*255.0, b*255.0)

def pygame_color(t):
    return (t[0]*255.0, t[1]*255.0, t[2]*255.0)



# -----------------------------------------------------------------------------------
from lxml import etree

def xml_set(xml_str, *path_value):
    xml = etree.fromstring(xml_str)
    #print xml
    for path, value in path_value:
        #print path, value
        tag_path, attrib_name = path.split('/@')
        #print xml.xpath(tag_path)
        x = xml.xpath(tag_path)[0]        
        x.attrib[attrib_name] = str(value) + ' ' + x.attrib[attrib_name]
        
    return etree.tostring(xml, pretty_print=True)



class Mirage(object):
    def __init__(self, file, **kwargs):
        """
        args = {name = (path, pattern)}
        """
        assert os.path.splitext(file)[1] == '.svg'
        
        # wczytaj svg
        f = open(file)
        self.data = f.read()
        f.close()
        
        self.kw = {}        
        # zapamietaj specyfikacje parametrow
        for name,(path,pattern) in kwargs.items():
            self.kw[name] = (path,pattern)
    
    def render(self, **kwargs):
        """ Zwraca zparametryzowany obrazek 
        """
        ps = []
        for name,value in kwargs.items():
            path,pattern = self.kw[name]
            ps.append((path, pattern % value))
        return Image(svg = xml_set(self.data, *ps))
            
        
        
    






from color3 import Color3 as c
from color3 import Color3
        

from vector2 import Vector2 as Vector





class Font(pygame.font.Font):
    def __init__(self, file, size):
        
        super(Font,self).__init__(file, size)
        # !
        #font = pygame.font.get_default_font()
        
        #if font != None:
        #    fp = pygame.font.match_font(font)
        #    super(Font,self).__init__(fp, size)
        #else:
        
        
    def split_text(self, text, width):
        """ Dzieli text na linie uwzgledniajac entery.
        """        
        ts = text.split('\n')
        rs = []
        for t in ts:
            #print t
            #print self._split_text(t, width)
            rs.extend(self._split_text(t, width))
        return rs    
        
    def _split_text(self, text, width):
        """ Dzieli text na linie nie uwzgledniajac enterow.
        """
        ts = []
        rest = text
        while 1:            
            #rest = rest.strip(' ')
            line, rest = self.separate_line(rest, width)
            ts.append(line)
            if not rest:
                break            
        return ts
        
    def separate_line(self, text, width):
        i = 0
        j = len(text)
        d = 0
        while i + 1 < j:
                        
            d = (i + j) / 2
            
            #print i,j,d

            if self.size(text[:d])[0] <= width:
                i = d
            else:
                j = d         
            
        if self.size(text[:j])[0] <= width:
            return text[:j], text[j:]
        else:
            return text[:i], text[i:]
            
        

    def render(self, text, color=(0.8,0.8,0.8), width=None, antialias=True, background=None):
        
        if width == None:
            return Image(surface = super(Font, self).render(text, antialias, pygame_color(color)))
        
        #return Image(surface = super(Font, self).render(text, antialias, color))
        
        ts = self.split_text(text, width)
                
        linesize = self.get_linesize()
        #em = self.get_height()
        
        s = Image(dim = (width, linesize * len(ts)))
        
        y = 0
        for line in ts:
            txt = Image(surface = super(Font, self).render(line, antialias, pygame_color(color)))
            s.blit(txt, (0,y))            
            y += linesize
        
        return s
        
        
        
class FormattedText(object):
    # formatted text
    
    def __init__(self, text, font):
        # docelowo pango text
        self.cache = font.render(text)
        self._text = text
        
    def render(self):
        return self.cache
        
        
        

"""
def from_text(img, text, color, dim):
    img.surface = FONT.render(text, True, color)
    return img
"""



    


class G(object):
    
    def draw_rect(self, pos, dim, col=None, wid=0, color=(1,1,1)):
        # pos, dim, color, width=0
        pygame.draw.rect(self.surface, pygame_color(col or color), Rect(pos[0], pos[1], dim[0], dim[1]), wid)
    
    
    def Font(self, *args, **kwargs):
        return Font(*args, **kwargs)
    
    def __init__(self, *args, **kwargs):
        self.init(*args, **kwargs)
    
    def set_clip(self, mode):
        self.surface.set_clip(mode)
        
    
    def init(self, mode):
        """ Init pygame system.
        opts:
            font -- str
            mode -- pair, vec
            fullscreen -- bool
        """
        
        pygame.init()
        pygame.font.init()
        
        #pygame.mixer.init()
        #Sound = pygame.mixer.Sound
        
        #print pygame.display.list_modes()
            
        #flags = pygame.FULLSCREEN
        flags = pygame.RESIZABLE | pygame.HWSURFACE
        self.flags = flags
        
        pygame.display.set_mode(mode, flags) 
                
        self.surface = pygame.display.get_surface()
        
        self._dt = 0.0

        #font = pygame.font.Font('font/Share-Regular.ttf', 16)
        #FONT = pygame.font.Font(pygame.font.match_font('Liberation Serif'), 36)
        
        #class Font(object):
        #    def __init__(self, name):
        #        self.font = pygame.font.match_font(name)
        
        #Image(surface = engine.screen), engine.window )
        
    def refresh(self, mode):
        #self.surface = pygame.display.get_surface()
        pygame.display.set_mode(mode, self.flags) 
        
    @property
    def dt(self):
        return self._dt
    
    def flip(self):
        pygame.display.flip()
    
    def loop(self, callback):
        """ 
        """
            
        clock = pygame.time.Clock()
         
        while True: 
            
            self._dt = float(clock.tick(60))/1000.0
            
            callback(self)
                        
            pygame.display.flip()
                            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit(0)
                
        
    def event(self):
        return pygame.event
        
    def pause(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return 
         
    def fill(self, c):
        self.surface.fill(pygame_color(c))
    
    
    def Image(self, *args, **kwargs):
        return Image(*args, **kwargs)

    def blit(self, img, pos=(0,0)):
        assert isinstance(img, Image)
        self.surface.blit(img.surface, tuple(pos)) 
        
        


        
Engine2 = G

G.WHITE = Color3(1,1,1)
G.GRAY = Color3(1,1,1)
G.BLACK = Color3(0,0,0)

G.GREEN = Color3(0,1,0)
G.BLUE = Color3(0,0,1)
G.RED = Color3(1,0,0)

G.YELLOW = Color3(1,1,0)
G.MAGNETA = Color3(1,0,1)
G.TEAL = Color3(0,1,1)



                
        
    
        

# sedzia render
"""
def blit(img, pos=(0,0), to=None):
    
    if to == None:
        to = engine.screen
        
    if type(img) == Image:
        to.blit(img.surface, tuple(pos)) 
        
    else:
        NotImplemented
"""



#def render_rect(pos, dim, color, width):
#    pygame.draw.rect(engine.screen, color, Rect(pos[0], pos[1], dim[0], dim[1]), width)
    
#def line(x, y, color, width=1):
#    pygame.draw.line(engine.screen, color, (x.x, x.y), (y.x, y.y), width)
    
    







"""
cache_image dekorator
img_storage
geti = getimage
memory_image
"""



# -------------------------------------
class Image(object):
    
    # -------------------------------------
    def __init__(img, fill=None, surface=None, file=None, svg=None, dim=None):
        scale = 1.0
        
        if svg:
            # load from xml string
            img.load_svg_data(svg)
        
        elif file:
            img.load_file(file, dim = dim)
            
        elif surface:
            img.surface = surface
            
        elif dim:
            img.surface = pygame.Surface(tuple(dim))
            if fill:
                img.surface.fill(pygame_color(*fill))
            
        
    def load_file(self, file, dim = None):
        scale = 1.0
        ext = os.path.splitext(file)[1]
            
        if ext == '.svg':
            self.load_svg_file(file, scale, dim)
        else:
            self.load_other_file(file, scale, dim)
    
    
    def scaled(self, dim=None, scale=None):        
        if scale != None:
            dim = vec(self.dim) * scale
                    
        return Image(surface=pygame.transform.scale(self.surface, map(int, dim)))
        
    def flipped_h(img):
        NotImplemented
        
    def flipped_v(img):
        NotImplemented
        
    def fill(self, color):
        self.surface.fill(pygame_color(color))
        
    def load_other_file(img, file, scale=1.0, dim=None):
        img.surface = pygame.image.load(file)

    def converted(self, ppa=False, *args, **kwargs):
        """
        ppa -- use per pixel alpha
        """
        if ppa:
            new_surface = self.surface.convert_alpha(*args, **kwargs)
            
        else:            
            new_surface = self.surface.convert(*args, **kwargs)
            
        return Image(surface = new_surface)
    
    @property
    def alpha(self):
        return self.surface.get_alpha()
        
    @alpha.setter
    def alpha(self, value):
        self.surface.set_alpha(value)
    

    def load_rsvg_obj(img, rsvg_obj, scale=1.0, dim=None):
        svg = rsvg_obj
        w, h = svg.get_dimension_data() [0:2]
        
        if dim == None: 
            dim = vec(w,h)
        else:
            dim = int(dim[0]), int(dim[1])
            scale = float(dim[0]) / float(w)
            
        csurf = cairo.ImageSurface(cairo.FORMAT_ARGB32, dim[0], dim[1])
        cr = cairo.Context(csurf)
        
        #cairo.Matrix.rotate( matrix, prop.rot )
        mx = cairo.Matrix(scale, 0, 0, scale, 0, 0)
        cr.transform(mx)
        
        svg.render_cairo(cr)
        
        data = str(csurf.get_data())
        
        ds = []
        i = 0
        while i < len(data):
            (B,G,R,A) = (data[i], data[i+1], data[i+2], data[i+3])
            ds.extend([R,G,B,A])
            i += 4
        
        # cairo surface -> pygamesurface
        img.surface = pygame.image.fromstring(''.join(ds), (dim[0], dim[1]), "RGBA")
        return img
    
    def load_svg_data(self, svg_data, scale=1.0, dim=None):
        return self.load_rsvg_obj(rsvg.Handle(data = svg_data), scale, dim)
    
    
    def load_svg_file(self, file, scale=1.0, dim=None):
        #f = open(file)
        #svg_data = f.read()
        #f.close()
        #return self.load_rsvg_obj(rsvg.Handle(data = svg_data), scale, dim)
        return self.load_rsvg_obj(rsvg.Handle(file=file), scale, dim)
        
    @property
    def dim(img):
        return vec(*img.surface.get_size())
        
    def blit(self, img, pos=(0,0)):
        self.surface.blit(img.surface, tuple(pos)) 
    
    def rblit(self, to, pos=(0,0), dim=None, from_pos=None):
        
        # TODO: auto dim
        area = None
        if dim != None and from_pos != None:
            area = (from_pos[0], from_pos[1], dim[0], dim[1])
        
        to.surface.blit(self.surface, tuple(pos), area = area) 
        
        
    def render(self):
        return self
        
    def copy(self):
        return Image(surface = self.surface.copy())

    def alpha_effect(self, alpha = 0.5):
        """	Efekt rownowazny ustawieniu alpha i color_key ale nie 
        wymaga aby obrazek mial specjalnie przygotowany color_key.
        Uzywa per pixel alpha. Zwraca nowy obrazek.
        BUG: Zmiana alpha na zero powoduje uznanie czarnego za przezroczysty przy nastepnej zmianie. Colorkey + alpha bylby lepszy.
        """
        dim = self.surface.get_size()
        self.surface.lock()
        for p in itertools.product(range(dim[0]), range(dim[1])):
            color = self.surface.get_at(p)
            if color != (0,0,0,0):
                new_color = (color[0], color[1], color[2], int(alpha*255))
                self.surface.set_at(p, new_color)
                
        self.surface.unlock()
        return self
        


    


txt = """LaLaLa

Move the image by dx pixels right and dy pixels down. dx and dy may be negative for left and up scrolls respectively. Areas of the surface that are not overwritten retain their original pixel values. Scrolling is contained by the Surface clip area. It is safe to have dx and dy values that exceed the surface size. 
"""
import random

def test():
    print 'test'
    
    
    g = G((800,600))
    f = Font('../font/Share-Regular.ttf', 16)
    kwad = Mirage('test.svg', 
        rot = ("*/*[@id='bbb']/@transform", 'rotate(%i 30 30)'),
    )
    
    ww = Mirage('test2.svg', 
        rot = ("*/*[@id='ww']/@transform", 'rotate(%i 34 27)'),
    )
    
    txt_img = f.render(txt, width = 400)
    
    
    g.t = 0.0
    g.lt = 0.0
    g.wind = 100.0
    g.rot = 0.0
    
    static_kwad = Image(file='test_t.svg', dim=(128,128))
    static_kwad.alpha_effect(0.5)
    
    
    def render(g):    
        #print g.dt   
        if int(g.t) > int(g.lt):
            g.lt = g.t
            g.wind += random.randint(0,100) - 50
            print g.wind
        
        g.rot = g.rot + g.dt * g.wind
        
        g.fill((0,0,0))
        g.blit(txt_img)
        g.blit(ww.render(rot = int(g.rot)), (400,0))
        
        g.draw_rect(dim=(300,200), pos=(50,200), color=(0.5,1.0,0.5))
        
        # tylko testowo - to ma niska wydajnosc
        a = (g.t/10) % 1
        static_kwad.alpha_effect(a if a >= 0.1 else 0.1)
        
        static_kwad.rblit(g, (60,210))
                
        g.flip()        
        g.t += g.dt
    
    
    g.loop(render)
    
    
    



'''
def xml_set(xml_str, path_value):
	xml = etree.fromstring(xml_str)
	for path, value in path_value:
		tag_path, attrib_name = path.split('/@')
		xml.xpath(tag_path).attrib[attrib_name] = str(value)
	return root.tostring()

'''

from StringIO import StringIO
    

if __name__ == '__main__':
    
    #f = open('test.svg')
    #tree = etree.parse(f)
    #tree = etree.parse(StringIO('<svg><g><rect/><rect id="aaa"/></g></svg>'))

    #print etree.tostring(tree, pretty_print=True)

    #rs = tree.xpath("*/*[@id='bbb']")
    #print [r.tag for r in rs]
    
    test()
    

    
    
    
    
    
    


#Create Cairo Surface
#Width, Height = 512, 512
#data = array.array('c', chr(0) * Width * Height * 4)
#stride = Width * 4
#surface = cairo.ImageSurface.create_for_data (data, cairo.FORMAT_ARGB32,Width, Height, stride)

        



#~ def draw(surface):
    #~ x,y, radius = (250,250, 200)
    #~ ctx = cairo.Context(surface)
    #~ ctx.set_line_width(15)
    #~ ctx.arc(x, y, radius, 0, 2.0 * math.pi)
    #~ ctx.set_source_rgb(0.8, 0.8, 0.8)
    #~ ctx.fill_preserve()
    #~ ctx.set_source_rgb(1, 1, 1)
    #~ ctx.stroke()
    

#Create Cairo Surface
#~ Width, Height = 512, 512
#~ data = array.array('c', chr(0) * Width * Height * 4)
#~ stride = Width * 4
#~ surface = cairo.ImageSurface.create_for_data (data, cairo.FORMAT_ARGB32,Width, Height, stride)

#init PyGame

#Draw with Cairo
#draw(surface)

#i = Image('mine.svg')
#f = Image('farm.svg')

#Tranfer to Screen

#screen.blit(i.surface, (0,0)) 
#screen.blit(f.surface, (128,128)) 
#screen.blit(Image().Text('aaa', (200,10,10)).surface, (200,50)) 



'''
# -------------------------------------
def main_loop(
        update=lambda dt: None, 
        render=lambda: None, 
        listen=lambda ev: None):
    """ Non-blocking main loop. 
    How about event driven loop?
    """
        
    clock = pygame.time.Clock()
     
    while True: 
        
        dt = float(clock.tick(60))/1000.0
        
        update(dt)
        render()
        
        pygame.display.flip()
        # screen.fill((20,20,20))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit(0)                
            else: 
                listen(event)

'''