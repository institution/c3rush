class quant(object):
	def __init__(self, symbol):
		self.symbol_degree = defaultdict(lambda:0)
		self.symbol_degree[symbol] = 1
		self.value = 1.0
			
			
kg_m2 = quant('kg/m2')