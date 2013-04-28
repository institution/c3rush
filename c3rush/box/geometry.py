# coding: utf-8
import sys
from functools import partial
from collections import defaultdict
from vec import point_in_rect


class Error(Exception):
	pass

#class Text(Box):
#	def __init__(self, text, align=-1, color=(1.0, 1.0, 1.0)):
#		pass
	

def val(s, l):
	if hasattr(l, '__call__'):
		l = l(s)
	if isinstance(l, tuple):
		l = tuple(val(s, x) for x in l)
	return l
	

class Event(object):
	def __init__(self, type, **kwargs):
		super(Event, self).__init__()
		self.type = type
		self.kwargs = kwargs
	
	def __getattr__(self, key):
		return self.kwargs[key]
	

from copy import copy
	
class EventSource(object):
	def __init__(self, **kwargs):
		super(EventSource, self).__init__(**kwargs)
		self.__reg = defaultdict(lambda: set())
			
	def fire(self, ev):
		if ev.type in self.__reg:
			hs1 = self.__reg[ev.type]
			hs2 = copy(hs1)
			for h in hs2:
				# still in hs1?
				if h in hs1:
					h(ev)
			
	def _register(self, type, handler):
		self.__reg[type].add(handler)
		
	def _unregister(self, type, handler):
		self.__reg[type].remove(handler)
		
	
	

class Interactive(object):
	def __init__(self, **kwargs):
		on = kwargs.pop('on', {})
		
		super(Interactive, self).__init__(**kwargs)
	
		self._on = defaultdict(lambda: [])

	def on(self, esrc, etype, handler):
		esrc._register(etype, handler)
		self._on[(esrc, etype)] = handler
		
	def destroy(self):
		for (esrc, etype),handler in self._on.items():
			esrc._unregister(etype, handler)
		self._on = None
		
		
		

class Box(Interactive):
	
	def __del__(self):
		print 'del', self
	
	def __init__(self, **kwargs):
		self._pos = kwargs.pop('pos', (0,0))
		self._dim = kwargs.pop('dim', (20,20))
		self.childs = kwargs.pop('childs', [])
		self.border = kwargs.pop('border', 0)
		self.p = kwargs.pop('p', None)
		
		super(Box, self).__init__(**kwargs)
				
		self._pos_c = None
		self._dim_c	= None
	
	#def set_p(self, p):
	#	self.p = p
				
	@property				
	def pos(self):
		if self._pos_c is None:
			self._pos_c = val(self, self._pos)
		return self._pos_c
	
	@pos.setter
	def pos(self, x):
		self._pos = x
			
	@property			
	def dim(self):
		if self._dim_c is None:
			self._dim_c	= val(self, self._dim)
		return self._dim_c
				
	@dim.setter
	def dim(self, x):
		self._dim = x
		
	@property			
	def end(self):
		d = self.dim
		p = self.pos
		return (p[0]+d[0], p[1]+d[1])
	
	def refresh(self):
		self._pos_c = None
		self._dim_c = None
		
	
	def propagate_click(self, event):
		xy = event.pos
		
		pos = self.pos
		end = self.end
		
		#print self, self.on.get('click'), pos, end, xy
		
		if point_in_rect(xy, pos, end):
			if 'click' in self._on:
				rel_xy = (xy[0] - pos[0], xy[1] - pos[1])
				
				for f in self._on['click']:
					f(event)
				
			for b in self:
				b.propagate_click(event)
		
	def __iter__(self):
		return; yield
				

class CBox(Box):
	def __init__(self, **kwargs):		
		content = kwargs.pop('content', None)
		
		#dim = kwargs.pop('dim', None)
		#if content is not None:
		#	content.dim
				
		super(CBox, self).__init__(**kwargs)
		
		self._content = content
	
	@property
	def content(self):
		return self._content
		
	@content.setter
	def content(self, value):
		self._content = value	
		
		
class TextBox(Box):
	pass
		
class PBox(Box):
	def __init__(self, **kwargs):
		childs = kwargs.pop('childs', [])
		super(PBox, self).__init__(**kwargs)
		
		self.add(*childs)
		
	def add(self, *cs):
		self.childs.extend(cs)
		for c in cs:
			c.p = self
			
	def destroy(self):
		Box.destroy(self)
		self.clear()
		
	def clear(self):
		for c in self.childs:
			c.p = None
			c.destroy()
		self.childs = []
		
	def __iter__(self):
		return iter(self.childs)
		
	def child_dim_(self, i):
		return (c.dim[i] for c in self)
	
	def __len__(self):
		return len(self.childs)
	
	def refresh(self):
		for c in self:
			c.refresh()
		Box.refresh(self)
		


class VBox(PBox):
	
	def __init__(self, **kwargs):
		self.__prev = None
		super(VBox, self).__init__(**kwargs)
		
		
	def add(self, *cs):
		for c in cs:
			if self.__prev is None:
				c._pos = lambda s: self.pos
			else:
				c._pos = partial(lambda prev, s: (prev.pos[0], prev.end[1]), self.__prev)
			
			self.__prev = c
			
		PBox.add(self, *cs)
	
		
	def clear(self):
		self.__prev = None
		PBox.clear(self)
		


class GridBox(PBox):
	
	def __init__(self, **kwargs):
		self.__prev = None
		self.cols = kwargs.pop('cols')
		super(GridBox, self).__init__(**kwargs)
		
		
	def add(self, *cs):
		for c in cs:
			if self.__prev is None:
				c._pos = lambda s: self.pos
				
			else:
				c._dim = lambda s: (self.dim[0]/self.cols, self.dim[0]/self.cols)
				
				if len(self) % self.cols == 0:
					# next row
					c._pos = partial(
						lambda prev, s: (self.pos[0], prev.end[1]), 
						self.__prev
					)
															
				else:
					c._pos = partial(
						lambda prev, s: (prev.end[0], prev.pos[1]), 
						self.__prev
					)
				
			self.__prev = c
			
		PBox.add(self, *cs)
	
		
	def clear(self):
		self.__prev = None
		PBox.clear(self)
		
		
		
			
			



		