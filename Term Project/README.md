# Neural Network Generator

The neural network generator is comprised of three main files: __NN.py__, __trainNN.py__, and __testNN.py__.

### NN.py module

The __NN.py__ module is the module that generates neural networks. To generate a neural network, you simply need to make an NeuralNetwork object with the specified hyperparameters:

```
import NN
Layer_sizes = [input_size, h1_size, h2_size, ..., hn_size, output_size]
nn = NN.NeuralNetwork(Layer_sizes, bias, activateFunc)
```
where the Layer_sizes specifies how many nodes are in each of the layers of the neural network, the bias is a boolean specifying if bias values should be used, and the activateFunc is the name of the activation function as a string. The available activation functions are sigmoid and rectified Linear Unit (reLU). 

When the object is initiated, the weights and biases are randomly assigned. In order to train the neural network, the _backPropLearning_ function is used as follows:

```
NN.backPropLearning(training_set, nn, alpha))
```

where alpha is the learning rate in ]0,1[, and the training_set is a list of input-output pairs. The function randomly shuffles the training set and performs the learning process. The learning process is a forward propagation phase with the input, a loss computation of the neural network output with the expected output, and a back propagation of the error to adjust the weights. 

When the neural network is trained, the hyperparameters and parameters can be saved using the _saveParameters_ function:

```
NN.saveParameters(filename, nn)
```

 and can be used later with the _loadParameters_ function:
 
 ```
NN.loadParameters(filename, nn) 
 ```
 
 The saved file generated with _saveParameters_ is human readable and contains the layer_sizes, the activation function, the weights and the biases. 

### trainNN.py script
 
 The __trainNN.py__ script is an easy, pre-implemented, script that makes the training of neural networks simple. The script performs training on the neural network over multiple epochs and uses the validation set early stopping condition to stop training. The script gives the user the option to either continue training or to stop training when the validation set loss increases, giving the user the decision and removing the possibility that noise stops the training.
 
 The only sections in the script that the user needs to modify are the Hyperparameters section, for putting your own, the Get Database section, to retrieve your data set, and the Preprocess data section so that the data is in the format acceptable by the neural network.
 
 Once done, the script needs only to be run and monitored. When finished, the neural network will be saved to the file given in the Hyperparameters section.
 
### testNN.py

The __testNN.py__ scipt loads the trained neural network and tests the accuracy, false positives, and false negatives of the neural network. Again, the only sections that the user needs to modify is the loadParameters filename, the Get Simulation Database section, which is the test set, and the Preprocess data, which needs to modify the database data to be acceptable by the neural network. 

Once done, the script needs only to be run and the results will be displayed after going through the entire data set.