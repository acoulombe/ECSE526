import random
import csv_util

# Get Database
raw_data_set = csv_util.read_csv('PointCloudDetection.csv')

random.shuffle(raw_data_set)

true_count = 0
samples_true = []
false_count = 0
samples_false = []

for data in raw_data_set:
    if data[-1] == 0 and false_count < 2500:
        false_count += 1
        samples_false.append(data)
    elif data[-1] == 1 and true_count < 2500:
        true_count += 1
        samples_true.append(data)
    if false_count >= 2500 and true_count >= 2500:
        break

csv_util.write_csv('CollisionSet.csv', samples_false+samples_true)
