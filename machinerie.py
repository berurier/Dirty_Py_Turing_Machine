import import_trans
from color import bcolors

class Etat :
	def __init__ (self,lt,mt) :
		self.courant = 'init'
		self.liste_trans = lt
		self.machine = mt
		self.etat_a_regarde = self.liste_trans.get_trans(self.courant)
		
	def machination_1 (self) :
		while (self.courant != 'accept' and self.courant != 'reject') :
			self.etat_a_regarde = self.liste_trans.get_trans(self.courant)
			etat_trouve = False
			for states in self.etat_a_regarde :
				#print (self.liste_trans.action)
				if  not etat_trouve and self.possible(states,0) :
					#print (self.courant,self.liste_trans.etat)
					self.courant = self.liste_trans.dep[states]
					self.ecriture(states,0)
					self.deplacement(states,0)
					#self.machine.bande[0].printe()
					etat_trouve = True
				if not etat_trouve and self.run(states,0)  :
					self.courant = self.liste_trans.dep[states]
					#self.machine.bande[0].printe()
					etat_trouve = True
					
			if not etat_trouve :
				print("Probleme Transition")
	def machination_2_bin (self) :
		while (self.courant != 'accept' and self.courant != 'reject') :
			self.etat_a_regarde = self.liste_trans.get_trans(self.courant)
			etat_trouve = False
			#self.Ecriture_Totale()
			for states in self.etat_a_regarde :
				if not etat_trouve :
					if self.mega_test(states,0) and self.mega_test(states,1) and self.mega_test_bin(states,0) and self.mega_test_bin(states,1):
						
						if self.possible(states,0) and self.possible_bin(states,0):
							self.ecriture(states,0)
							self.ecriture_bin(states,0)
							self.deplacement(states,0)
							self.deplacement_bin(states,0)
						else :
							if self.run_test(states,0)  :
								self.run(states,0) 
								self.run_bin(states,0)
						if self.possible(states,1) :
							self.ecriture(states,1)
							self.ecriture_bin(states,1)
							self.deplacement(states,1)
							self.deplacement_bin(states,1)
						else :
							if self.run_test(states,1)  :
								self.run(states,1)
								self.run_bin(states,1)
						self.courant = self.liste_trans.dep[states]
			etat_trouve = False
			if not self.comp_sym_bin() :
				print("Erreur : PAS MEME BANDES")


	def machination_n (self,n) :
		while (self.courant != 'accept' and self.courant != 'reject') :
			self.etat_a_regarde = self.liste_trans.get_trans(self.courant)
			etat_trouve = False
			multi_etat_trouve = [False]*n
			#self.Ecriture_Totale()
			for states in self.etat_a_regarde :
				if not etat_trouve :
					for num in range(self.liste_trans.nb) :
						if self.mega_test(states,num) :
							#self.machine.bande[num].printe()
							multi_etat_trouve[num] = True
						#else :
						#	print("Pas trouve")
							#print("FOUND",multi_etat_trouve)
				if sum(multi_etat_trouve) == self.liste_trans.nb :
					for num in range(self.liste_trans.nb) :
						if self.possible(states,num) :
							#print (self.courant,self.liste_trans.etat)
							
							self.ecriture(states,num)
							self.deplacement(states,num)
							#self.machine.bande[num].printe()
						if self.run_test(states,num)  :
							self.run(states,num)
							#self.machine.bande[num].printe()
					self.courant = self.liste_trans.dep[states]
				multi_etat_trouve = [False]*n
			etat_trouve = False

	def machination_n_bin (self,n) :
		while (self.courant != 'accept' and self.courant != 'reject') :
			self.etat_a_regarde = self.liste_trans.get_trans(self.courant)
			etat_trouve = False
			multi_etat_trouve = [False]*n
			for states in self.etat_a_regarde :
				if not etat_trouve :
					for num in range(self.liste_trans.nb) :
						if self.mega_test(states,num) and self.mega_test_bin(states,num) :
							multi_etat_trouve[num] = True
				if sum(multi_etat_trouve) == self.liste_trans.nb :
					print(bcolors.WARNING,"Machine : ",self.liste_trans.nom," Etat : ",self.courant,bcolors.ENDC)
					for num in range(self.liste_trans.nb) :
						if self.possible(states,num) and self.possible_bin(states,num) :
							
							self.ecriture(states,num)
							self.deplacement(states,num)
							self.ecriture_bin(states,num)
							self.deplacement_bin(states,num)
						if self.run_test(states,num)  :
							self.run(states,num)
							self.run_bin(states,num)
						print(bcolors.OKBLUE,"Bande symbole n",num+1,"Bande Gauche : ",bcolors.FAIL,self.machine.bande[num].l,bcolors.OKBLUE," Tete : ",bcolors.FAIL,self.machine.bande[num].h,bcolors.OKBLUE," Bande Droite :",bcolors.FAIL,self.machine.bande[num].r)
						print(bcolors.OKBLUE,"Bande binary n",num+1,"Bande Gauche : ",bcolors.FAIL,self.machine.bandebin[num].l,bcolors.OKBLUE," Tete : ",bcolors.FAIL,self.machine.bandebin[num].h,bcolors.OKBLUE," Bande Droite :",bcolors.FAIL,self.machine.bandebin[num].r)

					self.courant = self.liste_trans.dep[states]
				multi_etat_trouve = [False]*n
			etat_trouve = False
			if not self.comp_sym_bin() :
				print("Erreur : PAS MEME BANDES")

	def run_test (self,etat,n_boucle) :
		if "RUN" in self.liste_trans.action[etat][n_boucle][0] :
			return True
		else : 
			return False 	
	def nope_test (self,etat,n_boucle) :
		if "NOP" in self.liste_trans.action[etat][n_boucle][0] :
			return True 
		else :
			return False

	def run (self,etat,n_boucle) :
		if "RUN" in self.liste_trans.action[etat][n_boucle][0] :
			if self.liste_trans.action[etat][n_boucle][0][1] == 'left_most' :
				self.machine.bande[n_boucle].toutagauche()
				return True
			else :
				print ("Run a implementer")
				return True
		else :
			return False

	def run_bin (self,etat,n_boucle) :
		if "RUN" in self.liste_trans.action[etat][n_boucle][0] :
			if self.liste_trans.action[etat][n_boucle][0][1] == 'left_most' :
				self.machine.bandebin[n_boucle].toutagauche()
				return True
			else :
				print ("Run a implementer")
				return True
		else :
			return False
	def possible (self,etat,n_boucle) :

		if "NOP" in self.liste_trans.action[etat][n_boucle][0] :
			return False 
		if "RUN" in self.liste_trans.action[etat][n_boucle][0] :
			return False
		if "VAL" in self.liste_trans.action[etat][n_boucle][0] :
			#print("Regarder bande")
			if self.liste_trans.action[etat][n_boucle][0][1] == self.machine.bande[n_boucle].h :
				return True
			else :
				return False
		if "BUT" in self.liste_trans.action[etat][n_boucle][0] :
			#print("Regarder bande")
			if self.machine.bande[n_boucle].h not in self.liste_trans.action[etat][n_boucle][0][1] :
				return True
			else :
				return False
		if "OUT" in self.liste_trans.action[etat][n_boucle][0] :
			for letter in self.liste_trans.action[etat][n_boucle][0][1] :
				if self.machine.bande[n_boucle].h in letter :
					return False
			return True
		if "ANY" in self.liste_trans.action[etat][n_boucle][0] :
			#print ("On avance")
			return True
		else :
			#print("j'ai pas trouve")
			return False

	def possible_bin (self,etat,n_boucle) :
		
		if "NOP" in self.liste_trans.action[etat][n_boucle][0] :
			return False 
		if "RUN" in self.liste_trans.action[etat][n_boucle][0] :
			return False
		if "VAL" in self.liste_trans.action[etat][n_boucle][0] :
			#print("Regarder bande")
			if self.get_bin(self.liste_trans.action[etat][n_boucle][0][1]) == self.get_cur_bin(n_boucle) :
				return True
			else :
				return False
		if "BUT" in self.liste_trans.action[etat][n_boucle][0] :
			#print("Regarder bande")
			if self.get_cur_bin(n_boucle) not in self.get_bin(self.liste_trans.action[etat][n_boucle][0][1]) :
				return True
			else :
				return False
		if "OUT" in self.liste_trans.action[etat][n_boucle][0] :
			for letter in self.liste_trans.action[etat][n_boucle][0][1] :
				if self.get_cur_bin(n_boucle) in self.get_bin(letter) :
					return False
			return True
		if "ANY" in self.liste_trans.action[etat][n_boucle][0] :
			#print ("On avance")
			return True
		else :
			#print("j'ai pas trouve")
			return False

	def get_bin (self,symbole) :
		a = self.machine.a.index(symbole) 
		return self.machine.abin[a]

	def get_cur_bin (self,n_boucle) :
		a = self.machine.bandebin[n_boucle].h
		for i in range(self.machine.t-1) :
			a += self.machine.bandebin[n_boucle].r[i]
		return a

	def ecriture (self,etat,n_boucle) :
		try :
			if self.liste_trans.action[etat][n_boucle][1][0] == 'WRITE' :
				self.machine.bande[n_boucle].h = self.liste_trans.action[etat][n_boucle][1][1]
		except :
			print ("Erreur acces ecriture_sym")
	
	def ecriture_bin (self,etat,n_boucle) :
		try :
			if self.liste_trans.action[etat][n_boucle][1][0] == 'WRITE' :
				#print ("on peut ecrire")
				a=self.get_bin(self.liste_trans.action[etat][n_boucle][1][1])
				self.machine.bandebin[n_boucle].h = a[0]
				for i in range(self.machine.t-1) :
					self.machine.bandebin[n_boucle].r[i]=a[i+1]
		except :
			print ("Erreur acces ecriture_bin")

	def deplacement (self,etat,n_boucle) :
		try :
			if "Here" in self.liste_trans.action[etat][n_boucle][2]  :
				on_bouge_pas=True
				#print ("on bouge pas")
			elif "Right" in self.liste_trans.action[etat][n_boucle][2]  :
				#print("DROITE")
				self.machine.bande[n_boucle].droite()
			elif "Left" in self.liste_trans.action[etat][n_boucle][2]  :
				#print("GAUCHE")
				self.machine.bande[n_boucle].gauche()
			else :
				print("Erreur ou variable ?")

		except :
			print("Erreur acces dep")			

	def deplacement_bin(self,etat,n_boucle) :
		try :
			if "Here" in self.liste_trans.action[etat][n_boucle][2]  :
				on_bouge_pas=True
			elif "Right" in self.liste_trans.action[etat][n_boucle][2] :
				#print("DROITE")
				for i in range (self.machine.t) : 
					self.machine.bandebin[n_boucle].droite()
			elif "Left" in self.liste_trans.action[etat][n_boucle][2] :
				#print("GAUCHE")
				for i in range (self.machine.t) : 
				
					self.machine.bandebin[n_boucle].gauche()
			else :
				print(self.liste_trans.action[etat][n_boucle][2],"Erreur ou variable ?")

		except :
			print("Erreur acces dep")		

	def Ecriture_Totale (self) :
		print("Etat Courant : ",self.courant)
		for i in self.etat_a_regarde :
			print("Transition : ",i," Les Transitions : ",self.liste_trans.action[i]," L'etat suivant : ",self.liste_trans.dep[i])
		for j in self.machine.bande :
			j.printe()

	def mega_test (self,states,n) :
		return (self.possible(states,n) or self.run_test(states,n) or self.nope_test(states,n))
	def mega_test_bin (self,states,n) :
		return (self.possible_bin(states,n) or self.run_test(states,n) or self.nope_test(states,n))

	def comp_sym_bin(self) :
		for i in range(self.machine.nb_b) :

			
			a = self.machine.bandesymtobin(i)
			
			b = self.machine.bandebin[i]

			if self.bande_diff(a,b) :
				return False
			c = self.machine.bandebintosym(i)
			
			d = self.machine.bande[i]

			if self.bande_diff(c,d) :
				return False
		return True
	def bande_diff(self,a,b) :
		if a.r == b.r :
			if a.l == b.l :
				if a.h == b.h :
					return False
		return True
