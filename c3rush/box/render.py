# coding: utf-8
""" Ten plik definiuje przyjete zaleznosci miedzy zawartoscia a geometria boxow.
I dodaje troche interakcji.
"""

from engine import G, Vector as vec, Color3 as c, Image as Img



"""
box moze zawierac:
* obiekt z metoda renderujaca rblit

* obrazek?
* text (pango)?

przyjmujemy ze box MUSI byc wiekszy lub rowny od swojej zawartosci

box z obrazkiem to taki box z pustym textem

styl - element graficzny ktorego renderowanie zalezy od geometrii boxa
	czyli border, kolor tla, obrazek tla, obrazek rozciagniety do rozmiarow boxa
	
fazy:
	do boxow wkladamy content(placeholdery) z ktorych geometria bierze rozmiary minimalne
		czyli content musi wiedziec jaki jest rozmiar jego rendera
	geometria przelicza sie
	renderuja sie style (moga sie cachowac)
	mozna wyswietlac

content - wszystko co posiada dim i rblit
	
"""


class Box(object):
	def __init__(self, **kwargs):
		self.display = kwargs.pop('display', 1)
		assert not kwargs, kwargs
		super(Box, self).__init__(**kwargs)
			
	def rblit(self, to):
		if self.border and self.display == 1:
			to.draw_rect(self.pos, self.dim, (0.5,0.5,0.5), 1)
		

class PBox(Box):
	def rblit(self, to):
		Box.rblit(self, to)
		for b in self.childs:
			b.rblit(to)	


class CBox(Box):
	def rblit(self, to):
		if self.content:
			self.content.rblit(to, self.pos)
		
		Box.rblit(self, to)
		
class TextBox(Box):
	def __init__(self, **kwargs):
		self.__font = kwargs.pop('font')
		self.__text = kwargs.pop('text')
		self.content = self.__font.render(self.__text)		
		
		super(TextBox, self).__init__(**kwargs)
			
	def set_text(self, text):
		self.__text = text
		self.content = self.__font.render(text)		
	
	def get_text(self, text):
		return self.__text
	
	def rblit(self, to):
		if self.content:
			self.content.rblit(to, self.pos)
		
		Box.rblit(self, to)				
			
class VBox(PBox):
	pass

class GridBox(PBox):
	pass





