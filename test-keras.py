from __future__ import print_function
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.python.keras.layers import LSTM, CuDNNLSTM
from tensorflow.keras.optimizers import RMSprop, Adam
from keras.utils.data_utils import get_file
from time import time
import numpy as np
import random
import sys
import io
import time
import os
import keras

step_length = 1     # Decalage de sequence
epochs = 3         # Nombre de generations
batch_size = 128     # Taille de l'echantillon a chaque apprentissage
latent_dim = 64     # Taille du LSTM
dropout_rate = 0.2  # Dropout
model_path = os.path.realpath('./models/model2_11-12.h5')  # Lieu d'enregistrement du modele
load_model = False  # Est-ce qu'on charge le modele ?
store_model = not load_model  # Est-ce qu'on sauve le modele ?
verbosity = 1       # Affichage des generations
gen_amount = 1000    # Nombre de mots a generer
taux_train = 70
taux_dev = 10
taux_test = 20
min_length = 6
max_length = 11

def main(argv):
    ########### LECTURE DU FICHIER ###########
    f = open(argv[0], "r")
    texttmp = f.read().split('\n')
    text = []
    #model_path = os.path.realpath('./models/'+ argv[1])
    ########### SUPPRESSION DES MOTS TROP COURTS/LONGS ###########
    for mot in texttmp:
        if len(mot) >= min_length and len(mot) <= max_length:
            text.append(mot)

    ########### TOUS LES MOTS DE PASSE DANS UN STRING SEPARES PAR '\n' ###########
    texte_concat = '\n'.join(text)

    ########### RECUPERATION DE TOUS LES CARACTERES DIFFERENTS ###########
    chars = sorted(list(set(texte_concat)))
    num_chars = len(chars)
    print(num_chars)

    ########### CREATION DES DICOS CHAR -> INDICE ET INVERSEMENT ###########
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))
    mot_long = max([len(mdp) for mdp in text])
    sequences = []
    next_chars = []

    ########### STOCKE TOUTES LES SEQUENCES DE MOTS DE PASSE DANS UNE LISTE, EN SE DEPLACANT DE step_length A CHAQUE FOIS ###########
    ########### STOCKE LE CARACTERE SUIVANT DANS NEXT_CHAR ###########
    for i in range(0, len(texte_concat) - mot_long, step_length):
        sequences.append(texte_concat[i: i + mot_long])
        next_chars.append(texte_concat[i + mot_long])
    num_sequences = len(sequences)

    ########### CREE DES TABLEAUX REMPLIS DE ZEROS ###########
    ########### X : CODAGE DES CARACTERES DE CHAQUE SEQUENCE EN BOOL ###########
    ########### Y : CODAGE DES NEXT_CHARS EN BOOL ###########
    X = np.zeros((num_sequences, mot_long, num_chars), dtype=np.bool)
    Y = np.zeros((num_sequences, num_chars), dtype=np.bool)
    for i, sequence in enumerate(sequences):
        for j, char in enumerate(sequence):
            X[i, j, char_indices[char]] = 1
        Y[i, char_indices[next_chars[i]]] = 1


    ########### ON DIVISE LE TOUT EN 3 PARTIES, TRAIN/DEV/TEST ###########
    nb = len(X)

    max_train = int(float(nb) / 100 * taux_train)
    max_dev = int(float(nb) / 100 * (taux_dev + taux_train))

    X_train = X[:max_train]
    X_dev = X[max_train:max_dev]
    X_test = X[max_dev:]

    Y_train = Y[:max_train]
    Y_dev = Y[max_train:max_dev]
    Y_test = Y[max_dev:]
    
    ########### DEBUT KERAS ###########verbosity
    model = Sequential()

    ########### CHARGEMENT DU MODELE ###########
    if load_model:
        model = keras.models.load_model(model_path)
    else:
        
        model.add(CuDNNLSTM(latent_dim, input_shape=(mot_long, num_chars)))
        model.add(Dense(num_chars, activation='softmax'))
        optimizer = RMSprop(lr=0.01)
        #optimizer = Adam(lr=0.01) 
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=["accuracy"])

        model.summary()
        start = time.time()
        print('Start training ')
        tensor = TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)#TensorBoard(log_dir="logs\{}", histogram_freq=1, write_graph=True, write_images=True, write_grad=True)
        history = model.fit(X_train, Y_train, epochs=epochs, batch_size=batch_size, verbose=verbosity, validation_data=(X_dev, Y_dev), callbacks = [tensor])
        end = time.time()
        print('Finished training - time elapsed:', (end - start)/60, 'min')

        score = model.evaluate(X_test, Y_test, verbose=0)
        print("Test score : ", score)
        print("Test accuracy : ", score[1])
        model_path = os.path.realpath('./models/model-'+ str(round(score[1], 2)) +'.h5')

    if store_model:
        if not os.path.exists('models'):
            os.makedirs('models')
        print('Storing model at:', model_path)
        model.save(model_path)
    
    # Start sequence generation from end of the input sequence
    sequence = texte_concat[-(mot_long - 1):] + '\n'

    new_pwd = []

    print('{} generation de nouveau mdp'.format(gen_amount))

    while len(new_pwd) < gen_amount:
        x = np.zeros((1, mot_long, num_chars))
        for i, char in enumerate(sequence):
            x[0, i, char_indices[char]] = 1

        probs = model.predict(x, verbose = 0)[0]
        probs /= probs.sum()
        next_idx = np.random.choice(len(probs), p=probs)

        next_char = indices_char[next_idx]
        sequence = sequence[1:] + next_char

        # New line means we have a new password
        if next_char == '\n':
            gen_pwd = sequence.split('\n')[1] #[password for password in sequence.split('\n')][1]

            # Discard all passwords that are too short
            if len(gen_pwd) >= min_length:
                # Only allow new and unique passwords
                if gen_pwd not in new_pwd:
                    new_pwd.append(gen_pwd)

            if 0 == (len(new_pwd) % (gen_amount/ 10)):
                print('Generated '+ str(len(new_pwd)) +' password')

    print('First'+ str(gen_amount) +' generated passwords:')
    f = open("generated.txt", "w")
    for password in new_pwd[:gen_amount]:
        f.write(password +"\n")
    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
