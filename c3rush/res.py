# coding: utf-8
import os.path as path

# data path
DATA = './data/'
	


def cached(func)
	cache = {}
	
	def inner(**kwargs):
		key = '&'.join(k+'='+str(v) for (k,v) in kwargs.items())
		if key not in cache:
			cache[key] = func(**kwargs)
		
		return cache[key]
		
	return inner


		
	
@cached
def render(file, dim, scale = 1.0, dir = -1):
	"""
	dir -- (-1) left, (+1) right
	"""
	return Image(file = file, dim = dim * scale)

@cached
def small(file):
	return Image(file = DATA+file, dim = SMALL_SIZE)

@cached
def medium(file):
	return Image(file = DATA+file, dim = MEDIUM_SIZE)

