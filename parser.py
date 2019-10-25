#!/usr/bin/env python
# coding: utf-8

import sys
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

	print("Lettres only  : " + str(motsLettres))
	print("Chiffres only : " + str(motsChiffre))
	print("Spéciaux only : " + str(motsSpecial) + "\n")

	print("Lettres + chiffres  : " + str(lettresEtChiffres))
	print("Lettres + special   : " + str(lettresEtSpecial))
	print("Chiffres + special  : " + str(chiffresEtSpecial))
	print("Lett + chiff + spec : " + str(lettresEtChiffresEtSpecial) + "\n")

	print("Majuscule(s)        : " + str(uppercases))
	print("Majuscule au debut  : " + str(uppercasesFirst))

	print("\n\tMots de taille\n")

	for i in range(len(longueurMots)):
		if i != 0:
			if i < 10:
				print(str(i) + "   : " + str(longueurMots[i]))
			elif i == 14:
				print(str(i) + "+ : " + str(longueurMots[i]))
			elif i >= 10:
				print(str(i) + "  : " + str(longueurMots[i]))

	print("\n\tOccurences des lettres\n")

	for lettre in sorted(chars, key = chars.get, reverse = True):
		print(lettre + " : " + str(chars[lettre]) + " (" + str(motsContenantChar[lettre]) + " mots / " + str(round(Decimal(chars[lettre] / float(motsContenantChar[lettre])), 2)) + " par mot)")

if __name__ == "__main__":
    main(sys.argv[1:])