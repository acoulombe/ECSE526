import NN
import pylab as pl
import numpy as np
from sklearn.datasets import load_digits


nn = NN.NeuralNetwork([64,60,10,10])
NN.loadParameters('DigitClassifer.txt', nn)

digits = load_digits()

while(True):
    idx = int(input('Enter Index:'))
    print(f'Predicted : {np.argmax(nn.predict(digits.images[idx].flatten()))}')
    print(f'Expected : {digits.target[idx]}')
    pl.gray()
    pl.matshow(digits.images[idx])
    pl.show()