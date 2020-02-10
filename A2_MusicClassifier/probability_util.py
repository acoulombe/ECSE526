import numpy as np

def compute_means(data_set):
    """Computes the mean of each of the features independently in the data set

    Parameters
    --------
        data_set : list(list(str/float/int))
            data set containing the values of the features 
            values of set need to be convertable to floats

    Exceptions
    --------
        ValueError : thrown when the data in the set is not convertible to float

    Returns
    --------
        mean_vector : list(float)
            vector containing the mean of each of the features of the data set
    """
    mean_vector = [0] * len(data_set[0])
    
    for set_idx in range(0, len(data_set)):
        for feature_idx in range(0, len(data_set[0])):
            mean_vector[feature_idx] = set_idx/(set_idx+1)*mean_vector[feature_idx]+1/(set_idx+1)*float(data_set[set_idx][feature_idx])
    
    return mean_vector

def compute_covariance(data_set):
    """Computes the covariance matrix of the data set

    Parameters
    --------
        data_set : list(list(float/int))
            data set containing the values of the features 
            values of set need to be convertable to floats

    Returns
    --------
        covariance_matrix : list(list(float))
            covariance matrix of the features of the data_set
    """
    data = np.asmatrix(data_set)
    return np.cov(data.T).tolist()

