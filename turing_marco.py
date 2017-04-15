import import_trans
import machinerie
import re
from color import bcolors

class TM:
	def __init__(self, position, alphabet,raw_band,typx,taille):
		if typx == 'Symbole' :
			self.p = position
			self.a = alphabet
			self.t = self.bin_size()
			self.abin = self.alphabet_to_bin()
			self.nb_b = taille
			self.bande=[]
			self.bandebin=[]
			for i in range(self.nb_b) :
				self.bande.append(Band(raw_band[i],self.p,self.a))
				self.bandebin.append(self.bandesymtobin(i))
		if typx == 'Binaire' :
			self.p = position
			self.a = alphabet
			self.t = self.bin_size()
			self.abin = self.alphabet_to_bin()
			self.nb_b = taille
			for i in range(self.nb_b) :
				self.bandebin.append(Band(raw_band[i],self.p,self.a))
				self.bande.append(self.bandebintosym(i))

	def alphabet_to_bin (self) :
		x = 0
		alpha_code = []
		for i in self.a :
			alpha_code.append(get_bin(x,self.t))
			x+=1
		return alpha_code

	def bin_size (self) :
		i = 0
		while ( len(self.a) > 2**i) :
			i += 1
		return i

	def bandesymtobin (self,z) :
		new_band = ['begin']
		for i in self.bande[z].l[1:] :
			a = self.abin[self.a.index(i)]
			for char in a :
				new_band.append(char)
		position = len(new_band)
		a = self.abin[self.a.index(self.bande[z].h)]
		for char in a : 
			new_band.append(char)
		for i in self.bande[z].r[:-1] :
			a = self.abin[self.a.index(i)]
			for char in a :
				new_band.append(char)
		new_band.append('end')
		bandebin = Band(new_band,position,self.abin)
		return(bandebin)


	def bandebintosym (self,z) :
		new_band = ['begin']
		a = ''
		for i in self.bandebin[z].l[1:] : 
			a += i
			if len(a) % self.t == 0 :
				new_band.append(self.a[self.abin.index(a)])
				a=''
			
		position = len(new_band)
		a += self.bandebin[z].h
		if len(a) % self.t == 0 :
				new_band.append(self.a[self.abin.index(a)])
				a=''
		for i in self.bandebin[z].r[:-1] :
			a += i
			if len(a) % self.t == 0 :
				new_band.append(self.a[self.abin.index(a)])
				a=''
		new_band.append('end')
		if a != '' :  
			print("Probleme taille")
		bande = Band(new_band,position,self.a)
		return(bande)

def get_bin(x, n=0):
	return format(x, 'b').zfill(n)


class Band :
	def __init__ (self,raw_band,position,alphabet) :
		self.l = list(raw_band[:position])
		self.h = raw_band[position]
		self.r = list(raw_band[position+1:])
		self.a = alphabet 

	def gauche(self) :

		tmp = self.h
		self.h = self.l[-1]
		del(self.l[-1])
		self.r = [tmp] + self.r
		if self.l == ['begin'] :
			#Ajout d'un caractere vide si notre bande gauche est vide 
			self.l.append(self.a[0])
	
	def droite(self) :
		tmp = self.h
		self.h = self.r[0]
		del(self.r[0])
		self.l.append(tmp)
		if self.r == ['end'] :
			#Ajout d'un caractere vide si notre bande droite est vide
			self.r = [self.a[0]] + self.r

	def toutagauche(self) :
		tmp = self.l
		if len(tmp) > 1 :		
			self.l = ['begin']
			self.r = tmp[2:]+[self.h]+self.r
			self.h = tmp[1]
		else :
			print("Run impossible : on est deja au bout")
	
	
	def printe(self) :
		print("Bande Gauche : ",self.l," Tete : ",self.h," Bande Droite :",self.r)	


