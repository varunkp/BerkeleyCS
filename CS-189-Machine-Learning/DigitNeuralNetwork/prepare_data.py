import scipy.io as sio
import numpy as np


train_small = sio.loadmat('train_small.mat')
train = sio.loadmat('train.mat')
test = sio.loadmat('test.mat')

train_small_data = train_small['train']
train_data = train['train']
test_data = test['test']


def prepare_train_data(data):

	labels = []
	flattened = []
	features = []
	images = []
	images_norm = [0] * 7
	for i in range(7):
		labels.append(np.array([int(el[0]) for el in data[0][i][0][0][1]]))
		# labels.append(1.0 * data[0][i][0][0][1])
		images.append(1.0 * data[0][i][0][0][0])
		#print images[0].shape
		#print labels[0].shape
		# images.append(1.0 * np.array([float(el[0]) for el in data[0][i][0][0][0]]))
		reshaped = np.reshape(images[i], (784, labels[i].shape[0]))
		reshaped = np.transpose(reshaped) 

		#Center around 0, normalized
		mean = np.mean(reshaped, axis = 1)
		std = np.std(reshaped, axis =1)
		for k in xrange(std.shape[0]):
			if std[k] == 0: 
				std[k] = 1				
		reshaped = reshaped - mean[:,None]
		reshaped_normalized = reshaped / std[:,None]

		#reshaped_normalized = 1.0 * reshaped / sum(reshaped)
		reshaped_normalized = np.transpose(reshaped_normalized)
		flattened.append(reshaped_normalized)
		features.append(np.transpose(flattened[i]))

	return (features, labels)
def prepare_test_data(data):

       labels = data[0][0][1]
       images = 1.0 * data[0][0][0]
       reshaped = np.reshape(images, (784, labels.shape[0]))
       mean = np.mean(reshaped, axis = 0)
       std = np.std(reshaped, axis = 0)
       mean = np.transpose(mean)
       std = np.transpose(std)
       reshaped = np.transpose(reshaped)
       """       print "--------------TESTING MEAN-----------"

       print mean
       print mean.shape
       print std.shape"""
       for k in xrange(std.shape[0]):
               if std[k] == 0:
                       std[k] = 1                                
       reshaped = reshaped - mean[:,None]
       reshaped_normalized = reshaped / std[:,None]        

       features = reshaped_normalized

       return (features, labels)

"""def prepare_test_data(data):
	labels = data[0][0][1]
	images = 1.0 * data[0][0][0]
	reshaped = np.reshape(images, (784, labels.shape[0]))
	mean = np.mean(reshaped, axis = 0)
	std = np.std(reshaped, axis =0)

	for k in xrange(std.shape[0]):
		if std[k] == 0 and mean[k] == 0:
			std[k] = 1				
	reshaped = reshaped - mean[:,None]
	reshaped_normalized = reshaped / std[:,None]	

	flattened = reshaped_normalized
	features = np.transpose(flattened)

	return (features, labels)

f1, l1 = prepare_train_data(train_small_data)
print f1[0].shape
print l1[0].shape
f, l = prepare_test_data(test_data)
print f.shape
print l.shape"""
	
