#! /usr/bin/python3.5
# -*- coding:utf-8 -*

from random import randrange
from tkinter import *
import time
import threading
import pickle
from datetime import date

class TableAdditions(object):

	"""Un séance d'addition avec interface graphique"""

	def __init__(self,name,difficulte=1,vitesse=5,exo="additions"):

		self.name = name
		self.difficulte = difficulte
		self.vitesse = vitesse

		self.exo = exo

		self.pulse = 0										# Compteur pour le timer
		self.numero = 1 									# Compteur de questions
		self.bonnes_reponses = 0							# Nombre de bonnes réponses
		self.temps = MyTimer(1.0,self.tictac)				# Création du timer
		self.gagne = False

		try:												# Importer les scores
			with open(self.exo,"rb") as fichier:
				lecture = pickle.Unpickler(fichier)
				self.resultat = lecture.load()
		except FileNotFoundError:
			self.resultat = []


		#################################
		#								#
		#	Création de l'interface  	#
		#								#
		#################################



		self.root = Tk()
		self.root.config(bg='light blue')
		self.root.bind("<Escape>",self.quit)							# Interface

		self.root.title("Exercice")										# Titre
		
		self.aff = Label()												# Affichage
		self.aff = Label(self.root,text = "Est-tu prêt(e)s {}".format(self.name))
		self.aff.config(font=("courier",30,"bold"),bg='light blue')
		self.aff.config(height=6, width=60)
		self.aff.grid(row=1,column=1)


		self.entree = Entry(self.root, width = 3)						# Champ de saisie
		self.entree.config(font=("courier",100,"bold"))


		self.root.focus_force()
		self.root.bind('<Return>',self.choisir_une_operation)


		self.root.mainloop()



	def choisir_une_operation(self,*event):

		"""Selectionne deux chiffre en vue de les additionner et affiche l'opération"""


		if self.numero <= 20:

			self.entree.delete(0,len(self.entree.get()))
			self.entree.grid(row=1,column=2)
			self.entree.focus_force()

			self.operande1 = randrange(1,10**self.difficulte+1)
			self.operande2 = randrange(1,10**self.difficulte+1)

			self.mettre_en_forme()
			self.mise_a_jour()
			
			self.root.bind('<Return>',self.lire_le_resultat)
			self.temps.start()

		else:

			self.afficher_resultat()


	def mettre_en_forme(self):

		self.message = "{} + {} = ".format(self.operande1,self.operande2)

	def lire_le_resultat(self,*event):

		"""Interprète le résultat donné"""

		self.temps.stop()
		self.pulse = 0
		self.numero +=1
		self.gagne = False

		self.entree.grid_forget()
		
		self.root.bind('<Return>',self.choisir_une_operation)
		self.prop = self.entree.get()

		try:

			self.prop = int(self.prop)
			self.validation()

			if self.gagne is True:
				self.message="Gagné"
				self.bonnes_reponses += 1
				self.mise_a_jour()

			elif self.gagne is False:
				self.message="Perdu"
				self.mise_a_jour()

		except ValueError:

			self.message = "??????"
			self.mise_a_jour()

	def validation(self):

		"""Vérifie que le résultat est juste"""

		if self.prop == self.operande1+self.operande2:
			self.gagne = True
		

	def tictac(self):

		"""Pour gérer le timer"""

		self.pulse += 1

		if self.pulse == 11 - self.vitesse:
			self.lire_le_resultat()


	def afficher_resultat(self):

		"""Donne le résultat de la séance"""

		self.entree.grid_forget()

		if self.bonnes_reponses < 6:
			self.appreciation = "C'est nul !"

		elif 6 <= self.bonnes_reponses < 11:
			self.appreciation = "Pas terrible"

		elif 11 <= self.bonnes_reponses < 15:
			self.appreciation = "Pas mal"

		elif 15 <= self.bonnes_reponses < 20:
			self.appreciation = "C'est bien"

		elif self.bonnes_reponses == 20:
			self.appreciation = "Excellent !!"

		self.message = "Bonnes réponses : {}\n{}".format(self.bonnes_reponses,self.appreciation)
		self.aff.destroy()
		self.aff = Label(self.root,text = self.message)
		self.aff.config(font=("courier",20,"bold"),bg='light blue')
		self.aff.config(height=20, width=40)
		self.aff.grid()

		self.root.bind('<Return>',self.mise_en_forme_score)


	def mise_en_forme_score(self,*event):

		"""Genère la table des scores"""

		today = date.today()

		libelle = "{} le {} {} {}".format(self.name,today.day,today.month,today.year)
		self.resultat.append((libelle, self.bonnes_reponses*(self.vitesse+self.difficulte*3)))
		self.resultat = sorted(self.resultat, key = lambda colonnes: colonnes[1])

		self.resultat.reverse()

		if len(self.resultat) > 10:
			del self.resultat[10:]

		self.message ="Meilleurs score pour les {} :\n\n".format(self.exo)

		for i, valeur in enumerate(self.resultat):
			self.message = self.message + "\n{} : {} score = {}".format(i+1, valeur[0], valeur[1])		

		self.aff.destroy()
		self.aff = Label(self.root,text = self.message)
		self.aff.config(font=("courier",20,"bold"),bg="light blue")
		self.aff.config(height=30, width=50)
		self.aff.grid()

		self.enregistrer_scores()

		self.root.bind('<Return>',self.quit)

	def enregistrer_scores(self):

		"""Enregistre les scores"""

		with open(self.exo,"wb") as fichier:
			enregistrement = pickle.Pickler(fichier)
			enregistrement.dump(self.resultat)

		

	def mise_a_jour(self):

		"""Met l'affichage à jour"""

		self.aff.destroy()
		self.aff = Label(self.root,text = self.message)
		self.aff.config(font=("courier",100,"bold"),bg='light blue')
		self.aff.config(height=3, width=13)
		self.aff.grid(row=1,column=1)

	def quit(self,*event):

		self.root.destroy()
		self.temps.stop()



		#########################################################
		#														#
		#		Classes dérivées pour d'autres opérations		#
		#														#
		#########################################################



class TableSoustractions(TableAdditions):

	def __init__(self,name,difficulte,vitesse):

		TableAdditions.__init__(self,name,difficulte,vitesse,"soustractions")

	def mettre_en_forme(self):


		if self.operande1 < self.operande2:
				self.operande1, self.operande2 = self.operande2, self.operande1

		self.message = "{} - {} = ".format(self.operande1,self.operande2)


	def validation(self):

		if self.prop == self.operande1-self.operande2:
			self.gagne = True





class TableMultiplications(TableAdditions):

	def __init__(self,name,difficulte,vitesse):

		TableAdditions.__init__(self,name,difficulte,vitesse,"multiplications")


	def mettre_en_forme(self):


		self.message = "{} X {} = ".format(self.operande1,self.operande2)


	def validation(self):

		if self.prop == self.operande1*self.operande2:
			self.gagne = True





class TableDivisions(TableAdditions):

	def __init__(self,name,difficulte,vitesse):

		TableAdditions.__init__(self,name,difficulte,vitesse,"divisions")


	def mettre_en_forme(self):


		self.message = "{} / {} = ".format(self.operande1*self.operande2,self.operande2)


	def validation(self):

		if self.prop == self.operande1:
			self.gagne = True








class MyTimer:

	"""Le timer utilisé pour les exercices de Math Heloise"""

	def __init__(self,tempo,target,args=[]):

		self._tempo = tempo
		self._target = target
		self._args = args

	def _run(self):

		self._timer = threading.Timer(self._tempo,self._run)
		self._timer.start()
		self._target(*self._args)

	def start(self):

		self._timer = threading.Timer(self._tempo,self._run)
		self._timer.start()

	def stop(self):

		self._timer.cancel()



if __name__ == "__main__":

	exo = TableAdditions()
