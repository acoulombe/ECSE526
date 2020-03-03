import csv

def read_csv(filename):
    """function for reading the data from a csv file

    Parameters
    --------
        filename : str
            path to csv file to read data from
    
    Returns
    --------
        data : list(list(int))
            value of feature data in array form
    """
    data = {}
    file = open(filename, 'r')
    csv_data = csv.reader(file, delimiter=',')
    for row in csv_data:
        data[row[0]] = float(row[1]) 
    return data

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
    for key in data:
        csv_writer.writerow([key, data[key]])
    file.close()
