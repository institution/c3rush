


def add(a,b):
	return (a[0]+b[0], a[1]+b[1])
	
		
def range2(shape):
    for j in range(shape[1]):
        for i in range(shape[0]):
            yield (i,j)
        
class Array2(object):
	# random access 2d array
	
	def load(self, data):
		self.data = []
		j = 0
		for line in data:
			self.data.append([])
			i = 0
			for cell in line:
				self.data[j].append(cell)
				i += 1
			self.width = i				
			j += 1			
		self.height = j

	def copy(self):
		cp = self.__class__(self.width, self.height)
		for k in self:
			cp[k] = self[k]
		return cp
		
	def resize(self, width, height):
		self.width, self.height = width, height
		
		self.data = []
		for j in range(height):
			self.data.append([])
			for i in range(width):
				self.data[j].append(None)
		
		
	def dim(self):
		return (self.width, self.height)

	def keys(self):
		return range2(self.dim())
		
	def __iter__(self):
		return self.keys()
		
	def values(self):
		for k in self:
			yield self[k]

	def __init__(self, wid=0, hei=0):
		self.width = wid
		self.height = hei
		
		self.resize(wid, hei)
		
	
	def __getitem__(self, key):
		return self.data[key[1]][key[0]]
		
	def __setitem__(self, key, value):
		self.data[key[1]][key[0]] = value
		