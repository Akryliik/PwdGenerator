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

step_length = 1     # Decalage de sequence
epochs = 1         # Nombre de generations
batch_size = 32     # Taille de l'echantillon a chaque apprentissage
latent_dim = 64     # Taille du LSTM
dropout_rate = 0.2  # Dropout
model_path = os.path.realpath('./modele.h5')  # Lieu d'enregistrement du modele
load_model = False  # Est-ce qu'on charge le modele ?
store_model = not load_model  # Est-ce qu'on sauve le modele ?
verbosity = 1       # Affichage des generations
gen_amount = 100    # Nombre de mots a generer
taux_train = 70
taux_dev = 10
taux_test = 20

def main(argv):
    ########### LECTURE DU FICHIER ###########
    f = open(argv[0], "r")
    texttmp = f.read().split('\n')
    text = []

    ########### SUPPRESSION DES MOTS TROP COURTS/LONGS ###########
    for mot in texttmp:
        if len(mot) > 6 and len(mot) < 11:
            text.append(mot)
    
    nbmots = len(text)

    max_train = nbmots / 100 * taux_train
    max_dev = nbmots / 100 * (taux_dev + taux_train)

    text_train = text[:max_train]
    text_dev = text[max_train:max_dev]
    text_test = text[max_dev:]

    ########### TOUS LES MOTS DE PASSE DANS UN STRING SEPARES PAR '\n' ###########
    texte_concat = '\n'.join(text_train)

    texte_concat_test = '\n'.join(text_test)

    ########### RECUPERATION DE TOUS LES CARACTERES DIFFERENTS ###########
    chars = sorted(list(set(texte_concat)))
    num_chars = len(chars)

    chars_test = sorted(list(set(texte_concat_test)))
    num_chars_test = len(chars_test)

    ########### CREATION DES DICOS CHAR -> INDICE ET INVERSEMENT ###########
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))
    mot_long = max([len(mdp) for mdp in text_train])
    sequences = []
    sequences_test = []

    char_indices_test = dict((c, i) for i, c in enumerate(chars_test))
    indices_char_test = dict((i, c) for i, c in enumerate(chars_test))
    mot_long_test = max([len(mdp) for mdp in text_test])
    next_chars = []
    next_chars_test = []

    ########### STOCKE TOUTES LES SEQUENCES DE MOTS DE PASSE DANS UNE LISTE, EN SE DEPLACANT DE step_length A CHAQUE FOIS ###########
    ########### STOCKE LE CARACTERE SUIVANT DANS NEXT_CHAR ###########
    for i in range(0, len(texte_concat) - mot_long, step_length):
        sequences.append(texte_concat[i: i + mot_long])
        next_chars.append(texte_concat[i + mot_long])
    num_sequences = len(sequences)

    for i in range(0, len(texte_concat_test) - mot_long_test, step_length):
        sequences_test.append(texte_concat_test[i: i + mot_long_test])
        next_chars_test.append(texte_concat_test[i + mot_long_test])
    num_sequences_test = len(sequences_test)

    ########### CREE DES TABLEAUX REMPLIS DE ZEROS ###########
    ########### X : CODAGE DES CARACTERES DE CHAQUE SEQUENCE EN BOOL ###########
    ########### Y : CODAGE DES NEXT_CHARS EN BOOL ###########
    X = np.zeros((num_sequences, mot_long, num_chars), dtype=np.bool)
    Y = np.zeros((num_sequences, num_chars), dtype=np.bool)
    for i, sequence in enumerate(sequences):
        for j, char in enumerate(sequence):
            X[i, j, char_indices[char]] = 1
        Y[i, char_indices[next_chars[i]]] = 1

    X_test = np.zeros((num_sequences_test, mot_long_test, num_chars_test), dtype=np.bool)
    Y_test = np.zeros((num_sequences_test, num_chars_test), dtype=np.bool)
    for i, sequence in enumerate(sequences_test):
        for j, char in enumerate(sequence):
            X_test[i, j, char_indices_test[char]] = 1
        Y_test[i, char_indices_test[next_chars_test[i]]] = 1

    ########### DEBUT KERAS ###########
    model = Sequential()

    ########### CHARGEMENT DU MODELE ###########
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

        score = model.evaluate(X_test, Y_test, verbose=0)
        prin("Test score : ", score[0])
        prin("Test accuracy : ", score[1])

    if store_model:
        print('Storing model at:', model_path)
        model.save(model_path)
    
    # Start sequence generation from end of the input sequence
    sequence = texte_concat[-(mot_long - 1):] + '\n'

    new_names = []

    print('{} new names are being generated'.format(gen_amount))

    while len(new_names) < gen_amount:
        x = np.zeros((1, mot_long, num_chars))
        for i, char in enumerate(sequence):
            x[0, i, char_indices[char]] = 1

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
