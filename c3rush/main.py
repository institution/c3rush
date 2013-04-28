# coding: utf-8
#
#	SEApo Python Remake
#	version: 0.3
#	license: GPLv3 or later 
#	written by: sta256@gmail.com
#	
#	This is python cover of flash game "Super Energy Apocalipse".
#
#

#import psyco
#psyco.full()

'''
import property
from game import *
from vector2 import Vector as vec
from view import View
import pygame
import sys
from engine import flip, Image
from gui import *

game = Env()

view = View(game)

clock = pygame.time.Clock()
 
while True: 
	
	dt = float(clock.tick(60))/1000.0
	
	view.update(dt)
	
	view.render()
	flip()
		
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit(0) 
		else:  
			view.read_event(event)
'''

from engine import G, Vector as vec, Color3 as c, Image as Img
	
import pygame, sys

from view import Interface

def test():

	from game import Env
	from view import GameBox

	env = Env()
		
	window_size = (900,600)
	
	g = G(window_size)
		
	interface = Interface(game=env, g = g, window_size = window_size)
		
	g.loop(interface.mainloop)
	
	
def onclick_prop(frame, pos, button):
	for b in frame.boxes:
		if in_rect(pos, b.pos, b.dim):
			onclick_prop(b, pos, button)
			if hasattr(b, 'onclick'):
				b.onclick(vec(pos) - vec(b.pos), button)
			

def in_rect(xy, rpos, rdim):
	return rpos[0] <= xy[0] <= rpos[0] + rdim[0] and rpos[1] <= xy[1] <= rpos[1] + rdim[1]



if __name__ == '__main__':
	test()
	
	
	