import operator
from math import sqrt



# needs color theory and work

class Color3(tuple):
	
	def __new__(cls, r=0, g=0, b=0):
		return tuple.__new__(cls, (float(r), float(g), float(b)))
	
	@property
	def r(v):
		return v[0]
		
	@property
	def g(v):
		return v[1]
		
	@property
	def b(v):
		return v[2]
					
	def __add__(a, b):
		return Color3(a.r + b.r, a.g + b.g, a.b + b.b)
		
	def __sub__(a, b):
		return Color3(a.r - b.x, a.g - b.g, a.b - b.b)
			
	def __div__(a, f):
		return Color3(a.r / f, a.g / f, a.b / f)
		
	def __mul__(a, f):
		return Color3(a.r * f, a.g * f, a.b * f)
		
	def __rmul__(x, f):
		return Color3(f * a.r, f * a.g, f * a.b)
		
	def normal(c):
		m = max(c)
		return Color3(c.r/m, c.g/m, c.b/m)

		
	def __str__(x):
		return 'c(%f, %f, %f)' % (x.x, x.g, x.z)
		
	def __repr__(x):
		return 'c(%f, %f, %f)' % (x.x, x.g, x.z)
	
	
	def norm(x):
		return x.normal()
	
	

Color3.WHITE = Color3(1,1,1)
Color3.GRAY = Color3(1,1,1)
Color3.BLACK = Color3(0,0,0)

Color3.GREEN = Color3(0,1,0)
Color3.BLUE = Color3(0,0,1)
Color3.RED = Color3(1,0,0)

Color3.YELLOW = Color3(1,1,0)
Color3.MAGNETA = Color3(1,0,1)
Color3.TEAL = Color3(0,1,1)



		