import sys
import random

def main(argv):
    text = open(argv[0]).readlines()
    random.shuffle(text)

    open(argv[0], "w").writelines(text)

if __name__ == "__main__":
    main(sys.argv[1:])