import numpy
import scipy.io as sci
import random
import rf
import id3
import csv
import adaboost
data = sci.loadmat('spam.mat')

Xtrain = data['Xtrain']
ytrain = data['ytrain']
Xtest = data['Xtest']

attributes = set(range(57))

def kaggle_submit:
	trees = rf.raise_forest(Xtrain, ytrain, 100, Xtrain.shape[0], len(attributes))
	[ensemble_error, ensemble_pred] = rf.ensemble(Xtest, None, trees)
	with open ('test_set_predictions.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
		for i in xrange(Xtest.shape[0]):
			writer.writerow([str(i), str(ensemble_pred[i])])

k = 4
set_size = Xtrain.shape[0] / k

perm_ind = random.sample(xrange(Xtrain.shape[0]), Xtrain.shape[0])



partitions = []
label_partitions = []
for i in xrange(k):
	block = (i+1) * set_size
	partitions.append([])
	label_partitions.append([])
	partitions[i] = Xtrain[perm_ind[block - set_size:block]]
	label_partitions[i] = ytrain[perm_ind[block - set_size:block]]
error = [0,0,0]

for j in xrange(k):
	adaboost_rounds = 100
	print j
	sets = range(k)
	del(sets[j])
	#train on k-1 sets, test on last set
	training_block = numpy.vstack(([partitions[i] for i in sets]))
	training_label_block = numpy.vstack(([label_partitions[i] for i in sets]))
	test_block = partitions[j]
	test_label_block = label_partitions[j] 
	train_examples = zip(training_block, training_label_block.T.tolist()[0])
	test_examples = zip(test_block, test_label_block.T.tolist()[0])

	#cross validation for random forest
	print "Cross Validating Random Forest..."
	train_size = int(training_block.shape[0])
	att_size = int(len(attributes))
	forest_size = 100
	[ensemble_error, ensemble_pred] = rf.ensemble(test_block, test_label_block, rf.raise_forest(training_block,training_label_block, forest_size, train_size, att_size))
	error[0]+= (1.0/k) * ensemble_error

	#cross validation for decision tree
	print "Cross Validating Decision Tree..."
	dec_tree = id3.id3(train_examples, attributes)
	dec_tree_errors = 0
	for i in xrange(len(test_block)):
		if id3.classify(dec_tree, test_block[i]) != test_label_block[i]:
			dec_tree_errors += 1
	error[1] += (1.0/k) * (float(dec_tree_errors) / set_size)

	print "Cross Validating AdaBoost..."
	adaboost_classifier = adaboost.adaboost(train_examples, adaboost_rounds)
	adaboost_errors = 0
	for i in xrange(len(test_block)):
		if adaboost.classify(adaboost_classifier, test_block[i]) != test_label_block[i]:
			adaboost_errors += 1
	error[2] += (1.0/k) * (float(adaboost_errors) / set_size)



print (1-error[0]), (1-error[1])
print 'Estimated accuracy of Random Forest:', (1-error[0])
print 'Estimated accuracy of Decision Tree:', (1-error[1])
print 'Estimated accuracy of AdaBoost:', (1-error[2])
	
