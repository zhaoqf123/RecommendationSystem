#! This script is to split the whole dataset into train, cross-validation and test datasets
import csv as csv
import numpy as np
import time
import DataProcessing as dp
#from DataProcessing import stratification
#from sklearn.cross_validation import StratifiedShuffleSplit as sss
#from sklearn.cross_validation import StratifiedKFold as skf

'''
root_path_old_file = "/Volumes/Data/Dextra/KnowledgeChallenge/ml-latest-small/New"
root_path_new_file = "/Volumes/Data/Dextra/KnowledgeChallenge/ml-latest-small/New/Splitted"
path_old_file = "/new_ratings.csv" # userId, movieId -> links to other files. This csv file contains the ratings of all movies, it is the main file to be splitted
path_new_file_I = "/splitted_ratings.csv"
'''

dp_object = dp.read_write()
(header, array) = dp_object.csv_to_array("./stratification_sample.csv", 'rU')
#print header
#print
#print array
#(header, array) = dp_object.csv_to_array(root_path_old_file + path_old_file)

(train_index, cross_index, test_index) = dp.stratification().one_cln(array[:,0], train = 0.6, cross = 0.15)


# Step 1. Determine the files to be stratified. In this case, only the file ratings.csv should be stratified and splitted
# Step 2. Read csv files into array, check which rows should be used for stratification, and then stratify the rows.
# Step 3. Add noises to the test/validation datasets.




