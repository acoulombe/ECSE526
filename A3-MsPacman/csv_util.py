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
    data = []
    file = open(filename, 'r')
    csv_data = csv.reader(file, delimiter=',')
    for row in csv_data:
        element = []
        for i in range(0, len(row)):
            element.append(int(row[i])) 
        data.append(element)
    return data

def write_csv(filename, data_arr):
    """function for writing data into a csv file

    Parameters
    --------
        filename : str
            path to csv file to write data to    
        data_arr : list(list(str))
           data set in array form
    """
    file = open(filename, 'w')
    csv_writer = csv.writer(file, delimiter=',')
    for row in data_arr:
        csv_writer.writerow(row)
    file.close()
