import numpy as np
from matplotlib import pyplot as plt
import NN
import random


data_set = [
    [np.array([0, 0]), np.array([1,0])],
    [np.array([1, 0]), np.array([1,0])],
    [np.array([0, 1]), np.array([1,0])],
    [np.array([1, 1]), np.array([0,1])]
]

random.shuffle(data_set)
nn = NN.NeuralNetwork([2,4,2], bias=True)
loss = []
for i in range(5000):
    loss.append(sum(NN.backPropLearning(data_set, nn, 0.005)))

accuracy = 0
for test_pair in data_set:
    out = nn.predict(test_pair[0])
    if(np.argmax(out) == np.argmax(test_pair[1])):
        accuracy += 1
accuracy = accuracy/len(data_set)
print("{:.2f}%".format(accuracy*100))

NN.saveParameters('ANDClassifier.txt', nn)

plt.plot(loss, label='Training Error')
plt.legend()
plt.show()