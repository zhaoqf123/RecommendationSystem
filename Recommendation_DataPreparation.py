#! This script extracts a small portion of whole dataset to create a challenge
#! The size of the dataset can be adjusted upon request
import csv as csv
import numpy as np
import matplotlib.pyplot as plt
#import pprint



def id_replace(array, index, dictionary):
#	print array
	position = 0
	for ele in array[:, index]:
#		print ele
#		print array[position, index]
		array[position, index] = str(dictionary[ele])
#		print array[position, index]
#		print
		position = position + 1
	return array
#!	print sorted(np.unique(array[:, index]).astype(int))
#!	print array

def one_index_sort(array, cln):
	return array[array[:, cln].astype(int).argsort(),:]

def two_index_sort(array, cln_1, cln_2):
	ind = np.lexsort((array[:, cln_2].astype(int), array[:, cln_1].astype(int)))
	return array[ind,:]

# The following is to read the input csv file into array
def csv_to_array(file_path_name):
	file_object = open(file_path_name, 'rb')
	csv_file_oject = csv.reader(file_object)
	header = np.array([csv_file_oject.next()])
	csv_file_list = []
	for rows in csv_file_oject:
		csv_file_list.append(rows)
	csv_file_array = np.array(csv_file_list)
	return (header, csv_file_array)

def array_to_csv(array, file_path, header=None):
	open_file_object = open(file_path, 'wb')
	write_file_object = csv.writer(open_file_object)
	write_file_object.writerow(list(header.flatten()))
#	print
#	print header
#	print list(header)
	for row in array:
		write_file_object.writerow(list(row))
	open_file_object.close()

# The following function is to create keys and write the keys into files if the file path is given
def dict_create(keys, file_path = None): # keys is an array of string
	np.random.shuffle(keys) # random shuffle the array
	values = xrange(1,len(keys)+1)
	list_of_turples = zip(keys, values)
	dictionary = dict(list_of_turples)
	if file_path:
		array_to_csv(list_of_turples, file_path, np.array(['orginal_id', 'new_id']))
	return dictionary

# The function below is copied from http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
def chunks(array, granular, arr_len):
	for i in xrange(0, arr_len, granular):
		yield array[i:i+granular]

# This function is designed use stratification method to select sample dataset from whole dataset
# The output would be an array of userId selected as the sample
def select_sample_users(user_movie, granular, selection_pecentage):
	num_select_per_granular = int(round(granular*selection_pecentage/100))
	userId_sorted = user_movie[0, user_movie[1, :].argsort()] # userId is sorted according to the number of movies they watched, from small to large
	num_user = userId_sorted.shape # num_user[0] is the number of users
#	temp = list(chunks(userId_sorted, granular, num_user[0]))
#!	pprint.pprint(temp)
#	user_selected_whole = np.empty([0, 1], dtype=int) # This is strange, the following statement works
	user_selected_whole = np.array([], dtype=int) # Create an empty array to store all selected users
	for ele in chunks(userId_sorted, granular, num_user[0]):
		selected = np.random.choice(ele, num_select_per_granular, replace = False)
#!		print selected
		user_selected_whole = np.concatenate((user_selected_whole, selected))
#!		print ele
#!		print np.random.choice(ele, num_select_per_granular, replace = False)
#!		print
	num_last_granular = num_user[0] % granular
	num_select_last_granular = int(round(num_last_granular * selection_pecentage / 100))
	num_ele_to_delete = num_select_per_granular - num_select_last_granular
	if num_ele_to_delete > 0:
		user_selected_whole = np.delete(user_selected_whole, np.s_[-num_ele_to_delete:])
#!	print num_select_last_granular
#!	print user_selected_whole
	return user_selected_whole

'''This function can be further optimised, and I will take care of this later'''
def select_sample_dataset_ratings(sample_users, csv_file_array, userId_index):
	index_true_false = [] # This list contains the true-flase based on whether the userId is selected
#	print csv_file_array[:, userId_index]
	for userId in csv_file_array[:, userId_index].astype(int):
		index_true_false.append(userId in sample_users)
#	print index_true_false
	csv_file_array_selected = csv_file_array[np.array(index_true_false),:]
	return csv_file_array_selected
#!	for row in csv_file_array_selected:
#!		print row

'''	iterations = int(num_user[0]/granular)
#!	print num_user[0]
	index_0 = 0
	for index in xrange(iterations):
		index_1 = (index + 1)*granular
		print userId_sorted[index_0:index_1]
		index_0 = index_1
	print userId_sorted
#	user_movie = user_movie.transpose()
#	print user_movie
#	print user_movie[user_movie[:, 1].argsort()]
'''
root_path_original_file = "/Volumes/Data/Dextra/KnowledgeChallenge/ml-latest-small"
path_original_file_I = "/ratings.csv" # userId, movieId -> links to other files. This csv file contains the ratings of all movies, it is the main file to be splitted
path_original_file_II = "/movies.csv" # movieId -> links to other files
path_original_file_III = "/links.csv" # movieId -> links to other files
path_original_file_IV = "/tags.csv" # userId, movieId -> links to other files


root_path_new_file = "/Volumes/Data/Dextra/KnowledgeChallenge/ml-latest-small/New"
path_new_file_I = "/new_ratings.csv" # userId, movieId -> links to other files. This csv file contains the ratings of all movies, it is the main file to be splitted
path_new_file_II = "/new_movies.csv" # movieId -> links to other files
path_new_file_III = "/new_links.csv" # movieId -> links to other files
path_new_file_IV = "/new_tags.csv" # userId, movieId -> links to other files

userId_dict_file = "/userId_dict_table.csv"
movieId_dict_file = "/movieId_dict_table.csv"

selection_pecentage = raw_input("Enter the percentage you want to extract from whole dataset, e.g. 40: ") # the prcentage of data to be selected from the whole dataset
selection_pecentage = int(selection_pecentage)

file_path_name = root_path_original_file + path_original_file_I
(header_I, csv_file_array) = csv_to_array(file_path_name)

# The following is to count the unique values in one column of the data
# Here it will count the movies watched by each user
user_cln = csv_file_array[:, 0].astype(int)
unique, counts = np.unique(user_cln, return_counts = True)
user_movie = np.asarray((unique, counts))
#plt.bar(user_movie[0,:], user_movie[1,:])
#plt.show()
#plt.hist(user_movie[1,:], bins = 100)
#plt.show()
#print np.sort(user_movie[1,:])
granular = 10 # Granular here means the minimized size for stratification
# The process is like this: say, there are totally 706 users, each watched some amount of movies,
# ranging from 20 to 2k+, then we sort them from small to large, and take first 10, random select, say 3
# from them, and then take next 10, and repeat the random selection, so on so forth
sample_users = select_sample_users(user_movie, granular, selection_pecentage)
#2 The next step would be to select the sample array from the whole array of ratings based on the slected users
userId_index_I = 0
print sample_users
print sample_users.size
print sample_users[sample_users.argsort()]
print
selected_ratings = select_sample_dataset_ratings(sample_users, csv_file_array, userId_index_I)

#3 This step is to deal with the file tags.csv => The aim is to drop unnecessary users
file_path_name_IV = root_path_original_file + path_original_file_IV
(header_IV, csv_file_array_IV) = csv_to_array(file_path_name_IV)
userId_index_IV = 0
selected_tags = select_sample_dataset_ratings(sample_users, csv_file_array_IV, userId_index_IV)
movieId_index_IV = 1
#!for rows in selected_tags:
#!	print rows

#4 This step is to find out all the unique movieId that appears in the selected sample
movieId_index_I = 1
sample_movies_raw = np.concatenate((selected_ratings[:,movieId_index_I], selected_tags[:,movieId_index_IV]))
# The above sentence appears because some users give some movies tags without rating them
sample_movies = np.unique(sample_movies_raw).astype(int)
print sample_movies[sample_movies.argsort()]
print sample_movies.size
print

#5 This step is to select movies from movies.csv based on selected users => To drop unnecessary movies
file_path_name_II = root_path_original_file + path_original_file_II
(header_II, csv_file_array_II) = csv_to_array(file_path_name_II)
movieId_index_II = 0
selected_movies = select_sample_dataset_ratings(sample_movies, csv_file_array_II, movieId_index_II)
print selected_movies

#6 This step is to select movies from links.csv based on selected users => To drop unnecessary movies
file_path_name_III = root_path_original_file + path_original_file_III
(header_III, csv_file_array_III) = csv_to_array(file_path_name_III)
movieId_index_III = 0
selected_links = select_sample_dataset_ratings(sample_movies, csv_file_array_III, movieId_index_III)
print selected_links

#7 This step is to create a look-up function to replace userId and movieId with userId_new and movieId_new
#7.1 first, create a dictionary for look-up, and the dictionaary will be written into tables if the file path is given
userId_dict = dict_create(sample_users.astype(str), root_path_new_file + userId_dict_file)
movieId_dict = dict_create(sample_movies.astype(str), root_path_new_file + movieId_dict_file)
#7.2 second, look up the selected arrays, replace the keys with the values, start from first file, one by one
#print sorted(map(int, userId_dict.keys()))
'''For file ratings.csv, need two look-up for both userId and movieId'''
selected_ratings = id_replace(selected_ratings, userId_index_I, userId_dict)
selected_ratings = id_replace(selected_ratings, movieId_index_I, movieId_dict)
#print selected_ratings
'''For file movies.csv, need one look-up for movieId'''
selected_movies = id_replace(selected_movies, movieId_index_II, movieId_dict)
print selected_movies
print
'''For file links.csv, need one look-up for movieId'''
selected_links = id_replace(selected_links, movieId_index_III, movieId_dict)
print selected_links
print
'''For file tags.csv, need two look-up for both userId and movieId'''
selected_tags =  id_replace(selected_tags, userId_index_IV, userId_dict)
selected_tags = id_replace(selected_tags, movieId_index_IV, movieId_dict)
print selected_tags
print

#8 This step is to sort the selected arrays according to new userId and new movieId
selected_ratings = two_index_sort(selected_ratings, userId_index_I, movieId_index_I)

selected_movies = one_index_sort(selected_movies, movieId_index_II)

selected_links = one_index_sort(selected_links, movieId_index_III)
print selected_links
print

selected_tags = two_index_sort(selected_tags, userId_index_IV, movieId_index_IV)
print selected_tags

#9 This step is to output the selected sample data in newfiles


array_to_csv(selected_ratings, root_path_new_file + path_new_file_I, header_I)

array_to_csv(selected_movies, root_path_new_file + path_new_file_II, header_II)

array_to_csv(selected_links, root_path_new_file + path_new_file_III, header_III)

array_to_csv(selected_tags, root_path_new_file + path_new_file_IV, header_IV)




