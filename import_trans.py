import re
from color import bcolors
class Transition : 
	def __init__(self, nomfichier) :
		self.open_fich(nomfichier)


	def parsing_action (self,etat2,j,id_etat) :
		#print(j,id_etat)
		if 'ANY' in etat2[0+3*j] :
			#print("ANY")
			self.action[id_etat][j].append("ANY")
		elif 'BUT' in etat2[0+3*j] :
			#print("But")
			val=etat2[0+3*j].split("BUT")[1].split(")")[0].replace(" ","")
			self.action[id_etat][j].append(["BUT",val])
			if val not in self.variables :
				self.variables.append(val)
		elif 'VAL' in etat2[0+3*j] :
			#print("Val")
			val=etat2[0+3*j].split("VAL")[1].split(")")[0].replace(" ","")
			self.action[id_etat][j].append(["VAL",val])
			if val not in self.variables :
				self.variables.append(val)
		elif 'OUT' in etat2[0+3*j] :
			goal = etat2[0+3*j].split("[")[1].split("]")[0].split("-")
			self.action[id_etat][j].append(["OUT",goal])
			for var in goal :
				if var not in self.variables :
					self.variables.append(var)		
		else :
			print("CA NE DEVRAIT PAS ARRIVER - ACTION INCONNUE")	
		if etat2[1+3*j] == "No_Write" : 
			#print(etat2[1+3*j])
			self.action[id_etat][j].append(etat2[1+3*j])
		else :
			val = etat2[1+3*j].split(" ")[1]
			self.action[id_etat][j].append(["WRITE",val])
			if val not in self.variables :
				self.variables.append(val)
		direction = etat2[2+3*j].split(')')[0]
		self.action[id_etat][j].append(direction)


	def open_fich (self,nomfichier) :
		fichiertransition = open(nomfichier,'r')
		stri = ''
		for i in fichiertransition :
			z = i.replace('\n',' ')
			z = re.sub('(OUT.*?);', '\\1-', z)
				
			stri+=z


		parser = stri.split(';')
		#print(parser)
		position = 0
		nombre = 1
		if 'nb_bands' in parser[position] :
			nombre=parser[position].split("=")[1]
			nombre=nombre.split(";")[0]
			nombre=int(nombre)
			position += 1
			#print(nombre)
		self.nb=nombre
	

		if 'name' in parser[position] :
			name=parser[position].split("=")[1]
			name=name.split('"')[1]
			position += 1
			#print(name)
			self.nom=name
		parser[position]=parser[position].split('=')[1]
		tab_trans=[]
		if nombre > 1 :
			for i in range(position,len(parser)) :
				if (i-position)%nombre == 0 :
					tab_trans.append(parser[i])
				else :
					tab_trans[-1]+=','+parser[i]


		else :
			for i in range(position,len(parser)) :
				tab_trans.append(parser[i])
		self.action=[]
		self.etat=[]
		self.dep=[]
		self.dual_band={}
		self.variables=[]
		#TODO :reedlepee
		# Reconnaissance mode de Run.
		# Rangement des etats et de leurs types
		# Multibande dans le main
		# Gestion des multibande pour les etats, notamment les cas relous. 
		k = 0
		#print(tab_trans)
		for i in tab_trans :
			
			etat=i.split(', ')
			#print(i)
			#print(etat[0].split('(')[1])
			self.etat.append(etat[0].split('(')[1])
			self.dep.append(etat[-1].split(')')[0])
			etat2=etat[1:-1]
			#print("taille :",len(etat2)," chaine : ",etat2)
			if "Simultaneous" in etat2[0] :
				self.dual_band[i]='Simultaneous'
			if "Parallel" in etat2[0] :
				self.dual_band[i]="Parallel"
			
			self.action.append([])
			for l in range (self.nb) :
				self.action[k].append([])
			if len(etat2) == 3*nombre :
				for j in range(nombre) :
					self.parsing_action(etat2,j,k)
			else :
		# 3/4 Bandes pas pris en compte dans tout les cas
		# SEQ pas pris en compte non plus
		# Pas bonne transition en dual band si on vire le premier element. 
				good = 0
				savior = 0
				etat3 = list(etat2)
				for j in range(nombre) :
					#print(j,etat2)
					#print(good+j)
					if "Nop" in etat2[good+j] :	
						#print("nop")
						
						del(etat3[savior])
						savior -= 1
						self.action[k][j].append("NOP")
						#etat2=['','','']+etat2
					elif "Run" in etat2[good+j] :
						#print("run")
						run=etat2[j].split('(')[1].split(')')[0]
						self.action[k][j].append(["RUN",run])
						if run not in self.variables :
							self.variables.append(run)
						del(etat3[savior])
						savior -= 1
					elif "Match" in etat2[good+j] :
						#print(etat2)
						self.parsing_action(etat3,j,k)
						good += 2
					savior += 1
			k+=1

	def get_trans (self,nom) :
		liste_state = []
		for i in range(len(self.action)) :
			if nom == self.etat[i] :
				liste_state.append(i)
		if liste_state == [] :
			print(" LISTE VIDE, ERREUR" )
		return liste_state


		
