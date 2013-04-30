# coding: utf-8
"""
	Mapuje strukture obiektow na obraz.
"""
from vec import vec
from engine import Image, G
from box import CBox, VBox, PBox, PBox, Box, TextBox, GridBox
from box.geometry import EventSource, Event
import weakref

from pygame import *
from params import *
from game import *
import random

import pygame

GameBox=Env


"""
grass!
change building entry point
fps
game - check terrain on build
some kind of intro?


layer rendering:
	terrain layer
	track layer
	buildings layer
	vehicles layer
	weather/day-night/smog layer
	render mouse layer

"""

import os.path as path

# data path
DATA = './data/'

def cached(func):
	cache = {}
	
	def inner(**kwargs):
		key = '&'.join(k+'='+str(v) for (k,v) in kwargs.items())
		
	return inner

def make_key(kwargs):
	return '&'.join(k+'='+str(v) for (k,v) in kwargs.items())


class Mirage(object):
	def __init__(self, **defaults):
		self.defaults = defaults
		self.cache = {}
		
	def render(self, **kwargs):
		kw = {}
		kw.update(self.defaults)
		kw.update(kwargs)
		
		key = make_key(kw)
		if key not in self.cache:
			#print key, '-> cache'
			self.cache[key] = loadimg(**kw)
		
		return self.cache[key]
		
		
def loadimg(file, dim, scale = 1.0):
	"""
	dir -- (-1) left, (+1) right
	"""
	return Image(file = path.join(DATA, file), dim = dim * scale)


import pygame, sys
et = pygame

class Controller(EventSource):
	def dispath(self):
		# listen
		for event in pygame.event.get():
			#print event
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit(0)
							
			else:
				self.fire(event)


class Order(object):
	arg_types = {
		'move': ['obj', 'point'],
		'build': ['obj', 'type', 'point'],
		'stop': ['obj'],
	}
	
	def __init__(self):
		self.action = None
		self.args = []
				
	def reset(self):
		self.action = None
		self.args = []
		
	def append_arg(self, arg):
		self.args.append(arg)
		
	def is_ready(self):
		if self.action:
			return len(self.args) == len(self.arg_types[self.action])
		return False
			
	def get_next_param_type(self):
		if self.action:
			
			#print i, self.arg_types[self.action], self.action, self.args
			i = len(self.args)
			if i < len(self.arg_types[self.action]):
				return self.arg_types[self.action][i]
			else:
				return None
		else:
			return 'action'
		


class Interface(PBox):
	
	
	def build(self, object, pos, button):
		#print 'build:', object
		
		self.cursor = self.image_tab[object]
		self.mode = 'build'
		self.build_obj = object	

	def handle_video_resize(self, event):
		self.dim = (event.w, event.h)
		self.refresh()
		self.g.refresh((event.w, event.h))
		self.gamebox.mul_zoom(1.0)
	
	def get_mode(self):
		return self.order.get_next_param_type()
	
	def on_select_pos(self, event):
		assert self.get_mode() == 'point'
		self.order.args.append(event.pos)
	
	def __init__(self, game, g, window_size):
		self.g = g
		self.scale = 1.0
	
		self.order = Order()
	
		self.ctrl = Controller()
		
		
		SMALL = vec(24,24)
		MEDIUM = vec(48,48)
	
		self.render_tab = {	
			Energy: Mirage(file='symbol/energy.svg', dim=SMALL),
			Metal: Mirage(file='symbol/metal.svg', dim=SMALL),
			Coal: Mirage(file='symbol/coal.svg', dim=SMALL),
			Food: Mirage(file='symbol/food.svg', dim=SMALL),
			Waste: Mirage(file='symbol/waste.svg', dim=SMALL),
			'.': Mirage(file='land/mud.svg', dim=SMALL),
			'c': Mirage(file='land/coal.svg', dim=SMALL),
			'm': Mirage(file='land/iron.svg', dim=SMALL),
			'g': Mirage(file='land/grass.svg', dim=SMALL),
			'move': Mirage(file='symbol/move.svg', dim=SMALL),
			'stop': Mirage(file='symbol/stop.svg', dim=SMALL),
			Truck: Mirage(file='vehicle/truck.svg',dim=SMALL),
			Manip: Mirage(file='vehicle/manip.svg',dim=SMALL),
			CoalMine: Mirage(file='struct/coalmine.svg', dim=MEDIUM),
			MetalMine: Mirage(file='struct/metalmine.svg', dim=MEDIUM),
			Generator: Mirage(file='struct/generator.svg', dim=MEDIUM),
			Solar: Mirage(file='struct/solar.svg', dim=SMALL),
			MGPost: Mirage(file='struct/mg.svg', dim=SMALL),
			ControlPost: Mirage(file='struct/fort.svg', dim=MEDIUM),
			Factory: Mirage(file='struct/factory.svg', dim=MEDIUM),
			Mutant:	Mirage(file='struct/mutant.svg', dim=MEDIUM),
			Recycler: Mirage(file='struct/recycler.svg', dim=MEDIUM),
			GreenHouse:	Mirage(file='struct/greenhouse.svg', dim=MEDIUM),
		}
		
		def render(type, **kwargs):
			if type in self.render_tab:
				return self.render_tab[type].render(**kwargs)
			else:
				return None
		
		self.cursor = None
		self.mode = None

		self.game = game
	
		super(Interface, self).__init__(
			dim = window_size, 
			pos = (0,0)
		)
		
		self.on(self.ctrl, et.VIDEORESIZE, self.handle_video_resize)
		
		
		# -- place toplevel panels
		left = PBox(
			pos = lambda s: s.p.pos, 
			dim = lambda s: (180, s.p.dim[1]), 
			border = 1,			
		)
		
		top = PBox(
			pos = lambda s: (left.end[0], left.pos[1]), 
			dim = lambda s: (
				s.p.dim[0] - left.dim[0], 
				80, #max(s.max_child_dim(1), 80)
			), 
			border = 1
		)
		
		gamebox = GameBox(
			pos = lambda s: (left.end[0], top.end[1]), 
			dim = lambda s: (
				s.p.dim[0] - left.dim[0], 
				s.p.dim[1] - top.dim[1]
			),
			game = self.game, 
			env = self,
			border = 1,
			p = self,
			ctrl = self.ctrl,
		)
		
		self.add(left, top, gamebox)
		assert gamebox.p == self
		
		self.on(gamebox, 'select', self.on_unit_selected)
		self.on(gamebox, 'select_pos', self.on_select_pos)
		
		self.gamebox = gamebox
		


		font = g.Font('font/160MKA.TTF', 16)
		
		'''
		cmdbox = VBox(
			childs = [
				CBox(
					content = font.render(lab), 
					on = {'click': partial(self.build, obj)}, 
					border = 1,
					dim = lambda s: s.content.dim,
				) for obj,lab in buildings
			], 
			border = 1, 
			pos = lambda s: frame.pos,
			dim = lambda s: (max(s.child_dim_(0)), sum(s.child_dim_(1)))
		)
		'''
		
		infobox = Infobox(
			p = left,
			font = font,
			pos = (0, 200), 
			dim = lambda s: (s.p.dim[0], 600),
			render = render,
			ctrl = self.ctrl,
			order = self.order,
		)
		
		self.infobox = infobox
				
		#CBox(
		#	pos = (0, 200), 
		#	dim = lambda s: s.content.dim, 
		#	content = font.render('Aosnefbewfgasefgaserg\nafawer\ndtg', width=150)
		#)
		
		left.add(infobox)
		
		self.on(self.ctrl, et.MOUSEBUTTONDOWN, self.wheel_zoom)
		
		
		self._wheel_scrool = 0
		
		self.on(self.ctrl, et.MOUSEBUTTONDOWN, self.start_wheel_scrool)
		self.on(self.ctrl, et.MOUSEBUTTONUP, self.stop_wheel_scrool)

		self.refresh()		
		
		self.gamebox.set_zoom(1.0)
		
		#~ print '------------------------------'
		#~ print frame.dim[0] - left.dim[0], 
		#~ print frame.dim[1] - top.dim[1]
		#~ print gamebox.dim
		
	
	def on_unit_selected(self, ev):
		#if ev.sel is None:
		#	pass
		#else:
		
		self.infobox.select(ev.sel)
	
	
	
	def wheel_zoom(self, event):
		if event.button == 4:
			self.gamebox.mul_zoom(1.1)
			
		elif event.button == 5:
			self.gamebox.mul_zoom(0.9)
	
	def start_wheel_scrool(self, event):
		if event.button == 2:
			self._wheel_scrool = 1
			self._wheel_scrool_mpos = vec(pygame.mouse.get_pos())
		
	def stop_wheel_scrool(self, event):
		if event.button == 2:
			self._wheel_scrool = 0
			self._wheel_scrool_mpos = None
		
		
	def make_wheel_scrool(self):
		if self._wheel_scrool:
			cpos = vec(pygame.mouse.get_pos())
			delta = self._wheel_scrool_mpos - cpos
			self._wheel_scrool_mpos = cpos
			
			self.gamebox.move_window(delta)
			
		
	
	def rblit(self, to):
		super(Interface, self).rblit(to)
		if self.cursor:
			self.cursor.rblit(to, pygame.mouse.get_pos())
		
		
	def update(self, dt):
		self.infobox.update(dt)
		self.gamebox.update(dt)
		
		self.make_wheel_scrool()
	
	def mainloop(self, g):
		dt = g.dt

		# rener
		g.fill((0,0,0))
		self.rblit(g)
		g.flip()
		
		#print 'flip', dt
				
		self.ctrl.dispath()		
		
		#mpos = pygame.mouse.get_pos() 
		#print mpos
		
		if self.order.is_ready():
			print 'send_order', self.order.action, self.order.args
			self.game.send_order(self.order.action, self.order.args)
			self.order.reset()
			 
		# update
		self.update(dt)
		self.game.update(dt*8.0)
		
				
	
			
			



# --------------------------------------------------------
def find_collision(obj, p):
	
	# pozycja obiektow podana wzglednie
	
	if isinstance(obj, Node):
		for subobj in obj:
			if point_in_box(p, subobj):
				return find_collision(subobj, p - subobj.pos)
			
	return obj



#~ cmds = [
#~ 'build Mine', Position
#~ 'build Generator', Position
#~ 'select(P)'
#~ ]

# --------------------------------------------------------
def abs_pos(x, apos):
	apos += x.pos
	if x.env:
		return abs_pos(x.env, apos)
	else:
		return apos
		





class Infobox(VBox):
	
	def __init__(self, **kwargs):
		font = kwargs.pop('font')
		self.render = kwargs.pop('render')
		self.order = kwargs.pop('order')
		self.ctrl = kwargs.pop('ctrl')

		super(Infobox, self).__init__(**kwargs)
		self.font = font
		
		self.target = None
		self.last_ts = None
		
		self.progbox = VBox(
			dim = lambda s: (s.p.dim[0], 100),
		)
		
		self.cmdbox = GridBox(
			cols = 4,
			dim = lambda s: (s.p.dim[0], s.p.dim[0]),
		)
		
		self.resbox = VBox(
			dim = lambda s: (s.p.dim[0], 140),
		)

		self.add(self.cmdbox, self.resbox, self.progbox)

	def h_unit_order(self, box, action, event, addargs=None):	
		if event.button == 1:
			if point_in_rect(event.pos, box.pos, box.end):
				self.order.action = action
				self.order.args = [self.target.key]
				if addargs is not None:
					self.order.args.extend(addargs)
					
			
	
	
	def select(self, x):
		self.target = x
		
		if isinstance(x, MobileAutomat):
			
			# icon action addargs
			ICON = 0
			ACTION = 1
			ADDARG = 2
			orders = [
				('move', 'move'),
				('stop', 'stop'),
			]
			
			if isinstance(x, Manip):
				orders.extend([
					(CoalMine, 'build', CoalMine),
					(MetalMine, 'build', MetalMine),
					(Generator, 'build', Generator),
					(Solar, 'build', Solar),
					(MGPost, 'build', MGPost),
					(ControlPost, 'build', ControlPost),
					(Factory, 'build', Factory),
					#('build', Mutant),
					(Recycler, 'build', Recycler),
					(GreenHouse, 'build', GreenHouse),
				])
			
			self.cmdbox.clear()
			
			size = self.cmdbox.dim[0] / self.cmdbox.cols
			
			for o in orders:
				
				cb = CBox(
					content=self.render(o[ICON], dim = vec(size,size)),
					dim = lambda s: s.content.dim,
					border = 1,
				)
				
				cb.on(
					self.ctrl, 
					et.MOUSEBUTTONDOWN, 
					partial(
						self.h_unit_order, 
						cb, 
						o[ACTION], 
						addargs=([o[ADDARG]] if len(o) > 2 else None)
					),
				)		
				
				self.cmdbox.add(cb)
				
			self.cmdbox.refresh()
			
				
		else:	
			self.cmdbox.clear()
			
		
	def update(self, dt):
		x = self.target
		
		if isinstance(x, BaseContainer):
			self.resbox.clear()
			
			for r in x:
				t = '{0} {1:.1f}/{2:.1f}'.format(r.name, x.mult(r), x.capacity(r))
				
				self.resbox.add(
					TextBox(
						text = t, 
						font = self.font,
						dim = lambda s: s.content.dim,
					)
				)
				
				
			self.resbox.refresh()
			
		else:
			if len(self.resbox):
				self.resbox.clear()
				self.resbox.refresh()
				
				
		if isinstance(x, Automat):
			ts = [x.cget(i)[0].__name__ for i in range(0, x.clen())]
			if ts != self.last_ts:
				self.progbox.clear()
				for t in ts:	
					self.progbox.add(
						TextBox(
							text = t, 
							font = self.font,
							dim = lambda s: s.content.dim,
						)
					)
				
					
				self.progbox.refresh()
				self.last_ts = ts
				
		else:
			if len(self.progbox):
				self.progbox.clear()
				self.progbox.refresh()
				self.last_ts = None
		
	
'''	
	if isinstance(x, BaseContainer):
		infobox.append(ImageBox(img=Image(text='    ----    ', color=WHITE)))
		for c in x:
			txt = '%s: %.1f' % (c.__class__.__name__, x.mult(c))
			infobox.append(ImageBox(img=Image(text=txt, color=WHITE)))
	
	if hasattr(x, 'ballance'):
		infobox.append(ImageBox(img=Image(text='    ----    ', color=WHITE)))
		for k,v in x.ballance.items():
			tt = '%s: %.1f' % (str(k), v)
			infobox.append(ImageBox(img=Image(text=tt, color=WHITE)))
'''

	

# ------------------------------
infobox_tab = {

}



# draw images according to game
	


def connect(**kwargs):
	for lab1,obj1 in kwargs.items():
		for lab2,obj2 in kwargs.items():
			assert not hasattr(obj1, lab2)
			setattr(obj1, lab2, obj2)
	
	

	

class GameBox(Box, EventSource):
	def __init__(self, **kwargs):
		""" Proxy dodajace funkcjonalnosc content (rblit) dzieki czemu mozna wstawic do CBoxa
		game -- obiekt Game ktory bedzie reprezentowany
		"""
				
		self.game = kwargs.pop('game')
		self.env = kwargs.pop('env')
		self.ctrl = kwargs.pop('ctrl')		
		super(GameBox, self).__init__(**kwargs)
		
		
		self.window_pos = vec(0, 0)
		self.window_dim = None #(20,20)     #self.dim
		
		self._rscale = 1.0
		self._dscale = 1.0		
		
		self.map_dim = vec(self.game.map.size()) * 24 

		self.selected = None
		
		# warstwa sladow
		#self.tracks
		
		self.on(self.ctrl, et.MOUSEBUTTONDOWN, self.onclick)
		
		
	
	def refresh(self):
		super(GameBox, self).refresh()
		
	
	def get_zoom(self):
		return self._dscale

	def constraint_window(self):
		map_dim = vec(self.map_dim) * self.get_zoom()
		
		if self.window_pos[1] < 0:
			self.window_pos = vec(self.window_pos[0], 0)
						
		if self.window_pos[1] + self.window_dim[1] > map_dim[1]:
			self.window_pos = vec(self.window_pos[0], map_dim[1] - self.window_dim[1])
										
		if self.window_pos[0] < 0:
			self.window_pos = vec(0, self.window_pos[1])
							
		if self.window_pos[0] + self.window_dim[0] > map_dim[0]:
			self.window_pos = vec(map_dim[0] - self.window_dim[0], self.window_pos[1])
		
			
		
			

	def _update_zoom(self, _rscale):
		# discrette zoom such that field_dim is int
		_dscale = int(_rscale * FIELD_DIM) / float(FIELD_DIM)
		
		# window_dis
		window_dim = vec(self.dim) / _dscale
		
		# window pos such that map point under mouse do not move
		rmpos = vec(pygame.mouse.get_pos()) - vec(self.pos)
		window_pos = self.window_pos + rmpos/self._dscale - rmpos/_dscale
		
		# set
		self._rscale = _rscale
		self._dscale = _dscale
		self.window_dim = window_dim
		self.window_pos = window_pos
		
		self.constraint_window()

	def mul_zoom(self, mul):
		self._update_zoom(self._rscale * mul)
		
	def set_zoom(self, zoom):
		self._update_zoom(zoom)
		
	
	def BtoA(self, pos_b):
		"""
		B -- position on game map
		A -- position relative to user interface window
		"""
		return (vec(pos_b) - self.window_pos) * self.get_zoom() + vec(self.pos)
		
	def AtoB(self, pos_a):
		"""
		A -- position relative to user interface window
		B -- position on game map
		"""
		
		return (vec(pos_a) - vec(self.pos)) / self.get_zoom() + self.window_pos
	
		
	@property
	def window_end(self):
		return self.window_pos + self.window_dim
	
	
	
	def rblit_map(self, to, render_tab, window_pos, window_end, zoom):
		"""
		scale map visible through window to dim and blit
		
		window_dim = dim * scale
		
		"""
		
		terr = self.game.map
		
		# total area 
		cmax_ij = terr.size()
		cmin_ij = 0,0
			
		# window covered area
		vmin_ij = map(int, window_pos / FIELD_DIM)
		vmax_ij = map(int, window_end / FIELD_DIM + vec(1,1))
		
		min_ij = max(vmin_ij[0], cmin_ij[0]), max(vmin_ij[1], cmin_ij[1])
		max_ij = min(vmax_ij[0], cmax_ij[0]), min(vmax_ij[1], cmax_ij[1])
		
		for j in range(min_ij[1], max_ij[1]):
			for i in range(min_ij[0], max_ij[0]):
				t = terr.get(i,j)
				a = self.BtoA(vec(i,j) * FIELD_DIM)
				render_tab[t].render(scale = zoom).rblit(to, a)
		
				
	
	
	def onclick(self, event):
		pos, button = event.pos, event.button		
		
		if not point_in_rect(pos, self.pos, self.end):
			return
		
		#print 'onclick', self.AtoB(pos), button
		
		if button == 1:
			if self.env.mode == 'build':	
				self.env.game.build(self.env.build_obj, self.AtoB(pos))
				self.env.mode = None
				self.env.cursor = None
			
			elif self.env.get_mode() == 'point':	
				#print 'select_pos', self.AtoB(pos)
				self.fire(Event('select_pos', pos = self.AtoB(pos)))
				
			else:
				xs = list(self.game.iter_objs_under_pos(self.AtoB(pos)))
				self.selected = select_after(xs, self.selected)
				#print 'select', self.selected
				self.fire(Event('select', sel = self.selected))
				
				 

	
	
	

	
	def rblit(self, to):
		render_tab = self.env.render_tab
		zoom = self.get_zoom()
		
		to.set_clip(Rect(self.pos, self.dim))
		
		self.rblit_map(to, 
			render_tab = render_tab, 
			window_pos = self.window_pos,
			window_end = self.window_end,
			zoom = zoom,
		)
		
		sgame = sorted(self.game, lambda a,b: cmp(a.z, b.z))
		for x in sgame:
			if x.__class__ in self.env.render_tab:				
				ni = self.env.render_tab[x.__class__].render(scale = zoom)
				ni.rblit(to, self.BtoA(x.pos))
		
		if self.selected:
			to.draw_rect(self.BtoA(self.selected.pos), self.selected.dim * zoom, (0.5,0.5,0.5), 1)
			
		if self.border:
			to.draw_rect(vec(self.pos), self.dim, (0.5,0.5,0.5), 1)
		
		# draw ghost under mouse cursor if any
		mpos = vec(pygame.mouse.get_pos())
		
		
		
		o = self.env.order
		a = o.action
		p = o.get_next_param_type()
		if a == 'move' and p == 'point':
			ghost = render_tab['move'].render(scale = zoom)
			
		elif a == 'build' and p == 'point':
			struct = o.args[1]
			if struct in render_tab:
				ghost = render_tab[struct].render(scale = zoom)
		else:
			ghost = None
		
		if ghost:			
			ghost.rblit(to, mpos - ghost.dim / 2.0)
			
		
			
			
			
		to.set_clip(None)
		
	
		
		
		

	def render(self):
		w = Image(surface = self.terrain.surface.copy())
		# obrobka w
		return w
	
	
	def move_window(self, delta):
		self.window_pos = self.window_pos + delta
		self.constraint_window()

	
	def update(self, dt):
		
		SPEED = 20.0 
		
		keys = pygame.key.get_pressed()
		
		map_dim = vec(self.map_dim) * self.get_zoom()
		
		# pygame.VIDEORESIZE
		
		vert = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
		hori = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
			
		self.move_window(vec(hori, vert) * SPEED)			
			
		
		
		# pojazdy robia slady		
		#ts = self.game.radar(ALL, Truck)
		#for t in ts:			
		#	if random.randint(0,7) == 0:
		#		self.surface.blit(image_tab['track'].surface, tuple(t.center))
		
	
		
		
		
		


	
	
	

def render_gamebox(box):
	
	# box.view_pos
	
	surf = render_map(box.game)
	screen.blit(surf, pos = base_pos)
	

def uni_render(x, base_pos):
	func = render_tab.get(type(x), default = render_unknown)
	func(base_pos, x)
	
		

# ----------------------------
def render_all(x, base_pos):

	
	# render childrens
	if isinstance(x, Node):		
		base_pos += x.pos
		for xx in x:
			render_all(xx, base_pos)

		base_pos -= x.pos
		


	
			
def render_unknown(base_pos, x):
	render_rect(base_pos + x.pos, x.dim, (100,0,0), 1)

def render_image(base_pos, x):
	image_tab[type(x)].render(base_pos + x.pos)


#render_tab = {
#	ImageBox: render_ImageBox,
#	GameBox: partial(render_GameBox, )
#}


def select_after(xs, sel):
	ret_next = False
	for x in xs:
		if ret_next:
			return x				
		
		if x is sel:
			ret_next = True
			
	if xs:
		return xs[0]

	
	
	
def test_select_after():
	assert select_after([], None) == None
	assert select_after([1,2,3], None) == 1
	assert select_after([1,2,3], 1) == 2
	assert select_after([1,2,3], 2) == 3
	assert select_after([1,2,3], 3) == 1
	