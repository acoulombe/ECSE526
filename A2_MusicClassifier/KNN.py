import probability_util
import csv_util
import numpy as np
import os

data_path = 'music-classification/kaggle/'
test_set_path = data_path + 'test/'
training_set_path = data_path + 'training/'
labels_file = "labels.csv"

K = 13              # Number of nearest neighbors to use
weight = True       # use weighted K-NN?

def predictGenre(sample_features, labeled_data, labels, k):
    """Predicts the genre of the song using the K-Nearest Neighbors algorithm

    Parameters
    --------
        sample_features : list(list(float))
            data set of feature vector to predict genre of data, 
            dimensions mxn where m is the number of feature vectors and n is the number of features
        labeled_data : list(list(float))
            data set of labeled feature vectors used to make predictions on the genre of input features, 
            dimensions mxn where m is the number of feature vectors and n is the number of features
        k : int
            number of nearest neighbors to use for prediction

    Returns
    --------
        str
            genre with the highest probability    
    """
    # Get mean of the features to predict
    input_means = probability_util.compute_means(sample_features)

    # Get means of each song
    data_means = []
    for song in labeled_data:
        song_mean = probability_util.compute_means(song)
        data_means.append(song_mean)

    data_matrix = np.array(data_means)
    input_vector = np.array(input_means)

    # Compute distances from sample to points in data set
    data_matrix = data_matrix - input_vector
    data_matrix = np.square(data_matrix)
    data_matrix = data_matrix.sum(axis=1).T

    # Find K nearest neighbors
    idx = np.argpartition(data_matrix, k)

    # Find majority vote of neighbors
    genre_vote= {
    'rnb' : 0,
    'edm_dance' : 0,
    'jazz' : 0,
    'latin' : 0,
    'pop' : 0,
    'kids' : 0,
    'classical' : 0,
    'rock' : 0,
    'country' : 0,
    'metal' : 0
    }
    for p in range(0, k):
        if weight: 
            if(data_matrix[idx[p]]==0):
                genre_vote[labels[idx[p]]] += float("Inf")
            else:
                genre_vote[labels[idx[p]]] += 1/data_matrix[idx[p]]
        else: genre_vote[labels[idx[p]]] += 1

    max_genre = max(genre_vote.keys(), key=(lambda v: genre_vote[v]))

    return max_genre


if __name__ == "__main__":
    # ==================================== PREPARATION STAGE ============================

    # Make structures for holding relevant data
    genre_training_set = []
    training_set_labels = {}

    file_labels = csv_util.read_dict_csv(data_path+labels_file)

    # Make progress tracker
    max_count = len(file_labels)
    curr_file_idx = 0

    # Build data set by reading all training data features and sorting them by genre
    for training_set in file_labels:
        if training_set == 'id':
            continue
        features = csv_util.read_feature_csv(training_set_path+training_set)
        genre_training_set.append(features)
        training_set_labels[curr_file_idx] = file_labels[training_set]

        # Print Progress
        curr_file_idx += 1
        print('Loading data: %{:,.2f}'.format(curr_file_idx/max_count*100), end='\r')

    # ========================== PREDICTION STAGE =======================================
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
        label = predictGenre(features, genre_training_set, training_set_labels, K)
        predictions.append([test_set, label])
        
        # Print Progress
        curr_file_idx += 1
        print('Progress : %{:,.2f}      '.format(curr_file_idx/max_count*100), end='\r')

    print(f"Generating file 'predictions.csv'", end='\r')
    csv_util.write_csv('predictions.csv', predictions)
    print(f"Generated file 'predictions.csv'")
