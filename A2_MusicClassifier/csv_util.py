import csv

def read_feature_csv(filename):
    """function for reading the feature data from a csv file

    Parameters
    --------
        filename : str
            path to csv file to read data from
    
    Returns
    --------
        feature_arr : list(list(float))
            value of feature data in array form
    """
    feature_arr = []
    file = open(filename, 'r')
    csv_data = csv.reader(file, delimiter=',')
    for row in csv_data:
        features = []
        for i in range(0, len(row)):
            features.append(float(row[i])) 
        feature_arr.append(features)
    return feature_arr

def read_dict_csv(filename):
    """function for reading the label data from a csv file

    Parameters
    --------
        filename : str
            path to csv file to read data from
    
    Returns
    --------
        data_dict : dict[str](str)
            dictionary with data set as key and label as value
    """
    data_dict = {}
    file = open(filename, 'r')
    csv_data = csv.reader(file, delimiter=',')
    for row in csv_data:
        data_dict[row[0]] = row[1]
    return data_dict

def write_predict_csv(filename, data_arr):
    """function for writing the label of the prediction into a csv file

    Parameters
    --------
        filename : str
            path to csv file to write data to    
        data_arr : list(list(str))
            label of the test data set in array form
    """
    file = open(filename, 'w')
    csv_writer = csv.writer(file, delimiter=',')
    for row in data_arr:
        csv_writer.writerow(row)