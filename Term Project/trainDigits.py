from sklearn.datasets import load_digits
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from matplotlib import pyplot as plt
import NN
import random


digits = load_digits()
enc = OneHotEncoder()
enc.fit(digits.target.reshape(-1,1))
target_1hot = enc.transform(digits.target.reshape(-1,1)).toarray()

data_set = []
for idx in range(0, len(digits.images)):
    data_set.append([np.array((digits.images[idx]/256).flatten()), np.array(target_1hot[idx])])

random.shuffle(data_set)
test_set = data_set[int((len(data_set)-1)*0.85):-1]
training_set = data_set[:int((len(data_set)-1)*0.85)]
nn = NN.NeuralNetwork([len(digits.images[0].flatten()),60,10,10])
loss = []
for i in range(10000):
    loss.append(sum(NN.backPropLearning(training_set, nn, 0.005)))

accuracy = 0
for test_pair in test_set:
    out = nn.predict(test_pair[0])
    if(np.argmax(out) == np.argmax(test_pair[1])):
        accuracy += 1
accuracy = accuracy/len(test_set)
print("{:.2f}%".format(accuracy*100))

NN.saveParameters('DigitClassifer.txt', nn)

plt.plot(loss, label='Training Error')
plt.legend()
plt.show()