#!/usr/bin/env python
# coding: utf-8

import sys

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
	uppercases = 0
	uppercasesFirst = 0

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

				if contientUpper(ligne):
					uppercases += 1
				if ligne[0].isupper():
					uppercasesFirst += 1

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

	print("\tStatistiques de base\n")
	print("Nombre de mots    : " + str(nombreMots))
	print("Taille moyenne    : " + str(float(longueurTotale) / nombreMots))
	print("Mot le plus long  : " + str(motLePlusLong))
	print("Mot le plus court : " + str(motLePlusCourt))
	print("\n\tMots contenant\n")
	print("Lettres uniquement  : " + str(motsLettres))
	print("Chiffres uniquement : " + str(motsChiffre))
	print("Spéciaux uniquement : " + str(motsSpecial) + "\n")
	print("Lettres + chiffres  : " + str(lettresEtChiffres))
	print("Lettres + special   : " + str(lettresEtSpecial))
	print("Chiffres + special  : " + str(chiffresEtSpecial))
	print("Lett + chiff + spec : " + str(lettresEtChiffresEtSpecial) + "\n")
	print("Majuscule(s)        : " + str(uppercases))
	print("Majuscule au debut  : " + str(uppercasesFirst))
	print("\n\tMots d'une certaine taille\n")

	for i in range(len(longueurMots)):
		if i != 0:
			if i < 10:
				print(str(i) + "   : " + str(longueurMots[i]))
			elif i == 12:
				print(str(i) + "+ : " + str(longueurMots[i]))
			elif i >= 10:
				print(str(i) + "  : " + str(longueurMots[i]))

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

def contientUpper(mot):
	for i in mot:
		if i.isalpha() and i.isupper():
			return True
	return False

if __name__ == "__main__":
    main(sys.argv[1:])