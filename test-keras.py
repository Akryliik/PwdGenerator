from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import io
import time
import os
import keras

step_length = 1    # The step length we take to get our samples from our corpus
epochs = 10       # Number of times we train on our full data
batch_size = 32    # Data samples in each training step
latent_dim = 64    # Size of our LSTM
dropout_rate = 0.2  # Regularization with dropout
model_path = os.path.realpath('./modele.h5')  # Location for the model
load_model = False  # Enable loading model from disk
store_model = not load_model  # Store model to disk after training
verbosity = 1      # Print result for each epoch
gen_amount = 100    # How many


def main(argv):
    f = open(argv[0], "r")
    text = f.read().split('\n')
    print(text[:5])

    print('taille corpus : ', len(text))

    texte_concat = '\n'.join(text)

    chars = sorted(list(set(texte_concat)))
    num_chars = len(chars)
    print(chars)

    print('nb diff chars :', len(chars))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    mot_long = max([len(mdp) for mdp in text])
    print('mot le plus long : ', mot_long)

    sequences = []
    next_chars = []

    for i in range(0, len(texte_concat) - mot_long, step_length):
        sequences.append(texte_concat[i: i + mot_long])
        next_chars.append(texte_concat[i + mot_long])

    num_sequences = len(sequences)

    print('Number of sequences:', num_sequences)
    print('First 10 sequences and next chars:')
    for i in range(10):
        print('X=[{}]   y=[{}]'.replace('\n', ' ').format(
            sequences[i], next_chars[i]).replace('\n', ' '))

    X = np.zeros((num_sequences, mot_long, num_chars), dtype=np.bool)
    Y = np.zeros((num_sequences, num_chars), dtype=np.bool)

    for i, sequence in enumerate(sequences):
        for j, char in enumerate(sequence):
            X[i, j, char_indices[char]] = 1
        Y[i, char_indices[next_chars[i]]] = 1

    print('X shape: {}'.format(X.shape))
    print('Y shape: {}'.format(Y.shape))

    model = Sequential()

    if load_model:
        model = keras.models.load_model(model_path)
    else:
        model.add(LSTM(latent_dim, input_shape=(mot_long, num_chars), recurrent_dropout=dropout_rate))
        model.add(Dense(units=num_chars, activation='softmax'))

        optimizer = RMSprop(lr=0.01)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer)

        model.summary()
        start = time.time()
        print('Start training for {} epochs'.format(epochs))
        history = model.fit(X, Y, epochs=epochs, batch_size=batch_size, verbose=verbosity)
        end = time.time()
        print('Finished training - time elapsed:', (end - start)/60, 'min')

    if store_model:
        print('Storing model at:', model_path)
        model.save(model_path)
    
    # Start sequence generation from end of the input sequence
    sequence = texte_concat[-(mot_long - 1):] + '\n'

    new_names = []

    print('{} new names are being generated'.format(gen_amount))

    while len(new_names) < gen_amount:
        # Vectorize sequence for prediction
        x = np.zeros((1, mot_long, num_chars))
        for i, char in enumerate(sequence):
            x[0, i, char_indices[char]] = 1

        # Sample next char from predicted probabilities
        probs = model.predict(x, verbose=0)[0]
        probs /= probs.sum()
        next_idx = np.random.choice(len(probs), p=probs)   
        next_char = indices_char[next_idx]
        sequence = sequence[1:] + next_char

        # New line means we have a new name
        if next_char == '\n':
            gen_name = [name for name in sequence.split('\n')][1]

            # Discard all names that are too short
            if len(gen_name) > 2:
                # Only allow new and unique names
                if gen_name not in new_names:
                    new_names.append(gen_name)

            if 0 == (len(new_names) % (gen_amount/ 10)):
                print('Generated {}'.format(len(new_names)))

    print_first_n = min(10, gen_amount)
    print('First {} generated names:'.format(print_first_n))
    for name in new_names[:print_first_n]:
        print(name)

if __name__ == "__main__":
    main(sys.argv[1:])
