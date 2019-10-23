def main():

	f= open("data.txt", "r")
	if f.mode == 'r':
		contents = f.readlines()

		totalLength = 0
		clearWord = ""
		biggest = 0
		biggestWord=""
		smallest = 9999999 
		smallestWord = ""
		digitWord = 0 
		strWord = 0
		tabWordLength = 13 * [0]


		for word in contents:
			clearWord = word.rstrip()
			totalLength += len(clearWord)

			if clearWord.isdigit():
				digitWord += 1
			if clearWord.isalpha():
				strWord += 1
			if len(clearWord) <= 12:
				tabWordLength[len(clearWord)] += 1

			if len(clearWord) > biggest:
				biggest = len(clearWord)
				biggestWord = clearWord
			if len(clearWord) < smallest:
				smallest = len(clearWord)
				smallestWord = clearWord

			#print(word)
		average = float(totalLength) / float(len(contents))


		print("Biggest word length" + str(biggest)+ ", word "+ str(biggestWord))
		print("Smallest word length" + str(smallest)+ ", word "+ str(smallestWord))
		print("Taille moyenne des mots : "+ str(average))
		print("Mots contenant que des chiffres : "+ str(digitWord))
		print("Mots contenant que du string : "+ str(strWord))

		for size in range(len(tabWordLength)):
			print("Mot de taille " + str(size) + " : " + str(tabWordLength[size]))

if __name__ == "__main__":
	main()