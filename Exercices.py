#! /usr/bin/python3.5
#-*- coding:utf-8 -*

from tkinter import *
from additions import *

class Menu():

	def __init__(self):

		self.root = Tk()

		self.root.config(bg='light blue')

		self.root.bind('<Escape>',self.quit)

		self.aff = Label()												# Affichage

		self.entree = Entry(self.root, width = 50)						# Champ de saisie
		self.entree.config(font=("courier",30,"bold"))

		self.accueil()

		self.root.mainloop()


	def accueil(self):

		"""Accueil et demande de saisie du nom du joueur"""

		self.aff.destroy()												# Affichage
		self.aff = Label(self.root,text = "Quel est ton nom ?")
		self.aff.config(font=("courier",30,"bold"), bg='light blue')
		self.aff.config(height=6, width=50)
		self.aff.grid(row=1,column=1)

		self.entree.grid(row=2,column = 1)								# Création du champ de saisie
		self.entree.focus_force()

		self.root.bind('<Return>',self.choix_exo)

	def choix_exo(self, *event):

		self.name = self.entree.get()									# Enregistrement du nom
		self.name = self.name.capitalize()

		self.entree.grid_forget()

		self.difficulte = Scale(self.root, label="Difficultée", from_=3, to=1, length=300, width=30,bg='light blue')
		self.vitesse = Scale(self.root, label="Vitesse", from_=10, to=1, length=300, width=30,bg='light blue')


		self.bou1 = Button(self.root,text="Additions", command=self.lancer_addition)
		self.bou2 = Button(self.root,text="Soustractions", command=self.lancer_soustraction)
		self.bou3 = Button(self.root,text="Multiplications", command=self.lancer_multiplication)
		self.bou4 = Button(self.root,text="Divisions", command=self.lancer_division)

		self.bou1.config(height=3, width=15, bg='light green', font=40)
		self.bou2.config(height=3, width=15, bg='light green', font=40)
		self.bou3.config(height=3, width=15, bg='light green', font=40)
		self.bou4.config(height=3, width=15, bg='light green', font=40)

		self.aff.destroy()
		self.aff = Label(self.root,text = "Bonjour {}. Quel exercice veux-tu travailler ?".format(self.name))
		self.aff.config(font=("courier",30,"bold"),bg='light blue')
		self.aff.config(height=6, width=60)



######## Organisation ##########


		self.aff.grid(row=1,column=1,columnspan=4)

		self.bou1.grid(row=3,column=1)
		self.bou2.grid(row=3,column=2)
		self.bou3.grid(row=3,column=3)
		self.bou4.grid(row=3,column=4)

		self.difficulte.grid(row=1,column=5,rowspan=3)
		self.vitesse.grid(row=1,column=6,rowspan=3)

		
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

	def quit(self,*event):

		self.root.destroy()


		

if __name__ == "__main__":
	a = Menu()