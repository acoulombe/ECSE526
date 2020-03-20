import numpy as np
import math
import random


class NeuralNetwork():
    """Neural Network object

        Attributes
        ---------
            L : int
                number of layers in the Neural Network
                includes input layer, hidden layer(s) and output layer
            L_sizes : list(int)
                number of nodes inside each of the layers
            weights : list(np.array)
                list of the layers weights in order
            activateFunc : str
                activation function to use in the nodes
                Options : sigmoid
    """

    def __init__(self, L_sizes, bias=True, activateFunc='sigmoid'):
        """Initializes the neural network

        Parameters
            L_sizes : list(int)
                number of nodes inside each of the layers, includes input layer,
                hidden layers and output layer
            bias : bool
                flag to use layer node biases
            activateFunc : str
                activation function to use in the nodes
                Options : sigmoid, reLU
        """
        self.L = len(L_sizes)
        self.L_sizes = L_sizes
        self.activateFunc_str = activateFunc
        self.activateFunc = None
        self.activateFuncPrime = None
        self.useBias = bias

        self.weights = []
        self.bias = []
        for i in range(1, self.L):
            weights = np.random.randn(L_sizes[i], L_sizes[i-1])
            bias = np.random.randn(L_sizes[i])
            self.weights.append(weights)
            self.bias.append(bias)

        if(activateFunc =='sigmoid'):
            self.activateFunc = sigmoid
            self.activateFuncPrime = sigmoidPrime
        elif(activateFunc == 'reLU'):
            self.activateFunc = reLU
            self.activateFuncPrime = reLUPrime
        else:
            raise ValueError('Unsupported Activation Function')

    def feedForward(self, features):
        """Passes the features through the weights to generate the neural networks
        output at each layer before and after activation

        Parameters
        --------
            features : np.array
                feature vector for NN input
        Returns
        --------
            tuple(list(np.array), list(np.array))
                tuple with list of vectors of neuron inputs and list of neuron
                outputs produced by the NN
        """
        a = np.copy(features)
        z_l = []
        a_l = [a]
        for layer in range(0, self.L-1):
            # Multiply the inputs by the weights and add biases
            z = self.weights[layer].dot(a_l[-1])
            if(self.useBias):
                z += self.bias[layer]
            z_l.append(z)
            # Neuron activation
            a_l.append(self.activateFunc(z_l[-1]))
        return (z_l, a_l)

    def backPropagate(self, target, z_l, a_l):
        """Propagates the output error of the neural network to
        the weights and biases on the neural network

        Parameters
        --------
            target : np.array
                expected output of the neural network
            z_l : list(np.array)
                list of input values to the nodes of each layer of the network
            a_l : list(np.array)
                list of output values to the nodes of each layer of the network
        
        Returns
        --------
            tuple(list(np.array), list(np.array))
                tuple with list of matrices of neural network weight errors and list of
                neural network bias errors in the NN
        """
        dW = []
        db = []
        deltas = [None] * (self.L-1)
        # Compute Output error
        deltas[-1] = ((target-a_l[-1]))*self.activateFuncPrime(z_l[-1])

        # Back Propagate error to weights and biases
        for layer in reversed(range(0, len(deltas)-1)):
            deltas[layer] = self.weights[layer+1].T.dot(deltas[layer+1])*self.activateFuncPrime(z_l[layer])
        db = [d for d in deltas]
        dW = [np.outer(d, a_l[l]) for l,d in enumerate(deltas)]
        return dW, db

    def predict(self, features):
        """Passes the features through the weights to generate
        the neural networks output

        Parameters
        --------
            features : np.array
                feature vector for NN input
        Returns
        --------
            np.array
                output produced by the NN
        """
        z_l, a_l = self.feedForward(features)
        return a_l[-1]

def saveParameters(filename, network):
    """Saves the layer architecture, weights and biases of the neural network into a file
    
    Parameters
    --------
        filename : str
            name of the file to save the parameters in
        network : NeuralNetwork
            neural network to save to file
    """
    f = open(filename, 'w')
    # Write layer information
    f.write(f'Layer Sizes:[')
    for idx, layer_size in enumerate(network.L_sizes):
        f.write(f'{layer_size}')
        if(idx < (len(network.L_sizes)-1)):
            f.write(',')
    f.write(']\n')

    # Write activation function
    f.write(f'Activation Function:{network.activateFunc_str}\n')

    # Write weight information
    f.write('Weights {\n')
    for weights in network.weights:
        f.write('\t[\n')
        for row in weights:
            f.write('\t\t[')
            for idx,entry in enumerate(row):
                f.write(f'{entry}')
                if(idx < (len(row)-1)):
                    f.write(',')
            f.write(']\n')
        f.write('\t]\n')
    f.write('}\n')

    # Write bias information
    f.write('Biases {\n')
    for bias in network.bias:
        f.write('\t[')
        for idx, entry in enumerate(bias):
            f.write(f'{entry}')
            if(idx < (len(bias)-1)):
                f.write(',')
        f.write(']\n')
    f.write('}\n')
    f.close()

def loadParameters(filename, network):
    """Loads the layer architecture, weights and biases of the neural network from the given file
    
    Parameters
    --------
        filename : str
            name of the file to save the parameters in
        network : NeuralNetwork
            neural network to load parameters into
    """
    f = open(filename, 'r')

    # Read Layer sizes from file
    layer_str = f.readline()
    _, size_list = layer_str.split(':')
    network.L_sizes = [int(size) for size in size_list.replace('[','').replace(']','').split(',')]
    network.L = len(network.L_sizes)
    
    # Read the activation function
    activeFunc = f.readline()
    _, network.activateFunc_str = activeFunc.replace('\n','').split(':')

    if(network.activateFunc_str =='sigmoid'):
        network.activateFunc = sigmoid
        network.activateFuncPrime = sigmoidPrime
    elif(network.activateFunc_str == 'reLU'):
        network.activateFunc = reLU
        network.activateFuncPrime = reLUPrime
    else:
        raise ValueError('Unsupported Activation Function')

    # Read Weights
    f.readline()
    weights = []
    for l in range(1, len(network.L_sizes)):
        f.readline()
        layer_weight = []  
        for idx in range(network.L_sizes[l]):
            row = f.readline()
            row = row.replace('\t','').replace('\n','').replace('[','').replace(']','')
            layer_weight.append([float(entry) for entry in row.split(',')])
        f.readline()
        weights.append(np.array(layer_weight))
    f.readline()
    network.weights = weights
    
     # Read Weights
    f.readline()
    bias = []
    for l in range(1, len(network.L_sizes)):
        layer_bias = []  
        row = f.readline()
        row = row.replace('\t','').replace('\n','').replace('[','').replace(']','')
        layer_bias.append([float(entry) for entry in row.split(',')])
        bias.append(np.array(layer_bias).flatten())
    f.readline()
    network.bias = bias

    f.close()

def sigmoid(x):
    """Computes the sigmoid function for input x

    Parameters
    -------
    x : nd.array
        input value to sigmoid
    
    Returns
    --------
        nd.array
            sigmoid output
    """
    return 1 /(1 + np.exp(-x))

def sigmoidPrime(x):
    """Computes the derivative of the sigmoid function
    for input x

    Parameters
    -------
    x : nd.array
        input values to the derivative of the sigmoid function
    
    Returns
    --------
        nd.array
            derivation of the sigmoid function at x
    """
    return sigmoid(x)*(1 - sigmoid(x))

def reLU(x):
    """Computes the rectified linear unit

    Parameters
    --------
        x : nd.array
            input value to the reLU
    Returns
    --------
        nd.array
            reLU output
    """
    return x*(x>0)

def reLUPrime(x):
    """Computes the derivative of the rectified linear unit

    Parameters
    --------
        x : nd.array
            input value to the derivative of reLU
    Returns
    --------
        nd.array
            derivative of reLU
    """
    return 1*(x>0)

def backPropLearning(examples, network, alpha):
    """Trains the neural network using the given parameters

    Parameters
    -------
        examples : list([np.array, np.array])
            training examples for the NN, each with input feature vector
            (index 0) and output target vector (index 1)
        network : NeuralNetwork
            neural network base to start training with
        alpha : float
            learning rate of the neural network, value in range [0, 1]
    Returns
    --------
        NeuralNetwork
            final trained neural network
    """
    loss = []
    random.shuffle(examples)
    for training_pair in examples:
        # Forward Propagate
        z_l, a_l = network.feedForward(training_pair[0])
        
        # Error computation
        loss.append(np.linalg.norm(training_pair[1]-a_l[-1]))
        dW, db = network.backPropagate(training_pair[1], z_l, a_l)
        
        # Back Propagate
        for layer in range(0, network.L-1):
            network.weights[layer] = network.weights[layer] + alpha * dW[layer]
            network.bias[layer] = network.bias[layer] + alpha * db[layer]

    return loss
