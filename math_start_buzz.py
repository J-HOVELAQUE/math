#! /usr/bin/python3.5
# -*- coding : utf-8 -*


from random import randrange
from tkinter import *
import time
import threading
import pickle
from datetime import date
from serial import Serial


class Menu():

	def __init__(self,name=""):

		
		self.name = name
		self.root = Tk()

		self.root.config(bg='light blue')

		self.root.bind('<Escape>',self.quit)

		self.aff = Label(self.root)												# Affichage
		self.aff.config(font=("courier",30,"bold"), bg='light blue')
		self.aff.config(height=6, width=60)
		self.aff.grid(row=1,column=1,columnspan=4)

		self.entree = Entry(self.root, width = 50)						# Champ de saisie
		self.entree.config(font=("courier",30,"bold"))

		if self.name == "" :
			self.accueil()
		else:
			self.choix_exo()

		self.root.mainloop()


	def accueil(self):

		"""Accueil et demande de saisie du nom du joueur"""

														# Affichage
		self.aff.config(text = "Quel est ton nom ?")
		

		self.entree.grid(row=2,column = 1,columnspan=4)								# Création du champ de saisie
		self.entree.focus_force()

		self.root.bind('<Return>',self.enregistrer_nom)

	def enregistrer_nom(self, *event):

		self.name = self.entree.get()									# Enregistrement du nom
		self.name = self.name.capitalize()
		self.choix_exo()


	def choix_exo(self):

		
		self.entree.grid_forget()

		self.aff.config(font=("courier",30,"bold"), bg='light blue')
		self.aff.config(height=6, width=60)

		self.difficulte = Scale(self.root, label="Difficultée", from_=3, to=1, length=300, width=30,bg='light blue')
		self.vitesse = Scale(self.root, label="Vitesse", from_=10, to=1, length=300, width=30,bg='light blue')


		self.bou1 = Button(self.root,text="Additions", command=self.lancer_addition)
		self.bou2 = Button(self.root,text="Soustractions", command=self.lancer_soustraction)
		self.bou3 = Button(self.root,text="Multiplications", command=self.lancer_multiplication)
		self.bou4 = Button(self.root,text="Divisions", command=self.lancer_division)
		self.bou5 = Button(self.root,text="Scores", command=self.hi_scores)

		

		self.bou1.config(height=3, width=15, bg='light green', font=40)
		self.bou2.config(height=3, width=15, bg='light green', font=40)
		self.bou3.config(height=3, width=15, bg='light green', font=40)
		self.bou4.config(height=3, width=15, bg='light green', font=40)
		self.bou5.config(height=3, width=15, bg='light green', font=40)
		

		self.aff.config(text="Bonjour {}. Quel exercice veux-tu travailler ?".format(self.name))



######## Organisation ##########


		self.aff.grid(row=1,column=1,columnspan=4)

		self.bou1.grid(row=3,column=1,pady=10)
		self.bou2.grid(row=3,column=2,pady=10)
		self.bou3.grid(row=3,column=3,pady=10)
		self.bou4.grid(row=3,column=4,pady=10)
		self.bou5.grid(row=3,column=5,columnspan=2,pady=10)
		

		self.difficulte.grid(row=1,column=5,rowspan=2,pady=10)
		self.vitesse.grid(row=1,column=6,rowspan=2,pady=10)

		
######## Lancer un exercice à l'aide d'un bouton #############



	def lancer_addition(self):

		"""Lance une séance d'additions"""

		diff=self.difficulte.get()
		vit=self.vitesse.get()		
		self.root.destroy()
		exo = TableAdditions(self.name,diff,vit)

	def lancer_soustraction(self):

		"""Lance un séance de soustractions"""

		diff=self.difficulte.get()
		vit=self.vitesse.get()		
		self.root.destroy()
		exo = TableSoustractions(self.name,diff,vit)

	def lancer_multiplication(self):

		"""Lance un séance de multiplications"""

		diff=self.difficulte.get()
		vit=self.vitesse.get()		
		self.root.destroy()
		exo = TableMultiplications(self.name,diff,vit)

	def lancer_division(self):

		"""Lance un séance de divisions"""

		diff=self.difficulte.get()
		vit=self.vitesse.get()		
		self.root.destroy()
		exo = TableDivisions(self.name,diff,vit)


	def hi_scores(self):



		self.tables = ["additions","soustractions","multiplications","divisions"]
		self.indice = 0

		self.bou1.grid_forget()
		self.bou2.grid_forget()
		self.bou3.grid_forget()
		self.bou4.grid_forget()
		self.bou5.grid_forget()
		

		self.difficulte.grid_forget()
		self.vitesse.grid_forget()
		
		self.aff.config(font=("courier",20,"bold"),bg="light blue")
		self.aff.config(height=30, width=50)
		

		self.temps=MyTimer(3.00,self.affichage_scores)

		self.affichage_scores()
		self.temps.start()



	def affichage_scores(self):

		
		if self.indice < 4:
			try:												# Importer les scores
				with open(self.tables[self.indice],"rb") as fichier:
					lecture = pickle.Unpickler(fichier)
					resultat = lecture.load()
			except FileNotFoundError:
				resultat = []

			self.message ="Meilleurs score pour les {} :\n\n".format(self.tables[self.indice])

			for i, valeur in enumerate(resultat):
				self.message = self.message + "\n{} : {} score = {}".format(i+1, valeur[0], valeur[1])

			print(self.message)

			
		

			self.rafraichir()

			self.indice +=1

		else:
			self.choix_exo()
			self.temps.stop()

	def rafraichir(self):

		self.aff.config(text=self.message)
		


	def quit(self,*event):

		self.root.destroy()




class TableAdditions(object):

	"""Un séance d'addition avec interface graphique"""

	def __init__(self,name,difficulte=1,vitesse=5,exo="additions"):

		self.name = name
		self.ard = Serial('COM3',9600)
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
			self.entree.grid(row=1,column=2,padx=10)
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
				self.ard.write(bytes("buzzGagne",'UTF-8'))
				self.bonnes_reponses += 1
				self.mise_a_jour()

			elif self.gagne is False:
				self.message="Perdu"
				self.ard.write(bytes("buzzPerdu",'UTF-8'))
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

		self.root.bind('<Return>',self.fin)

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

	def fin(self, *event):

		"""Propose de rejouer"""

		self.aff.destroy()
		self.aff = Label(self.root,text = "Veux-tu-rejouer ?")
		self.aff.config(font=("courier",30,"bold"),bg='light blue')
		self.aff.config(height=3, width=50)
		self.aff.grid(row=1,column=1,columnspan=2)

		self.bou1 = Button(self.root,text="OUI", command=self.rejouer)
		self.bou2 = Button(self.root,text="NON", command=self.quit)

		self.bou1.config(height=3, width=15, bg='light green', font=40)
		self.bou2.config(height=3, width=15, bg='light green', font=40)

		self.bou1.grid(row=2,column=1)
		self.bou2.grid(row=2,column=2)

	def rejouer(self):

		self.root.destroy()
		self.temps.stop()
		a=Menu(self.name)

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
        
	a = Menu()
