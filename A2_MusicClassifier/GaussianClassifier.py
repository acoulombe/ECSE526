import csv_util
import probability_util
import numpy as np
import os

# Paths to important files
genre_count = 10
data_path = 'music-classification/kaggle/'
test_set_path = data_path + 'test/'
param_path = 'parameters/'

# Structure IDs to be used
genre_idx = {
    'rnb' : 0,
    'edm_dance' : 1,
    'jazz' : 2,
    'latin' : 3,
    'pop' : 4,
    'kids' : 5,
    'classical' : 6,
    'rock' : 7,
    'country' : 8,
    'metal' : 9
}

idx_to_genre = {
    0 :'rnb',
    1 :'edm_dance',
    2 :'jazz',
    3 :'latin',
    4 :'pop',
    5 :'kids',
    6 :'classical',
    7 :'rock',
    8 :'country',
    9 :'metal'
}

def predictGenre(data_set, means, covariances):
    """Uses the training parameters to predict the most likely genre of the features
    using the unnormalized negative log likelihood (UNLL) for each genre

    Parameters
    --------
        data_set : list(list(float))
            data set of feature vector to predict genre of data, 
            dimensions mxn where m is the number of feature vectors and n is the number of features
        means : list(list(float))
            list of the means vector of each genre,
            list size of number of genres and dimensions 1xn where n is the number of features
        covariances : list(list(list(float)))
            list of the covariance matrix of each genre,
            list size of number of genres and dimensions nxn for matrices where n is the number of features
    
    Returns
    --------
        str
            genre with the highest probability
    """
    unll_vector = [None]*genre_count

    # compute UNLL of each song in the data set for each genre
    for idx in range(0, genre_count):
        for feature_vector in data_set:
            if unll_vector[idx] is None:
                unll_vector[idx] = [computeUNLL(feature_vector, means[idx], covariances[idx])]
            else:
                unll_vector[idx] += [computeUNLL(feature_vector, means[idx], covariances[idx])]
    unll_means = probability_util.compute_means((np.array(unll_vector).T).tolist())

    # find genre with lowest UNLL
    predict_val = float('Inf')
    predict_idx = 0
    for idx in range(0, genre_count):
        if(unll_means[idx]<predict_val):
            predict_val = unll_means[idx]
            predict_idx = idx
    return idx_to_genre[predict_idx]

def computeUNLL(features, means, covariances):
    """Computes the unnormalized negative log likelihood (UNLL) of the feature vector

    Parameters
    --------
        features : list(float)
            feature vector to analyse of dimensions 1xn where n is the number of features
        means : list(float)
            means vector of the genre of dimensions 1xn where n is the number of features
        covariances : list(list(float))
            covariance matrix of the genre of dimensions nxn where n is the number of features
    
    Returns
    --------
        unll : float
            the unnormalized negative log likelihood (UNLL) of the feature vector
    """
    feature_vector = np.array(features)
    mean_vector = np.array(means)
    covariance_matrix = np.array(covariances)
    return np.linalg.multi_dot([feature_vector-mean_vector, np.linalg.inv(covariance_matrix), (feature_vector-mean_vector).T]).astype(float)

def loadParams():
    """Load parameter values generated from training

    Returns
    --------
        mean_vector : list(float)
            vector containing the mean of each of the features of the data set
        covariance_matrix : list(list(float))
            covariance matrix of the features of the data_set
    """
    genre_mean = [0]*genre_count
    genre_covariance = [None]*genre_count

    for genre in genre_idx:
        params = csv_util.read_feature_csv(param_path+genre+'.csv')
        genre_mean[genre_idx[genre]] = params[0]
        genre_covariance[genre_idx[genre]] = params[1:]

    return genre_mean, genre_covariance

if __name__ == "__main__":

    # Load the trained parameters
    genre_means, genre_covariances = loadParams()

    # Load data set to predict
    files = []
    for (dirpath, dirnames, filenames) in os.walk(test_set_path):
        files.extend(filenames)

    # Make progress tracker
    max_count = len(files)
    curr_file_idx = 0

    predictions = [['id','category']]
    # Build data set by reading all training data features and sorting them by genre
    for test_set in files:
        if test_set == 'id':
            continue
        features = csv_util.read_feature_csv(test_set_path+test_set)
        label = predictGenre(features, genre_means, genre_covariances)
        predictions.append([test_set, label])

        # Print Progress
        curr_file_idx += 1
        print(f'Progress : %{curr_file_idx/max_count*100}', end='\r')

    csv_util.write_csv('predictions.csv', predictions)