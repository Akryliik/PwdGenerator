#!/usr/bin/env python

import sys
import io
import webbrowser, os
import base64
import numpy as np
import matplotlib.pyplot as plt

def main(argv):
	longueurTotale = 0
	nombreMots = 0
	motLePlusLong = 0
	motLePlusCourt = 9999
	longueurMots = 13 * [0]
	motsLettres = 0
	motsChiffre = 0
	motsSpecial = 0
	lettresEtChiffres = 0
	lettresEtSpecial = 0
	chiffresEtSpecial = 0
	lettresEtChiffresEtSpecial = 0

	with open(argv[0], 'r') as fichier:
		lignes = fichier.read().split('\n')

		for ligne in lignes:
			if len(ligne) > 0:
				nombreMots += 1
				longueurTotale += len(ligne)

				if len(ligne) > motLePlusLong:
					motLePlusLong = len(ligne)

				if len(ligne) < motLePlusCourt:
					motLePlusCourt = len(ligne)

				if len(ligne) > 12:
					longueurMots[12] += 1
				else:
					longueurMots[len(ligne)] += 1

				if ligne.isalpha():
					motsLettres += 1

				if ligne.isdigit():
					motsChiffre += 1

				if contientLettre(ligne) and contientChiffre(ligne) and not contientSpecial(ligne):
					lettresEtChiffres += 1
				if contientLettre(ligne) and contientSpecial(ligne) and not contientChiffre(ligne):
					lettresEtSpecial += 1
				if contientSpecial(ligne) and contientChiffre(ligne) and not contientLettre(ligne):
					chiffresEtSpecial += 1
				if contientSpecial(ligne) and contientChiffre(ligne) and contientLettre(ligne):
					lettresEtChiffresEtSpecial += 1
				if contientSpecial(ligne) and not contientChiffre(ligne) and not contientLettre(ligne):
					motsSpecial += 1

	print("Nombre de mots      : " + str(nombreMots))
	print("Taille moyenne      : " + str(float(longueurTotale) / nombreMots))
	print("Mot le plus long    : " + str(motLePlusLong))
	print("Mot le plus court   : " + str(motLePlusCourt))
	print("Lettres uniquement  : " + str(motsLettres))
	print("Chiffres uniquement : " + str(motsChiffre))
	print("Special uniquement  : " + str(motsSpecial))
	print("Lettres + chiffres  : " + str(lettresEtChiffres))
	print("Lettres + special   : " + str(lettresEtSpecial))
	print("Chiffres + special  : " + str(chiffresEtSpecial))
	print("Lett + chiff + spec : " + str(lettresEtChiffresEtSpecial))
	print("Total               : " + str(motsLettres + motsChiffre + motsSpecial + lettresEtChiffres + lettresEtSpecial + chiffresEtSpecial + lettresEtChiffresEtSpecial))

	for i in range(len(longueurMots)):
		if i != 0:
			if i < 10:
				print("Mots de taille " + str(i) + "    : " + str(longueurMots[i]))
			elif i == 12:
				print("Mots de taille " + str(i) + "+  : " + str(longueurMots[i]))
			elif i >= 10:
				print("Mots de taille " + str(i) + "   : " + str(longueurMots[i]))

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
	lettresEtChiffresEtSpecial)

def contientLettre(mot):
	for i in mot:
		if i.isalpha():
			return True
	return False


def contientChiffre(mot):
	for i in mot:
		if i.isdigit():
			return True
	return False


def contientSpecial(mot):
	for i in mot:
		if not i.isdigit() and not i.isalpha():
			return True
	return False

def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())

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
	lettresEtChiffresEtSpecial):

	html = "<html><head><script src='https://unpkg.com/tlx/browser/tlx.js'></script><script src='https://unpkg.com/tlx-chart/browser/tlx-chart.js'></script></head><body>\n"
 	
	html = html + "<h3> Resultat du parseur fichier : "+ os.path.basename(sys.argv[-1]) +" </h3><table>\n"
	html = html + "<tr> <td> Nombre de mots      :  </td><td>"  + str(nombreMots) +"</td> </tr>\n"
	html = html + "<tr> <td> Taille moyenne      :  </td><td>"  + str(float(longueurTotale) / nombreMots) +"</td> </tr>\n"
	html = html + "<tr> <td> Mot le plus long    :  </td><td>"  + str(motLePlusLong) +"</td> </tr>\n"
	html = html + "<tr> <td> Mot le plus court   :  </td><td>"  + str(motLePlusCourt) +"</td> </tr>\n"
	html = html + "<tr> <td> Lettres uniquement  :  </td><td>"  + str(motsLettres) +"</td> </tr>\n"
	html = html + "<tr> <td> Chiffres uniquement :  </td><td>"  + str(motsChiffre) +"</td> </tr>\n"
	html = html + "<tr> <td> Special uniquement  :  </td><td>"  + str(motsSpecial) +"</td> </tr>\n"
	html = html + "<tr> <td> Lettres + chiffres  :  </td><td>"  + str(lettresEtChiffres) +"</td> </tr>\n"
	html = html + "<tr> <td> Lettres + special   :  </td><td>"  + str(lettresEtSpecial) +"</td> </tr>\n"
	html = html + "<tr> <td> Chiffres + special  :  </td><td>"  + str(chiffresEtSpecial) +"</td> </tr>\n"
	html = html + "<tr> <td> Lett + chiff + spec :  </td><td>"  + str(lettresEtChiffresEtSpecial) +"</td> </tr>\n"
	html = html + "<tr> <td colspan='2'> Longueur des mots : </td><td>\n"
	html = html + "</table>\n"


	nombre =[]
	longueur =[]
	for i in range(len(longueurMots)):	
		nombre.append(str(i))
		longueur.append(str(longueurMots[i]))

	index = np.arange(13)
	fig, ax = plt.subplots()
	plt.bar(index, longueur, 0.35, 0.8, label='Longueur')
	plt.xlabel('Taille')
	plt.ylabel('Nombre de mots')
	plt.title('Repartition des mots en fonction de leurs tailles.')
	fig.savefig('graph/tableLongueur'+ os.path.basename(sys.argv[-1]).split('.')[0] +'.png')

	html = html + "<img src=\"../graph/tableLongueur"+ os.path.basename(sys.argv[-1]).split('.')[0] +".png\" style=\"display:block;margin: auto;width: 60%;border: 3px solid black;padding: 10px;\">\n"

	nombre = [motsLettres, motsChiffre, motsSpecial, lettresEtChiffres, lettresEtSpecial, chiffresEtSpecial, lettresEtChiffresEtSpecial]
	type_ = ["Lettres uniquement", "Chiffres uniquement", "Special uniquement", "Lettres + chiffres", "Lettres + special", "Chiffres + special", "Lett + chiff + spec"]
	index = np.arange(7)
	fig, ax = plt.subplots()
	plt.bar(index, nombre, 0.35, 0.8, label='Type')
	plt.xlabel('Type')
	plt.xticks(index, type_, rotation=15)
	plt.ylabel('Nombre de mots')
	plt.title('Repartition des mots en fonction de leurs types.')
	fig.savefig('graph/tableType'+ os.path.basename(sys.argv[-1]).split('.')[0] +'.png')
	html = html + "<img src=\"../graph/tableType"+ os.path.basename(sys.argv[-1]).split('.')[0] +".png\" style=\"display:block;margin: auto;width: 60%;border: 3px solid black;padding: 10px;\">\n"
	html = html + "</body></html>\n"
	hs = open("resultat/"+os.path.basename(sys.argv[-1]).split('.')[0]+".html", 'w')
	hs.write(html)
	
	print html
	webbrowser.open('file://' + os.path.realpath("resultat/"+os.path.basename(sys.argv[-1]).split('.')[0]+".html"))


if __name__ == "__main__":
    main(sys.argv[1:])
