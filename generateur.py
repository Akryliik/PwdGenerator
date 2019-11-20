
from keras.models import Sequential
from keras import optimizers
from keras import losses
from keras.utils import np_utils
from keras.datasets import mnist
from keras.layers import Dense, Activation

def main():

    data_raw = "abcd"
    chars = sorted(list(set(data_raw)))
    char_to_int = dict((c, i) for i, c in enumerate(chars))

    n_chars = len(data_raw)
    n_vocab = len(chars)
    print "Total Characters: ", n_chars
    print "Total Vocab: ", n_vocab

    # prepare the dataset of input to output pairs encoded as integers
    seq_length = 100
    dataX = []
    dataY = []
    for i in range(0, n_chars - seq_length, 1):
        seq_in = raw_text[i:i + seq_length]
        seq_out = raw_text[i + seq_length]
        dataX.append([char_to_int[char] for char in seq_in])
        dataY.append(char_to_int[seq_out])
    n_patterns = len(dataX)
    print "Total Patterns: ", n_patterns

if __name__ == "__main__":
	main()