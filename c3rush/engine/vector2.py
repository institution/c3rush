import operator
from math import sqrt



def point_in_rect(xy, pos, end):
	""" Checks whether the point is within the rectangle.
	xy -- test point
	pos -- top-left rectangle corner
	end -- bottom-right rectangle corner
	"""
	return pos[0] <= xy[0] <= end[0] and pos[1] <= xy[1] <= end[1]



class Vector2(tuple):
	
	def __new__(cls, x=0, y=0):
		if isinstance(x,tuple):
			return tuple.__new__(cls, (x[0], x[1]))
			
		return tuple.__new__(cls, (x, y))
	
	@property
	def x(v):
		return v[0]
		
	@property
	def y(v):
		return v[1]
				
	def __add__(a, b):
		return Vector2(a.x + b.x, a.y + b.y)
		
	def __sub__(a, b):
		return Vector2(a.x - b.x, a.y - b.y)
			
	def __div__(a, f):
		return Vector2(a.x / f, a.y / f)
		
	def __mul__(a, f):
		return Vector2(a[0] * f, a[1] * f)
		
	def __rmul__(x, f):
		return Vector2(f * x[0], f * x[1])
	
	def dot(a, b):
		return a.x * b.x + a.y * b.y
		
	def magnitude(a):
		return sqrt(a.dot(a))
		
	def mag2(a):
		return a.dot(a)
		
	def distance(a,b):
		return (a - b).magnitude()
		
	def __neg__(a):
		return Vector2(-a.x, -a.y)
	
	def rotate(rot, vec):
		return rotate(rot, vec)
		
	def normal(a):
		m = a.magnitude()
		return a / m if m else Vector2()
		
	def __str__(x):
		return 'v(%f, %f)' % (x.x, x.y)
		
	def __repr__(x):
		return 'v(%f, %f)' % (x.x, x.y)
	
	
	def norm(x):
		return x.normal()
	def dist(x):
		return x.distance()		
	def mag(x):
		return x.magnitude()
	
	
	
	
		
	@staticmethod
	def oper(f,s):
		""" Defines new function
		
		op(v,w) := (f(v_x, w_x), s(v_y, w_y))
		
		"""
		
		def op(a,b):
			return Vector2(f(a.x,b.x), s(a.y,b.y))
		return op
			
		
	
	
	
	
	
	
	
	
def test():
	v = Vector2
	print v(1,2)
	from operator import add
	
	op = v.oper(add,max)
	print reduce(op, [v(1,2),v(3,4)])
	
	
	

if __name__ == '__main__':
    test()
	