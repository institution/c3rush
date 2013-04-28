# coding: utf-8

from engine import vec

from functools import partial



# ------------------------------------
def space2d(x, y):
	j = 0
	while j < y:
		i = 0
		while i < x:
			yield (i,j)
			i += 1
		j += 1
		

# ------------------------------------
def mulset(A, B):
	for a in A:
		for b in B:
			yield (a,b)
		

# ------------------------------------
class Error:
	pass

# ------------------------------------	
def default(val, def_val):
	return val if val != None else def_val
	
# ------------------------------------
def point_in_box(point, box):
	if box.pos.x < point.x < box.pos.x + box.dim.x:
		if box.pos.y < point.y < box.pos.y + box.dim.y:
			return 1
	return 0

# ------------------------------------
def DefaultDict(val):
	
	class DD(dict):
		def __init__(self):
			dict.__init__(self)
			
		def __missing__(key):
			return []
	

# ------------------------------------
class Node(object):
	def __init__(self):
		self._data = []

	def append(self, x):
		self._data.append(x)
		x.env = self
		
	def __getitem__(self, idx):
		return self._data[idx]
		
	def __setitem__(self, idx, x):
		self._data[idx] = x
		x.env = self
	
	def __iter__(self):
		return iter(self._data)
		
	def remove(self, x):
		self._data.remove(x)
	
	def __len__(self):
		return len(self._data)
	
	

# ------------------------------------		
INF = float('+inf')		


# ------------------------------------		
def is_empty(x):
	return bool(len(x))
	
# ------------------------------------
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)



		