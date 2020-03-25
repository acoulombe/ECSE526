import numpy as np
from matplotlib import pyplot as plt
import NN
import random
import csv_util


# Hyperparameters
alpha = 0.005
Layer_sizes = [5, 10, 10, 2]
train_test_split = 0.85

early_exit_samples = 20     # how many samples to use to check for early exit on training

# Get Database
raw_data_set = csv_util.read_csv('CollisionSet.csv')

# Preprocess data
data_set = []
for idx in range(0, len(raw_data_set)):
    features = np.array(raw_data_set[idx][:5])
    target = np.array([int(raw_data_set[idx][-1]==0),int(raw_data_set[idx][-1]==1)])
    data_set.append([features, target])

# Setup training data, test data and NN
random.shuffle(data_set)
validation_set = data_set[int((len(data_set)-1)*train_test_split):-1]
training_set = data_set[:int((len(data_set)-1)*train_test_split)]
nn = NN.NeuralNetwork(Layer_sizes)

# Training
training_loss = []
validation_loss = []
selection = 'y'
cnt = 0
while(True):
    training_loss.append(sum(NN.backPropLearning(training_set, nn, alpha))/len(training_set))

    loss = []
    for validation_pair in validation_set:
        out = nn.predict(validation_pair[0])
        loss.append(np.linalg.norm(validation_pair[1]-out))
    validation_loss.append(sum(loss)/len(validation_set))

    if(cnt > early_exit_samples and cnt%early_exit_samples==0):
        current_loss = sum(validation_loss[-int(early_exit_samples/2):])
        previous_loss = sum(validation_loss[-early_exit_samples:-int(early_exit_samples/2)])
        if(previous_loss <= current_loss):
            plt.plot(training_loss, label='Training Error')
            plt.plot(validation_loss, label='Validation Error')
            plt.xlabel('Number of Epochs')
            plt.ylabel('Loss Function')
            plt.title('Neural Network Loss over the number of epochs trained')
            plt.legend()
            plt.show()
            while(True):
                selection = input("Continue training the Neural Network? (y/n): ")
                if(selection == 'y' or selection =='n'):
                    break
                else:
                    print("Invalid Answer.")
            if(selection =='n'):
                break
    cnt += 1

print(f"Number of Epochs : {cnt}")

# Accuracy on Training Set
training_accuracy = 0
for training_pair in training_set:
    out = nn.predict(training_pair[0])
    if(np.argmax(out) == np.argmax(training_pair[1])):
        training_accuracy += 1
training_accuracy = training_accuracy/len(training_set)
print("Accuracy on Training Set : {:.2f}%".format(training_accuracy*100))

# Accuracy on Validation Set
validation_accuracy = 0
for validation_pair in validation_set:
    out = nn.predict(validation_pair[0])
    if(np.argmax(out) == np.argmax(validation_pair[1])):
        validation_accuracy += 1
validation_accuracy = validation_accuracy/len(validation_set)
print("Accurary on Test Set : {:.2f}%".format(validation_accuracy*100))

# Backup NN parameters
NN.saveParameters('CollisionClassifer2.txt', nn)

plt.plot(training_loss, label='Training Error')
plt.plot(validation_loss, label='Validation Error')
plt.xlabel('Number of Epochs')
plt.ylabel('Loss Function')
plt.title('Neural Network Loss over the number of epochs trained')
plt.legend()
plt.show()