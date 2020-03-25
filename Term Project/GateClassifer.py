import NN
import numpy as np


nn = NN.NeuralNetwork([64,60,10,10], bias=True)
NN.loadParameters('ANDClassifier.txt', nn)

while(True):
    input_1 = int(input('Enter Input 1:'))
    input_2 = int(input('Enter Input 2:'))
    print(f'Predicted : {np.argmax(nn.predict(np.array([input_1, input_2])))}')
