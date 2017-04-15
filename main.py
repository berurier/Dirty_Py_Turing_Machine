import import_trans
import machinerie
import turing_marco
from color import bcolors

# Ceci est une implementation de Machine de Turing en Python.

# REGLES POUR LES ALPHABETS
# 1er element  Element VIDE ( Carre ) 

# REGLES POUR LES BANDES 
# Commence par 'begin'
# Termine par 'end'
# Liste de listes

# REGLES POUR LES TRANSITIONS :
# Entre {}
# name : Champ nom
# nb_bands : Par defaut a 1
# Si plusieurs bandes, separer les differentes transitions par ;
# Transitions : comme dans les exemples
# Peut bugger pour des machines à plus de deux bandes.


#XOR
alphabet=['Carre','U','Z','B','test']
position = 2
bandidos=[['begin','U','Z','U','Z','Z','Z','B','Z','end'],['begin','U','Z','U','Z','U','Z','U','Z','U','Z','Z','Z','end']]
nb_bandes = 2 
typ = 'Symbole'
fichier_transition = 'xor'



print(bcolors.OKGREEN,"Bienvenue dans le Turing_Machine_Simulator v-1 \n Decommentez le main pour changer les machines",bcolors.ENDC)

machine=turing_marco.TM(position,alphabet,bandidos,typ,nb_bandes)
transition=import_trans.Transition(fichier_transition)
fonctionnement=machinerie.Etat(transition,machine)

fonctionnement.machination_n_bin(nb_bandes)

