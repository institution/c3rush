
quantity

class Unit(object):
	def __init__(self, symb=None, value=None, ud=None):
		
		self.ud = ud if ud != None else self.ud = defaultdict(lambda:0)
			
		self.base
			
		if symb:
			self.ud[symb] = 1
			
		self.value = value if value != None else 1.0
		
	
	def equal_to(self, unit):
		pass
		
	def add(self, other):
		
		
	def mul(self, other):
		ud = self.unit.copy()		
		for k,v in other.unit.items():
			ud[k] += v			
		return Unit(value = self.value * other.value, ud = ud)
			
	def rmul(self, other):
		
		
		
(10 * m/s).to(km/h)