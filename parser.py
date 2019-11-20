#!/usr/bin/env python
# coding: utf-8

import sys
import io
import webbrowser, os
import base64
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from decimal import Decimal

def main(argv):
	longueurTotale = 0
	nombreMots = 0
	motLePlusLong = 0
	motLePlusCourt = 9999
	longueurMots = 15 * [0]
	motsLettres = 0
	motsChiffre = 0
	motsSpecial = 0
	lettresEtChiffres = 0
	lettresEtSpecial = 0
	chiffresEtSpecial = 0
	lettresEtChiffresEtSpecial = 0
	uppercases = 0
	uppercasesFirst = 0
	chars = defaultdict(int)
	motsContenantChar = defaultdict(int)

	with open(argv[0], 'r') as fichier:
		lignes = fichier.read().split('\n')

		for ligne in lignes:
			if len(ligne) > 0:
				### On compte les mots et leur longueur (pour la moyenne)
				nombreMots += 1
				longueurTotale += len(ligne)

				### On stocke le mot le plus long et le mot le plus court
				if len(ligne) > motLePlusLong:
					motLePlusLong = len(ligne)
				if len(ligne) < motLePlusCourt:
					motLePlusCourt = len(ligne)

				### On compte les mots d'une certaine taille
				if len(ligne) > 14:
					longueurMots[14] += 1
				else:
					longueurMots[len(ligne)] += 1

				### On initialise les booléens à false pour l'opération ci-dessous
				aLettre = False
				aChiffre = False
				aSpecial = False
				aMaj = False
				
				### On regarde si le mot contient une lettre, un chiffre, un caractère spécial ou une majuscule
				for char in ligne:
					chars[char] += 1 #
					if char.isalpha():
						aLettre = True
					if char.isdigit():
						aChiffre = True
					if char.isalpha():
						aLettre = True
					if not char.isalpha() and not char.isdigit():
						aSpecial = True
					if char.isalpha() and char.isupper():
						aMaj = True
				
				### Selon ce que le mot contient, on incrémente les variables de comptage
				if aLettre and not aChiffre and not aSpecial:
					motsLettres += 1
				if not aLettre and aChiffre and not aSpecial:
					motsChiffre += 1
				if not aLettre and not aChiffre and aSpecial:
					motsSpecial += 1
				if aLettre and aChiffre and not aSpecial:
					lettresEtChiffres += 1
				if aLettre and not aChiffre and aSpecial:
					lettresEtSpecial += 1
				if not aLettre and aChiffre and aSpecial:
					chiffresEtSpecial += 1
				if aLettre and aChiffre and aSpecial:
					lettresEtChiffresEtSpecial += 1
				if aMaj:
					uppercases += 1
					if ligne[0].isupper():
						uppercasesFirst += 1

				### On incrémente motsContenantChar pour savoir combien de mots contiennent un certain char
				for lettre in chars:
					if lettre in ligne:
						motsContenantChar[lettre] += 1

	### Affichage
	print("\tStatistiques de base\n")

	print("Nombre de mots    : " + str(nombreMots))
	print("Taille moyenne    : " + str(round(Decimal(float(longueurTotale) / nombreMots), 2)))
	print("Mot le plus long  : " + str(motLePlusLong))
	print("Mot le plus court : " + str(motLePlusCourt))

	print("\n\tMots contenant\n")

	print("Lettres only  : " + str(motsLettres) + " (" + str(round(Decimal(motsLettres / float(nombreMots) * 100), 2)) + "%)")
	print("Chiffres only : " + str(motsChiffre) + " (" + str(round(Decimal(motsChiffre / float(nombreMots) * 100), 2)) + "%)")
	print("Spéciaux only : " + str(motsSpecial) + " (" + str(round(Decimal(motsSpecial / float(nombreMots) * 100), 2)) + "%)\n")

	print("Lettres + chiffres  : " + str(lettresEtChiffres) + " (" + str(round(Decimal(lettresEtChiffres / float(nombreMots) * 100), 2)) + "%)")
	print("Lettres + special   : " + str(lettresEtSpecial) + " (" + str(round(Decimal(lettresEtSpecial / float(nombreMots) * 100), 2)) + "%)")
	print("Chiffres + special  : " + str(chiffresEtSpecial) + " (" + str(round(Decimal(chiffresEtSpecial / float(nombreMots) * 100), 2)) + "%)")
	print("Lett + chiff + spec : " + str(lettresEtChiffresEtSpecial) + " (" + str(round(Decimal(lettresEtChiffresEtSpecial / float(nombreMots) * 100), 2)) + "%)\n")

	print("Majuscule(s)        : " + str(uppercases) + " (" + str(round(Decimal(uppercases / float(nombreMots) * 100), 2)) + "%)")
	print("Majuscule au debut  : " + str(uppercasesFirst) + " (" + str(round(Decimal(uppercasesFirst / float(nombreMots) * 100), 2)) + "%)")

	print("\n\tMots de taille\n")

	for i in range(len(longueurMots)):
		if i != 0:
			if i < 10:
				print(str(i) + "   : " + str(longueurMots[i]) + " (" + str(round(Decimal(longueurMots[i] / float(nombreMots) * 100), 2)) + "%)")
			elif i == 14:
				print(str(i) + "+ : " + str(longueurMots[i]) + " (" + str(round(Decimal(longueurMots[i] / float(nombreMots) * 100), 2)) + "%)")
			elif i >= 10:
				print(str(i) + "  : " + str(longueurMots[i]) + " (" + str(round(Decimal(longueurMots[i] / float(nombreMots) * 100), 2)) + "%)")

	print("\n\tOccurences des lettres\n")

	for lettre in sorted(chars, key = chars.get, reverse = True):
		print(lettre + " : " + str(chars[lettre]) + " (" + str(motsContenantChar[lettre]) + " mots / " + str(round(Decimal(chars[lettre] / float(motsContenantChar[lettre])), 2)) + " par mot)")
	
	printHTML( longueurTotale, 
	nombreMots, 
	motLePlusLong, 
	motLePlusCourt,
	longueurMots,
	motsLettres, 
	motsChiffre, 
	motsSpecial, 
	lettresEtChiffres, 
	lettresEtSpecial, 
	chiffresEtSpecial, 
	lettresEtChiffresEtSpecial,
	lettre,
	chars,
	motsContenantChar)

def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())

# ------------  VEUILLEZ FERMER LES YEUX ET NE PAS PAS SCROLL AU DELA !!! DANGER !! -------------------------
def printHTML(longueurTotale, 
	nombreMots, 
	motLePlusLong, 
	motLePlusCourt,
	longueurMots,
	motsLettres, 
	motsChiffre, 
	motsSpecial, 
	lettresEtChiffres, 
	lettresEtSpecial, 
	chiffresEtSpecial, 
	lettresEtChiffresEtSpecial,
	lettre,
	chars,
	motsContenantChar):

	if not os.path.exists('graph'):
		os.makedirs('graph')
	if not os.path.exists('resultat'):
		os.makedirs('resultat')
	html = "<html><head><script src='https://unpkg.com/tlx/browser/tlx.js'></script>\n"
	html = html + "<script src='https://unpkg.com/tlx-chart/browser/tlx-chart.js'></script>\n"
	html = html + "<style> tr:nth-child(even){background-color: #f2f2f2;} td{border: 1px solid #ddd;padding: 8px;text-align:center;}</style>"
	html = html + "</head><body>\n"
 	
	html = html + "<h1 style=\"text-align: center;\"> Resultat du parseur fichier : "+ os.path.basename(sys.argv[-1]) +" </h1><table style=\"margin: auto;\">\n"
	html = html + "<tr> <td> Nombre de mots      :  </td><td>"  + str(nombreMots) +"</td> </tr>\n"
	html = html + "<tr> <td> Taille moyenne      :  </td><td>"  + str(round(Decimal(float(longueurTotale) / nombreMots), 2)) +"</td> </tr>\n"
	html = html + "<tr> <td> Mot le plus long    :  </td><td>"  + str(motLePlusLong) +"</td> </tr>\n"
	html = html + "<tr> <td> Mot le plus court   :  </td><td>"  + str(motLePlusCourt) +"</td> </tr>\n"
	html = html + "<tr> <td> Lettres uniquement  :  </td><td>"  + str(motsLettres) + " (" + str(round(Decimal(motsLettres / float(nombreMots) * 100), 2)) + "%)</td> </tr>\n"
	html = html + "<tr> <td> Chiffres uniquement :  </td><td>"  + str(motsChiffre) + " (" + str(round(Decimal(motsChiffre / float(nombreMots) * 100), 2)) + "%)</td> </tr>\n"
	html = html + "<tr> <td> Special uniquement  :  </td><td>"  + str(motsSpecial) + " (" + str(round(Decimal(motsSpecial / float(nombreMots) * 100), 2)) + "%)</td> </tr>\n"
	html = html + "<tr> <td> Lettres + chiffres  :  </td><td>"  + str(lettresEtChiffres) + " (" + str(round(Decimal(lettresEtChiffres / float(nombreMots) * 100), 2)) + "%)</td> </tr>\n"
	html = html + "<tr> <td> Lettres + special   :  </td><td>"  + str(lettresEtSpecial) + " (" + str(round(Decimal(lettresEtSpecial / float(nombreMots) * 100), 2)) + "%)</td> </tr>\n"
	html = html + "<tr> <td> Chiffres + special  :  </td><td>"  + str(chiffresEtSpecial) + " (" + str(round(Decimal(chiffresEtSpecial / float(nombreMots) * 100), 2)) + "%)</td> </tr>\n"
	html = html + "<tr> <td> Lett + chiff + spec :  </td><td>"  + str(lettresEtChiffresEtSpecial) + " (" + str(round(Decimal(lettresEtChiffresEtSpecial / float(nombreMots) * 100), 2)) + "%)</td> </tr>\n"
	html = html + "</table>\n"

	# ------------  REPARTITION DES LETTRES -------------
	html = html + "<h1 style=\"text-align:center;\"> Répartition des lettres </h1>\n"
	html = html + "<table style=\"margin: auto;\">\n"
	html = html + "<tr> <td> Lettre </td><td> Nombre d'apparition </td><td> Mots contenant cette lettre</td><td> Apparition moyenne dans un mot </td> </tr>\n"
	for lettre in sorted(chars, key = chars.get, reverse = True):
		html = html + "<tr> <td>"+ lettre +"</td><td>"  +  str(chars[lettre]) +"</td><td>"+ str(motsContenantChar[lettre]) +"</td><td>"+ str(round(Decimal(chars[lettre] / float(motsContenantChar[lettre])), 2)) +"</td> </tr>\n"
	html = html + "</table>\n"

	# ------------  GRAPH LONGUEUR MOT -------------
	html = html + "<h1 style=\"text-align:center;\"> Graphiques</h1>\n"
	nombre =[]
	longueur =[]
	for i in range(len(longueurMots)):	
		nombre.append(round(Decimal(longueurMots[i] / float(nombreMots) * 100), 2))
		longueur.append(str(i))

	index = np.arange(len(longueurMots))
	fig, ax = plt.subplots()
	plt.bar(index, nombre, 0.35, 0.8, label='Longueur')
	plt.xlabel('Nombre de characteres')
	plt.ylabel('Nombre de mots en %')
	plt.title('Repartition des mots en fonction de leurs tailles.')
	fig.savefig('graph/tableLongueur'+ os.path.basename(sys.argv[-1]).split('.')[0] +'.png')

	html = html + "<img src=\"../graph/tableLongueur"+ os.path.basename(sys.argv[-1]).split('.')[0] +".png\" style=\"display:block;margin: auto;width: 60%;border: 3px solid black;padding: 15px;margin-bottom: 20px;\">\n"

	# ------------  GRAPH CONTENU DES MOTS -------------
	nombre = [round(Decimal(motsLettres / float(nombreMots) * 100), 2),
	round(Decimal(motsChiffre / float(nombreMots) * 100), 2),
	round(Decimal(motsSpecial / float(nombreMots) * 100), 2),
	round(Decimal(lettresEtChiffres / float(nombreMots) * 100), 2),
	round(Decimal(lettresEtSpecial / float(nombreMots) * 100), 2),
	round(Decimal(chiffresEtSpecial / float(nombreMots) * 100), 2),
	round(Decimal(lettresEtChiffresEtSpecial / float(nombreMots) * 100), 2)]
	type_ = ["Lettres uniquement", "Chiffres uniquement", "Special uniquement", "Lettres + chiffres", "Lettres + special", "Chiffres + special", "Lett + chiff + spec"]
	index = np.arange(7)
	fig, ax = plt.subplots()
	plt.bar(index, nombre, 0.35, 0.8, label='Type')
	plt.xlabel('Type')
	plt.xticks(index, type_, rotation=15)
	plt.ylabel('Nombre de mots en %')
	plt.title('Repartition des mots en fonction de leurs contenu.')
	fig.savefig('graph/tableType'+ os.path.basename(sys.argv[-1]).split('.')[0] +'.png')
	html = html + "<img src=\"../graph/tableType"+ os.path.basename(sys.argv[-1]).split('.')[0] +".png\" style=\"display:block;margin: auto;width: 60%;border: 3px solid black;padding: 15px;\">\n"
	html = html + "</body></html>\n"
	hs = open("resultat/"+os.path.basename(sys.argv[-1]).split('.')[0]+".html", 'w')
	hs.write(html)
	
	print html
	#webbrowser.open('file://' + os.path.realpath("resultat/"+os.path.basename(sys.argv[-1]).split('.')[0]+".html"))

	

if __name__ == "__main__":
    main(sys.argv[1:])
