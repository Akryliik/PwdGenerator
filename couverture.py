import sys

def main(argv):
    cnt = 0 
    corpusLines = open(argv[0]).readlines()
    lines = open(argv[1]).readlines()
    for line in lines: 
        if line in corpusLines:
            cnt += 1
            #print(line)
    print(cnt)
    

if __name__ == "__main__":
    main(sys.argv[1:])