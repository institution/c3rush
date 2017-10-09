#/usr/bin/env python
# coding: utf-8

# wszystkie jednostki w SI

from base import *
from params import *
import time
import conf
from vec import point_in_rect, vec
from collections import defaultdict
EPSILON = 4.0
import weakref
import math

def dist(x,y):
	a = x[0]-y[0]
	b = x[1]-y[1]
	return math.sqrt(a*a + b*b)


g_dt = 0.0

from engine.geometry import *

# --------
class Res(object):
	def __eq__(x, y):
		return type(x) == type(y)

	def __hash__(x):
		return hash(type(x))
		
	def __str__(self):
		return self.name
		
	def dump(self):
		return '{}()'.format(self.__class__.__name__)


class Energy(Res):
	volume = 0.01
	name = 'energy'
	
class Wind(Res):
	volume = 0.01
	name = 'wind'
	
class Solar(Res):
	volume = 0.01
	name = 'solar'



class Coal(Res):
	volume = 1.0
	name = 'coal'

class Food(Res):
	volume = 1.0
	name = 'food'

class Smog(Res):
	volume = 1.0
	name = 'smog'

class Metal(Res):
	volume = 1.0
	name = 'metal'

class Oil(Res):
	volume = 0.1
	name = 'oil'

class NaturalGas(Res):
	volume = 0.1
	name = 'natural gas'




class Waste(Res):
	volume = 0.1
	name = 'scrap'

class Junk(Res):
	volume = 0.1
	name = 'scrap'

class SolidWaste(Res):
	volume = 0.1
	name = 'scrap'

class OrganicWaste(Res):
	volume = 0.1
	name = 'organic waste'
		
class SynteticWaste(Res):
	volume = 0.1
	name = 'syntetic waste'




class TruckRes(Res):
	volume = 18
	name = 'truck'


waste = Waste()
coal = Coal()
metal = Metal()
oil = Oil()
energy = Energy()
natural_gas = NaturalGas()
food = Food()
new_truck = TruckRes()




# -------------------------
COAL_TO_ENERGY = [(coal, -0.4), (energy, +5.2)]
ENERGY_TO_TRUCK = [(energy, -2.5), (new_truck, +0.05)]


MINE_COAL = [(energy, -2.5), (coal, +0.1)]
MINE_METAL = [(energy, -2.5), (metal, +0.1)]
MINE_OIL_NG = [(energy, -2.5), (oil, +0.5), (natural_gas, +2.0)]

COAL_TO_ENERGY = [(coal, -0.1), (energy, +5.0)]

MAKE_TRUCK = [(metal, -1.0), (energy, -1.0), (new_truck, +0.01)]

MAKE_FOOD = [(energy, -2.0), (food, +0.01)]







# deploy
#------------------------------------------
# Fort [food, energy -> workforce?]
# Coal Mine [energy -> coal]
# Metal Mine  [energy -> metal]
# Oil Rig [energy -> oil + natural_gas]
# Coal Generator [coal -> energy]
# Factory [metal + energy -> truck]
# GreenHouse [energy -> food]
# MGPost [metal]
# Truck [oil] [natural_gas] [energy] [food]

# Solar Generator [solar -> energy]
# Wind Generator [wind -> energy]
# Lab [energy -> lab]
# RecyclingCenter [solid_garbage -> metal, organic_garbage -> energy]
# Geothermal Generator [energy]

# global(energy, smog), field(natural resource, wind, coal...) and building storage


class Health(object):
	max_health = 1.0
	
	def __init__(self):
		self.health = self.max_health
	
	def __nonzero__(self):
		return int(self.health)
		





import random

# ---------------------------
def nearest(xs, pos):

	best = INF
	rs = []
		
	for x in xs:
		d = dist(pos, x.pos)
			
		if d < best:
			best = d
			rs = [x]
			
		elif d == best:
			rs.append(x)
			
	return random.choice(rs) if rs else None




# ---------------------------
def nearestd(xs, pos):

	best = INF
	rs = []
		
	for x in xs:
		d = dist(pos, x.pos)
			
		if d < best:
			best = d
			rs = [x]
			
		elif d == best:
			rs.append(x)
			
	return (random.choice(rs) if rs else None, best)





# ---------------------------
class Ballance(dict):
	def __missing__(self, key):
		return 0.0



# -------------------------
class Control(object):
	
	# -------------------------
	def __init__(self):
		
		self.transports = []
		self.registered = []
		
		self.what = [waste, coal, metal, food]
		
	# -------------------------
	def register(self, who):
		self.registered.append(who)

	# -------------------------
	def best_producent_for(self, who, what):
		xs = []
		for x in self.registered:
			if x.ballance[what] >= 10:
				print x, 'ballance', what, x.ballance[what], '>= 10'
				xs.append(x)
			
		return nearest(xs, who.pos) if xs else None
	
	# -------------------------	
	def best_consument_for(self, who, what):
		xs = []
		for x in self.registered:
			if x.ballance[what] <= -10:
				print x, 'ballance', what, x.ballance[what], '<= -10'
				xs.append(x)
		
		return nearest(xs, who.pos) if xs else None
	
	
	# -------------------------
	def register_transport(self, who):
		self.transports.append(who)

	# -------------------------
	def assign(ctrl, truck, a, b, what, max):
		truck.cclear()
		truck.cpush(truck.move, a.truck_entry_center)
		truck.cpush(truck.wait, 1.0)
		truck.cpush(ctrl.register_transport, truck)
		truck.cpush(truck.unload, b, what, max)
		truck.cpush(truck.load, a, what, max)
		
		print 'assign', a, b
	
	# -------------------------
	def reserve_truck(self, where):
		free_truck = nearest(self.transports, where)
		self.transports.remove(free_truck)
		return free_truck
					
	
	# -------------------------
	def update(self, dt):
		
		what = self.what.pop(0)
					
		if self.transports:
						
			what_have = [x for x in self.registered if x.ballance[what] >= 10]
			what_need = [x for x in self.registered if x.ballance[what] <= -10]
			
			rs = []
			for (a,b) in mulset(what_have, what_need):
				rs.append( (a, b, dist(a.pos, b.pos)) )
				
			if rs:
				rs.sort(lambda e1,e2: cmp(e1[2], e2[2]))
				
				a, b, _dis = rs[0]
				
				free_truck = self.reserve_truck(a.pos)
				a.ballance[what] -= 10
				b.ballance[what] += 10
				self.assign(free_truck, a, b, what, 10)
						

		self.what.append(what)





def g_get_uniq_key(use=None, _used=set([0])):
	if use is None:
		use = max(_used) + 1		
	
	if use in _used:
		raise Error('use key not unique')
		
	_used.add(use)
		
	return use

class Keyed(object):
	def __init__(self, **kw):
		key = kw.pop('key', None)
		self.key = g_get_uniq_key(key)
		
	



class Error(Exception):
	pass



def test_automat_dump():
	a = Automat(key = 11, _cmds = [1,2,3], _exec_delay = 0.3)
	d = a.dump()
	e = {
		'key': 11,
		'_cmds': [1,2,3],
		'_exec_delay': 0.3,
	}
	assert d == e, repr((d, e))

class Automat(Keyed):
	def __init__(self, **kwargs):
		#self.ctrl = kwargs.pop('ctrl', None)
		
		self._cmds = kwargs.pop('_cmds', [])
		self._exec_delay = kwargs.pop('_exec_delay', 1.0)
		
		Keyed.__init__(self, **kwargs)
				
		
	#def cmd_push(self, ctrl, cmd):
	#	if self.ctrl != ctrl:
	#		raise Error('will not comply')
	

		
	
	def exec_prog(self):
		while len(self._cmds) > 0:
			func, args1, args2 = self.cpop()
			x = func(*args1, **args2)
			if x == None or x == 0 or x == False:
				break
	
	def update(self, dt):
		self._exec_delay += dt
		if self._exec_delay > 0.5:
			self.exec_prog()
			self._exec_delay = 0.0
	
	def crpush(self, cmd, *args1, **args2):
		""" Append command to program """
		self._cmds.insert(0, (cmd, args1, args2))
	
	def cpush(self, cmd, *args1, **args2):
		""" Append command to program """
		self._cmds.append((cmd, args1, args2))
	
	def cclear(self):
		""" Clear program """
		self._cmds = []
	
	# -------------------------
	def cpop(self):
		""" Pop next command from program """
		return self._cmds.pop(-1)
		
	# -------------------------
	def clen(self):
		""" Length of the program """
		return len(self._cmds)
		
	# -------------------------
	def cget(self, i):
		""" Get command from program at i """
		return self._cmds[i]
	
	#def list_orders(self):
	#	return [dict(label = f.__name__, func=f) for f in (self.wait,)]
		
	#
	# common orders
	#
	# -------------------------
	def wait(self, time):
		if time > 0:
			self.cpush(self.wait, time - g_dt)
			return 0
		else:
			return 1
			
	
	
#~ class PhysicalUnit(object):
	#~ def weight(self):
		#~ return self.unit_weight
		
	#~ def volume(self):
		#~ return self.unit_volume
		


""" indeksowany instancja obiektu 
moze przechowywac objekty podtypu takiego jak what
cont.volume
cont[what]
"""

class BaseContainer(dict):
	pass

class UnivContainer(BaseContainer):

	def __init__(self, volume=float('+inf')):
		dict.__init__(self)

		self.volume = volume
		self.filled = 0.0

	def mult(self, what):
		return self[what]

	def free(self, what):
		return (self.volume - self.filled) / what.volume

	def __missing__(self, key):
		return 0.0

	def capacity(self, what):
		return self.volume / what.volume

	def empty(self, what):
		return self.volume / what.volume - self[what]
		
	# low level	
	def add(self, what, m):
		self.filled += m * what.volume
		self[what] += m

	# low level
	def sub(self, what, m):
		self[what] -= m
		self.filled -= m * what.volume

	def __hash__(self):
		s = 0
		for k,v in self.items():
			s += hash(k) + hash(v)
		return s

	def __eq__(self, other):
		NotImplemented

#~ def create(cont, what, max=1):
#~ m = min(cont.empty / what.volume, max)
#~ cont.filled += m * what.volume
#~ cont[what] += m
#~ return m

#~ def destroy(cont, what, max=float('inf')):
#~ m = min(cont[what], max)
#~ cont.filled -= m * what.volume
#~ cont[what] -= m
#~ return m



# ------------------------------------
#~ """ indeksowany instancja obiektu 
		#~ moze przechowywac objekty podtypu takiego jak what
		#~ cont.volume
		#~ cont[what]
#~ """
class SpecContainer(BaseContainer):
	# --------------------------
	def __init__(self, specs, conns=None):
		dict.__init__(self)
		self.capa = specs
		for k in specs: 
			self[k] = 0.0
			
		self.connected = default(conns, {})

	# --------------------------
	def mult(self, what):
		return self.cont(what)[what]

	# --------------------------
	def capacity(self, what):
		return self.cont(what).capa[what]

	# --------------------------
	def free(self, what):
		c = self.cont(what)
		return c.capa[what] - c[what]

	# low level	
	def add(self, what, m):
		self.cont(what)[what] += m

	# low level
	def sub(self, what, m):
		self.cont(what)[what] -= m
		
	# --------------------------
	def connect(self, what, where):
		self.connected[what] = where
		
	# --------------------------
	def cont(self, what):
		if what in self.connected:
			return self.connected[what]
		else:
			return self
		
			
		
			
	

# --------------------------
#~ def destroy(cont, what, max=float('inf')):
#~ m = min(cont[what], max)
#~ cont[what] -= m
#~ return m

# --------------------------
#~ def create(cont, what, max=float('inf')):
#~ m = min(cont.free(what), max)
	#~ cont[what] += m
	#~ return m

#~ def transfer_to_world		
#~ def extract_one(cont, what):
	#~ if cont[what] >= 1:
		#~ cont[what] -= 1
	
	#~ cont.filled -= what.volume		
	#~ return copy(what)

# ----------------------------------------------
#def transfer_from_world(cont, what):
	#	what.desc()

# ----------------------------------------------
def transfer(target, source, what, max=INF):
	#if source isinstance world_container
	#m = int( min(target.free(what), source.mult(what), max) )
	m = min(target.free(what), source.mult(what), max)
	source.sub(what, m)
	target.add(what, m)
	return m




 
# ------------------------
class Decoy(object):
	z = 1
	# must have dim
	
	# ------------------------------
	def __init__(self, pos, env=None):
		self.pos = pos
		self.env = env
		

	@property
	def center(self):
		return self.pos + self.dim * 0.5

	@property
	def end(self):
		return self.pos + self.dim

	@center.setter
	def center(self, c):
		self.pos = c - self.dim * 0.5
		
	@property
	def truck_entry_center(self):
		return vec(self.pos.x + Truck.dim.x * 0.5, self.pos.y + self.dim.y - Truck.dim.y * 0.5)
		
		
	#@property.setter
	#def entry(self, c):
	#	self.pos = c - self.dim * 0.5
	
	# ---------------------
	def update(x, dt):
		pass

# ------------------------
class Mobile(Decoy):
	z = 2
	def __init__(self, env, pos, vel=None):
		Decoy.__init__(self, env, pos)
		self.vel = default(vel, vec())

	def update(x, dt):
		Decoy.update(x, dt)
		x.center += x.vel * dt










class Dump(Decoy, UnivContainer):
	dim = SMALL_SIZE
	
	def __init__(self, env, pos):
		Decoy.__init__(self, env, pos)
		UnivContainer.__init__(self)
		
		
		



class MobileAutomat(Mobile, Automat):
	max_velocity = None
	
	# -------------------------
	def __init__(self, env, pos):
		Mobile.__init__(self, env, pos)
		Automat.__init__(self)
	


	def stop(self):
		self.vel = vec()
		self.cclear()
			
	def move(self, center, d = EPSILON):
		if dist(center, self.center) < d:
			# dojechane
			print 'move complete', dist(center, self.center)
			self.vel = vec()
			return 1
			
		else:
			delta = (center - self.center)
									
			# jedz dalej
			self.vel = (center - self.center).normal() * self.max_velocity
			
			self.cpush(self.move, center, d)
			
			
			return 0

	# -------------------------
	def follow(self, cel, d = EPSILON):

		if not cel or dist(cel.center, self.center) < d:
			# dojechane albo zgubione
			self.vel = vec()
			return 1
		
		else:
			# przelicz predkosc
			self.vel = (cel.center - self.center).normal() * self.max_velocity
			self.cpush(self.follow, cel, dist)			
			return 0


	# -------------------------
	def update(self, dt):
		Automat.update(self, dt)
		Mobile.update(self, dt)
		
		

	

# ----------------------------
class Mutant(MobileAutomat, Health):
	dim = SMALL_SIZE
	max_velocity = 20.0
	max_health = MUTANT_HEALTH
	
	# -------------------------
	def __init__(self, pos, ctrl=None, env=None):
		MobileAutomat.__init__(self, env, pos)
		Health.__init__(self)
		
		self.ctrl = ctrl
		
		self.cpush(self.choose_target)

	def dump(self, blacklist=None):
		bl = ['ctrl']

	# -------------------------
	def update(self, dt):
		MobileAutomat.update(self, dt)

	
	def choose_target(self):
		self.cpush(self.choose_target)
		
		t = self.env.radar(NEAREST, MGPost, self)
		if not t:
			t = self.env.radar(NEAREST, Decoy, self)
		
		if t:
			
			self.cpush(self.shoot, t)
			return 1
	
	# -------------------------
	def shoot(self, t):
		
		if t:
			self.cpush(self.shoot, t)
			
			d = dist(t.pos, self.pos)
		
			if d <= 50:
				m = Missile(self.env, self.center - Missile.dim * 0.5, target=t)
				self.env.append(m)
				self.cpush(self.wait, 2.0)
				return 1
			else:
				self.cpush(self.follow, t, d=49)
	
		return 0


# ----------------------------
class Missile(Mobile):
	dim = vec(5,5)
	max_velocity = 70.0
	

	# -------------------
	def __init__(self, env, pos, target):
		
		Mobile.__init__(self, env, pos)
		
		self.target = target
		
		
	# -------------------
	def update(self, dt):
		Mobile.update(self, dt)
		
		if self.target:
			if dist(self.target.center, self.center) < 10:
				
				self.env.shoot(self.target)
				self.env.destroy(self)
			else:			
				self.vel = self.max_velocity * (self.target.center - self.center).normal()
		else:
				self.env.destroy(self)









# ------------------------------------
class MGPost(Decoy, Automat, Health):
	
	dim = SMALL_SIZE
	max_health = MGPOST_HEALTH
	
	# -------------------------
	def __init__(self, env, pos, ctrl):
		Decoy.__init__(self, env, pos)
		Automat.__init__(self)
		Health.__init__(self)
		
		self.ctrl = ctrl
		
		self.cpush(self.watch)
		

	
	# -------------------------
	def update(self, dt):
		Automat.update(self, dt)

	
	
	
	# -------------------------
	def watch(self):
		self.cpush(self.watch)
		
		t = self.env.radar(NEAREST, Mutant, self)
		if t and dist(t.pos, self.pos) > 96:
			t = None
		
		if t:
			self.cpush(self.shoot, t)
			return 1
			
		return 0
		
	
	# -------------------------
	def shoot(self, t):
		
		if t:
			self.cpush(self.shoot, t)
		
			d = dist(t.pos, self.pos)
		
			if d <= 96:
				m = Missile(self.env, self.center - Missile.dim * 0.5, target=t)
				self.env.append(m)
				self.cpush(self.wait, 0.5)
				return 1
			
		return 0








class Manip(MobileAutomat, Health):
	dim = SMALL_SIZE
	max_velocity = TRUCK_MAX_VELOCITY / 3.0
	max_health = TRUCK_HEALTH * 1.5
	
	# -------------------------
	def __init__(self, env, pos, ctrl):
		MobileAutomat.__init__(self, env, pos)
		Health.__init__(self)
		
		#self.tank = SContainer(volume=TRUCK_TANK_SIZE)
		self.ctrl = ctrl
		
	def place(self, what, where):
		if dist(self.center, where) <= EPSILON:
			self.env.add(what(self.env, where - what.dim/2.0, self.ctrl))
		else:
			raise Error('too far to place', dist(self.pos, where))
		
	def build(self, what, where):
		self.cpush(self.place, what, where)
		self.move(where)
		
		

# ------------------------------------
class Truck(MobileAutomat, UnivContainer, Health):
	dim = SMALL_SIZE
	max_velocity = TRUCK_MAX_VELOCITY
	max_health = TRUCK_HEALTH
	
	# -------------------------
	def __init__(self, env, pos, ctrl):
		MobileAutomat.__init__(self, env, pos)
		UnivContainer.__init__(self, volume=TRUCK_STORE_SPACE)
		Health.__init__(self)
		
		#self.tank = SContainer(volume=TRUCK_TANK_SIZE)
		self.ctrl = ctrl
		ctrl.register_transport(self)
		
	
	def __str__(self):
		return "<Truck {0}>".format(id(self))

	# -------------------------
	def wait(self, hmm):
		pass
	
	# -------------------------
	def __eq__(self, other):
		return type(self) == type(other) and self.ctrl == other.ctrl and UnivContainer.__eq__(self, other)
		
	# -------------------------
	def __hash__(self):
		return hash(self.ctrl) + UnivContainer.__hash__(self)
	
	# -------------------------
	def plan_route(self):
		
		self.cpush(self.plan_route)
		
		# zglos sie po przydzial
		x = self.ctrl.get_task(max=10)
		
		if x != None:
			(a,b,what,max) = x
			
		
			self.cpush(self.unload, b, what, max)
			self.cpush(self.load, a, what, max)				
			return 1
		
		return 0

	
	# -------------------------
	def load(self, source, what, max):
				
		if (source.truck_entry_center - self.center).magnitude() < EPSILON:
			
			transfer(self, source, what, max)
			return 1
			
		else:
			
			self.cpush(self.load, source, what, max)
			self.cpush(self.move, source.truck_entry_center)
			return 1 
	

	# -------------------------
	def unload(self, deposit, what, max):
				
		if (deposit.truck_entry_center - self.center).magnitude() < EPSILON:
			
			transfer(deposit, self, what, max)
			return 1
			
		else:
			
			self.cpush(self.unload, deposit, what, max)
			self.cpush(self.move, deposit.truck_entry_center)
			return 1
	
		
		return 1

	# -------------------------
	def update(truck, dt):
		MobileAutomat.update(truck, dt)


	
	

	
def get_next_name(basename, _c=defaultdict(lambda:0)):
	_c[basename] += 1
	return basename + '-' + str(_c[basename])

class Named(object):
	def __init__(self, **kwargs):
		super(Named, self).__init__(**kwargs)
		self.name = get_next_name(self.__class__.__name__)
		
	def __str__(self):
		return self.name

# --------------------------------------
class Reactor(object):
	
	# --------------------------------------
	def __init__(self, regs, form):
		dict.__init__(self)
		self._regs = regs
		self._formula = form
		
		#print self._formula

	# --------------------------------------
	def update(self, dt):
		r = self._regs
		
		# sprawdz dostepne skladniki i przestrzen
		min_wsp = 1.0
		
		for k,v in self._formula.items():
			if v < 0:
				# ubywa
				#print regs.mult(k), (-v)
				wsp = r.mult(k) / (-v)
			else:
				# przybywa
				#print regs.free(k), (v)
				wsp = r.free(k) / v
		
			if wsp < min_wsp:
				min_wsp = wsp
		
		ww = min_wsp * dt
		#print 'wsp:', ww
		# wykonaj
		delta = {}
		for (k,v) in self._formula.items():
			dv = ww * v		
			r.add(k, dv)
			delta[k] = dv
		
		return delta
		
		

class Abstract(object):
	pass

Abstract = Abstract()

# ------------------------------------
class Structure(Decoy, SpecContainer, Health, Reactor):
	dim = MEDIUM_SIZE
	max_health = MEDIUM_HEALTH
	
	# -------------------------
	def __init__(self, env, pos, form, cont):
		Decoy.__init__(self, env, pos)
		SpecContainer.__init__(self, cont, {energy: env.cont})
		Health.__init__(self)
		Reactor.__init__(self, self, form)
				
		self.enabled = 1		
		self.ballance = Ballance()
			
	# -------------------------
	def __str__(self):
		return self.__class__.__name__
			
	# -------------------------
	def update(self, dt):
		if self.enabled:
			delta = Reactor.update(self, dt)
			
			for k in self.ballance:
				self.ballance[k] += delta[k]

		

# ------------------------------------
class Factory(Structure):
	dim = MEDIUM_SIZE
	max_health = FACTORY_HEALTH
	
	def __init__(self, env, pos, ctrl):
		Structure.__init__(self, env, pos, 
			{metal: -0.6, energy: -12.0, new_truck: +0.01, waste: +0.05},
			{metal: 80, new_truck: 2, waste: 40}
		)
		
		self.ballance = Ballance({metal: -40, waste: 0})
		ctrl.register(self)
		self.ctrl = ctrl
		
			
	# -------------------------
	def update(self, dt):
		Structure.update(self, dt)
			
		if self.mult(new_truck) >= 1:
			self.add(new_truck, -1)
			self.env.add(Truck(self.env, self.pos, ctrl=self.ctrl))
			
			



# ---------------------------------------
class GreenHouse(Structure):
	dim = MEDIUM_SIZE
	max_health = FACTORY_HEALTH
	
	def __init__(self, env, pos, ctrl):
		Structure.__init__(self, env, pos, 
			{energy: -0.1, food: +0.1, waste: +0.05},
			{food: 40, waste: 20}
		)
		
		self.ballance = Ballance({food: 0, waste: 0})
		ctrl.register(self)
		



# ---------------------------------------
class Recycler(Structure):
	dim = MEDIUM_SIZE
	max_health = 80
	
	def __init__(self, env, pos, ctrl):
		Structure.__init__(self, env, pos,
			{waste: -0.4},
			{waste: 100}
		)
		
		self.ballance = Ballance({waste: -100})
		ctrl.register(self)
		
		
				


# ------------------------------------
class CoalMine(Structure):
	dim = MEDIUM_SIZE
	max_health = MINE_HEALTH
	
	# -------------------------
	def __init__(self, env, pos, ctrl):
		Structure.__init__(self, env, pos, 
			{energy: -0.1, coal: +0.4},
			{coal: 60}
		)
		
		self.ballance = Ballance({coal: 0})
		ctrl.register(self)
			

# ------------------------------------
class MetalMine(Structure):
	dim = MEDIUM_SIZE
	max_health = MINE_HEALTH
	
	# -------------------------
	def __init__(self, env, pos, ctrl):
		Structure.__init__(self, env, pos, 
			{energy: -0.1, metal: +0.4},
			{metal: 60}
		)
		
		self.ballance = Ballance({metal: 0})
		ctrl.register(self)



# ------------------------------------
class Generator(Structure):
	dim = MEDIUM_SIZE
	max_health = GENERATOR_HEALTH
	
	# -------------------------
	def __init__(self, env, pos, ctrl):
		Structure.__init__(self, env, pos, 
			{coal: -0.3, energy: +3.0, waste: 0.1},
			{coal: 80, waste: 40}
		)
		
		self.ballance = Ballance({coal: -40, waste: 0})
		ctrl.register(self)
		
		


# ------------------------------------
class Solar(Structure):
	dim = SMALL_SIZE
	max_health = GENERATOR_HEALTH
	
	# -------------------------
	def __init__(self, env, pos, ctrl):
		Structure.__init__(self, env, pos, 
			{energy: +1.0},
			{}
		)
		
		self.ballance = Ballance({})
		ctrl.register(self)
		

# ------------------------------------
class ControlPost(Structure):
	
	dim = MEDIUM_SIZE
	max_health = CONTROLPOST_HEALTH
	
	# -------------------------
	def __init__(self, env, pos, ctrl):
		Structure.__init__(self, env, pos,
			{energy: -2.0, food: -0.5, waste: +0.2},
			{food: 400, waste: 20}
		)
		
		self.ballance = Ballance({food: -100, waste: 0})
		ctrl.register(self)
		self.ctrl = ctrl
			
	



# --------------------
class Map(object):
	MUD = '.'
	COAL = 'c'
	METAL = 'm'
	THERMAL = 't'
	GRASS = 'g'
	
	
	def __init__(self, file):
		f = open(file)
		self.load(f)
		f.close()
	
	def dump(self):
		return 'Map({0})'.format(repr('\n'.join(self._map)))
					
	def load(self, strio):
		self._map = []
		ls = strio.readlines()
		for l in ls:
			self._map.append(l[:-1])	# bez entera
					
	def __call__(self, x, y):
		return self._map[y][x]
	
	def get(self, x, y):
		return self._map[y][x]
			
	def size(self):
		return (len(self._map[0]), len(self._map))
	
	def dim(self):
		return (len(self._map[0]), len(self._map))
		
	def __iter__(self):
		(mi, mj) = self.size()
		j = 0
		i = 0
		for j in range(0, mj):
			l = self._map[j]
			for i in range(0, mi):
				yield (l[i], vec(i, j))
		
		raise StopIteration
	
		
	
		
	



import operator


# for radar
RANDOM = 0
NEAREST = 1
ALL = 2


class IndexedList(object):
	def __init__(self):
		super(IndexedList, self).__init__()
		self._index_z = [[],[],[]]
		self._xs = []
		self._by_key = weakref.WeakValueDictionary()
		
	def append(self, x):
		self._index_z[x.z].append(x)
		self._xs.append(x)
		if hasattr(x, 'key'):
			self._by_key[x.key] = x
	
	def remove(self, x):
		self._index_z[x.z].remove(x)
		self._xs.remove(x)	
	
	def by_z(self, z):
		return iter(self._index_z[z])
		
	def __iter__(self):
		return iter(self._xs)
		
	def by_key(self, key):
		return self._by_key.get(key)
	
	
from types import FunctionType, MethodType

def test_dump():
	g = Game()
	g.update(0.01)
	print dump(g)
	assert 0

def fkw(d):
	return ', '.join(['{}={}'.format(k, dump(v)) for k,v in d.items()])
	
def fag(xs):
	return ', '.join([dump(v) for v in xs])

def dump(x, attrs=None, _vis=set()):
	if hasattr(x, 'dump'):
		return x.dump()
	
	elif type(x) in (dict,):
		return 'Dict({})'.format(fkw(x))
	
	elif type(x) in (list,):
		return 'List({})'.format(fag(x))
		
	elif type(x) in (dict, list, tuple, float, int, str, unicode):
		return repr(x)
		
	else:
		print '>>>', x
		t = dict()
		for k in x.__dict__:
			if attrs is not None and k in attrs:
				k_in_attrs = 1
			else:
				k_in_attrs = 1
								
			if k_in_attrs and not k.startswith('_'):
				v = getattr(x, k)
				if not type(v) == MethodType:
					t[k] = dump(v)
		ka = ', '.join(['{}={}'.format(k,v) for k,v in t.items()])
		return '{}({})'.format(x.__class__.__name__, ka)
		




class Env(object):
	
	def add(self, x):
		if hasattr(x, 'env'):
			x.env = self
		self.xs.append(x)
	
	def dump(self):
		self.map.dump()
	
	def __init__(self):
		super(Env, self).__init__()
		
		self.xs = IndexedList()
		self.map = Map('map/aaa.txt')
		
		self.pos = vec(0,0)
		self.dim = vec(*self.map.size()) * FIELD_DIM
					
		self.total_time = 0.0
		self.is_day = 1
		self.hour = DAY_TIME

		self.cc1 = Control()
		self.add(Truck(pos=vec(10,10), ctrl=self.cc1))
		self.add(Truck(pos=vec(40,20), ctrl=self.cc1))
		self.add(Manip(pos=vec(90,25), ctrl=self.cc1))
		self.add(Manip(pos=vec(0,0), ctrl=self.cc1))
		
		
		#self.append(Mutant(pos=vec(170, 320), ctrl=None))
		#self.append( Missile(pos=vec(300, 300), target=vec(10,10)) )

		self.cont = SpecContainer({energy: INF})
		self.cont.add(energy, 500)
		
		self.wind = 0.0
		self.solar = 0.0

		self.total_days = 1

		self.kill_list = []
		
		self.speed = 1.0
	
	
	def get_f(self, key, attr):
		who = self.xs.by_key(key)
		if who is None:
			raise Error('obj_not_found; key={0}'.format(key))
		else:
			if hasattr(who, attr):
				return getattr(who, attr)
			else:
				raise Error('type assertion failed')
			
	def send_order(self, act, args):
		# ctrl
		
		a = act
		if a in ['build', 'move', 'stop']:
			key = args[0]
			func = self.get_f(key, a)
			#print 'order recived', a, func, args[1:]
			func(*args[1:])
			return 'ok'
		
		else:
			raise Error('unknown order')
		
	
	def round_xy_by_ab(self, v):
		x = int(v.x)
		y = int(v.y)
		s = int(SMALL_SIZE.x)
		return s * vec(operator.div(x,s), operator.div(y,s))
	
	def ab_dim(self):
		return SMALL_SIZE
	
	
	def build(self, what_type, where):
		# where is x,y pos contained in a,b square where ab will be left-top square of new building
		
		x = what_type(env=self, pos=self.round_xy_by_ab(where), ctrl=self.cc1)
		self.append(x)
	
	def destroy(self, what):
		self.kill_list.append(what)

	
	def shoot(self, what):
		if what == None:
			print 'shoot to None??'
			return
			
		if what not in self:
			print 'shoot to non-existing target'
			return
	
		what.health -= 1
		if what.health <= 0:
			self.kill_list.append(what)
		
	

	# -------------------------
	def random_pos(self):
		w = self.dim
		x = random.randint(0, w.x)
		y = random.randint(0, w.y)
		return vec(x,y)


	
	def update(self, dt):
		dt *= self.speed
		
		global g_dt
		g_dt = dt
		
		self.total_time += dt
		
		self.hour -= dt
		
		if self.hour <= 0.0:
			if not self.is_day:
				self.total_days += 1
			
			self.is_day = not self.is_day
			if self.is_day:
				self.hour = DAY_TIME 
			else:
				self.hour = NIGHT_TIME
				
				#for x in range(0, 4*self.total_days):
				#	p = self.random_pos()
				#	self.append(Mutant(env=self, pos=p))
		
		self.cc1.update(dt)
		
		for x in self:
			x.update(dt)
			
			
		while self.kill_list:
			x = self.kill_list.pop()
			self.remove(x)
			
			
	# -------------------------
	def next_wave(self, num):
		for x in range(0, num):
			p = self.random_pos()
			self.append(Mutant(env=self, pos=p))
		
	
	def iter_objs_under_pos(self, pos, z=None):
		if z is None:
			zs = [2,1,0]
		else:
			zs = [z]
		
		for i in zs:
			for x in self.xs.by_z(i):
				if point_in_rect(pos, x.pos, x.end):
					yield x
					
						
					
		
		
	def radar_all(self, type=object):
		return (x for x in self if isinstance(x, type))
		
		
	# -------------------------
	def radar(self, how, object_type, arg=None):
		objs = []
						
		if how == RANDOM:
			objs = []
			
			for obj in self:
				if isinstance(obj, object_type):
					objs.append(obj)
			
			return random.choice(objs) if objs else None
		
		elif how == NEAREST:
			best = INF
			objs = [None]
			
			for obj in self:
				if isinstance(obj, object_type):
					d = dist(arg.center, obj.center)
					
					if d < best:
						best = d
						objs = [obj]
						
					elif d == best:
						objs.append(obj)
						
			return random.choice(objs)
			
		elif how == ALL:
			objs = []
			
			for obj in self:
				if isinstance(obj, object_type):
					objs.append(obj)
			
			return objs
		
		else:
			raise 'Error'
		
		


	# -------------------------
	def radar_anything(self):
		
		if len(self) > 0:
			return random.choice(self)
		
		return None

	def __iter__(self):
		return iter(self.xs)



Game = Env


