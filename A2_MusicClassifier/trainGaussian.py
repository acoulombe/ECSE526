import csv_util
import probability_util

data_path = 'music-classification/kaggle/'
training_set_path = data_path + 'training/'
parameter_path = 'parameters/'
labels_file = "labels.csv"

genre_count = 10
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

genre_param_filename = [
    'rnb.csv',
    'edm_dance.csv',
    'jazz.csv',
    'latin.csv',
    'pop.csv',
    'kids.csv',
    'classical.csv',
    'rock.csv',
    'country.csv',
    'metal.csv'
]

if __name__ == "__main__":
    genre_training_sets = [None]*genre_count
    genre_mean = [0]*genre_count
    genre_covariance = [None]*genre_count

    file_labels = csv_util.read_dict_csv(data_path+labels_file)
    
    # Build data set by reading all training data features and sorting them by genre
    for training_set in file_labels:
        if training_set == 'id':
            continue
        features = csv_util.read_feature_csv(training_set_path+training_set)
        if genre_training_sets[genre_idx[file_labels[training_set]]] is None:
            genre_training_sets[genre_idx[file_labels[training_set]]] = features    # Add features to the right genre
        else:
            genre_training_sets[genre_idx[file_labels[training_set]]] += features    # Add features to the right genre

    # Compute the means and covariance matrix of each genre and save to csv file
    for idx in range(0, genre_count):
        genre_mean[idx] = probability_util.compute_means(genre_training_sets[idx])
        genre_covariance[idx] = probability_util.compute_covariance(genre_training_sets[idx])
        csv_util.write_csv(parameter_path+genre_param_filename[idx], [genre_mean[idx]]+genre_covariance[idx])
