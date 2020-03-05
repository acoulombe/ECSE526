import csv

def read_csv(filename):
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

def write_csv(filename, data):
    """function for writing data into a csv file

    Parameters
    --------
        filename : str
            path to csv file to write data to    
        data_arr : dict(float)
           data set in array form
    """
    file = open(filename, 'w')
    csv_writer = csv.writer(file, delimiter=',')
    csv_writer.writerow(data)
    file.close()
