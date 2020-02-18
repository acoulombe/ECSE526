# Assignment 2 - Music Classifier

### Dependencies

The only external module used by this software program is numpy. The dependency can be easily downloaded by using pip to install the module in your python environment or a python virtual environment as follows:
```
pip install numpy
```

### Gaussian Classifier

The code of the assignment is in three main scripts and two helper modules. The Gaussian classifier has two scripts, _trainGaussian.py_ and _GaussianClassifier.py_. The _trainGaussian.py_  loads the data set in the training subdirectory and places the parameters of the classifier after training the model in the parameters/ subdirectory. The file hierarchy needed for the scripts to find their dependencies is the following :
```
Music-Classifier
	- trainGaussian.py
	- GaussianClassifier
	- KNN.py
	- csv_util.py
	- probability_util.py
	- parameters/
	- music-classification/kaggle/
			- labels.csv
			- training/
			- test/
```

Once the Gaussian model is trained with the data in the file _labels.csv_ and music-classification/kaggle/training/, the script _GaussianClassifier.py_ can be run and generate the _predictions.csv_ file with the predictions of the labels of the music-classification/kaggle/test/ data set. The scripts should be run in the following fashion using python 3.7 or higher (the scripts take some time to run, but a progress bar is integrated into the terminal to show the programs progress):
```
python trainGaussian.py
python GaussianClassifier.py
```

### K-Nearest Neighbours

The K-Nearest Neighbours (KNN) algorithm is implement in the _KNN.py_ script. It can be run easily by just calling the script as follows: 
```
python KNN.py
```

The script will generate the _predictions.csv_ file which contains all the labels the algorithm predicts for the  the music-classification/kaggle/test/ data set.

In order to change the value of k or to toggle the weighted KNN algorithm, simply open the script to edit the variables at the top of the script. The variables _k_ and _weight_ control these options. _k_ tells the algorithm how many nearest neighbours to use and is an integer value. _weight_ is a boolean value that tells the algorithm whether to use weights (true) or not (false).