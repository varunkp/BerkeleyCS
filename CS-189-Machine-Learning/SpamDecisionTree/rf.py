import scipy.io as sio
import numpy
import math
import random
import preprocess as pp
import id3

attributes = numpy.array(xrange(57))

def sample_with_rep(points, subset_size):
	sample_ind = [random.random() * points.shape[0] for i in xrange(subset_size)]
	samples = points[sample_ind]
	return samples, sample_ind	
#Grow trees
def raise_forest(Xtrain, ytrain, n, train_size, att_size):
	print "Raising forest with " + str(n) + " trees"
	trees = []
	for i in xrange(n):
		sub_train_x, sub_train_ind = sample_with_rep(Xtrain, train_size)	
		sub_train_y = ytrain[sub_train_ind]
		examples = [(sub_train_x[i], sub_train_y[i]) for i in xrange(len(sub_train_ind))]
		sub_att, sub_att_ind = sample_with_rep(attributes,att_size)
		sub_att = set(sub_att)
		trees.append(id3.id3(examples, sub_att))	
	return trees

def ensemble(Xtest, ytest, trees):
	error = 0
	predictions = []

	ensemble_pred = []
	for i in xrange(Xtest.shape[0]):
		example = Xtest[i]
		predictions.append({})
		for j in xrange(len(trees)):
			curr_pred = id3.classify(trees[j],example)
			if curr_pred not in predictions[i]:
				predictions[i][curr_pred] = 1
			else:
				predictions[i][curr_pred] += 1
			
		ensemble_pred.append(max(predictions[i],key = predictions[i].get))	

	for i in xrange(len(ensemble_pred)):
		if ensemble_pred[i] != ytest[i]:
			error +=1
	return float(error) / float(len(Xtest))


data = sio.loadmat('spam.mat')
Xtrain = data['Xtrain']
ytrain = data['ytrain']
Xtest = data['Xtest']
#raise_forest(Xtrain,ytrain,100)
#ensemble(Xtrain, ytrain, raise_forest(Xtrain, ytrain, 100))

if __name__ == '__main__':
	### the following  3 lines can be modified as needed to input the test set ###
	file_name = sys.argv[1]
	data = sio.loadmat(file_name)
	Xtest = data['Xtest']
	########################################################################
	output_file = sys.argv[2]
	if len(sys.argv) > 3:
		n = int(sys.argv[3])
	else:
		n = 100

	print 'Learning...'
	forest = adaboost(Xtrain, ytrain, n, len(Xtrain), 57)
	print 'Classifying...'
	predictions = []

	ensemble_pred = []
	for i in xrange(Xtest.shape[0]):
		example = Xtest[i]
		predictions.append({})
		for j in xrange(len(trees)):
			curr_pred = id3.classify(trees[j],example)
			if curr_pred not in predictions[i]:
				predictions[i][curr_pred] = 1
			else:
				predictions[i][curr_pred] += 1

	print 'Writing to', output_file
	with open(output_file, 'wb') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow(['Id', '|' 'Category'])
		for index, classification in enumerate(ensemble_pred):
			filewriter.writerow([index+1, '|', classification])
	print 'Done writing to', output_file




