import numpy as np
import scipy.io as sio
import gradient as gr
import prepare_data as pre
import sigmoid
import random
import math
import time
import csv
import datetime
import sys

timing = False

# t0 = time.clock() 
# train_small = sio.loadmat('train_small.mat')
# train = sio.loadmat('train.mat')
# test = sio.loadmat('test.mat')
# t1 = time.clock()

# if timing:
# 	print 'Load time ' + str(t1 - t0)
# 	print t0
# 	print t1

# train_small_data = train_small['train']
# train_data = train['train']
# test_data = test['test']

# t0 = time.clock() 

# (features, labels) = pre.prepare_train_data(train_small_data)
# (x_train, y_train) = pre.prepare_test_data(train_data)
# (x_test, y_test) = pre.prepare_test_data(test_data)

# t1 = time.clock()


# if timing:
# 	print 'Prepare data time ' + str(t1 - t0)

def classify(x,W,b):
	W_bias = np.vstack((W,b))
	ones = np.ones((x.shape[0],1))
	x_bias = np.hstack((x, ones))
	inp = np.dot(x_bias,W_bias)
	y = np.transpose(sigmoid.sigmoid(inp))
	y[y>.999] = .999
	y[y<.001] = .001
	return y

def classify_majority(y):
	""" Take in output from classify and assign it to a digit using majority"""
	y_maj = np.zeros(y.shape)
	majority_indices = np.argmax(y, axis =0)
	for i in range(y.shape[1]):
		y_maj[majority_indices[i]][i] = 1
	return y_maj

def test_classification(y, x, W, b):
	y_class = classify(x, W, b)

	y_class_maj= classify_majority(y_class)
	y_class_label = np.argmax(y_class_maj,axis = 0)					
	np.savetxt('classifications.txt',y_class_label, fmt = '%4.1f')
	np.savetxt('truth.txt', y,fmt= '%4.1f') 
	t = [0] * 10
	t_mat = np.zeros((10, y.shape[0])) 
	for j in xrange(t_mat.shape[1]):
		t_mat[y[j],j] = 1

	J = 0.5 * (t_mat - y_class) ** 2
			
	error = np.sum(J)
	misclassifications = []
	for i in xrange(y_class_maj.shape[1]):
		misclassifications.append((t_mat[:,i] == y_class_maj[:,i]).all())
	accuracy = 1.0 * sum(misclassifications) / len(misclassifications)
	return (y_class_maj, error, accuracy)

def SGD (y,x, eta_0, num_epochs, error_type):
	t0 = time.clock()
	f = open('performance.csv', 'wb')
     	fwriter = csv.writer(f, delimiter=',')
	fwriter.writerow(['Epoch Number', 'Time Elapsed', 'Training Accuracy (10k set)', 'Test Accuracy', 'Mean Squared Error','Cross Entropy Error', 'Eta', 'Num_epochs'])  
	fwriter.writerow(['', '', '', '', '','',str(eta_0), str(num_epochs)])  
	W_old = np.random.random((784,10)) -.5 
	bias_old = np.random.random((1,10)) -.5
	batch_size = 200	
	indices = range(x.shape[0])
	t = [0] * 10
	t_mat = np.zeros((10, y.shape[0])) 

	x_batch = np.zeros((batch_size, x.shape[1]))
	y_batch = np.zeros((batch_size,))
	for j in xrange(t_mat.shape[1]):
		t_mat[y[j],j] = 1

	t_mat_trans = np.transpose(t_mat)	
	t1 = time.clock()
	start = time.clock()
			
	for i in xrange(num_epochs):
		print "Epoch " + str(i+1)
		random.shuffle (indices)
		eta = eta_0 * (1.0/math.sqrt(i+1))

		t0_outer = time.clock()

		for batch in xrange(x.shape[0]/ batch_size):
			chunk = indices[batch_size * batch: batch_size * (batch + 1)]
			x_batch = x[chunk, :] 
			y_batch = y[chunk]
			t_batch = t_mat_trans[chunk,:]
			t0 = time.clock()
			if str(error_type) == 'cse':
				(W_grad, bias_grad) = gr.cross_entropy_gradient(t_batch, W_old, x_batch, bias_old)
			elif str(error_type) == 'mse':
				(W_grad, bias_grad) = gr.mean_squared_gradient(t_batch, W_old, x_batch, bias_old)
			else:
				print 'WRONG INPUT'
			W_new = W_old - np.multiply(eta, W_grad)
			W_old = W_new
			bias_new = bias_old - np.multiply(eta, bias_grad)
			bias_old = bias_new

		t1_outer = time.clock()

		if timing:
			print 'Runtime of epoch: ' + str(t1_outer - t0_outer)

		#y is a d by n matrix
		if (i+1) % 1 == 0:	
			y_class = classify(x, W_new, bias_new)
			MSE = 0.5 * (t_mat - y_class) ** 2
			MSE = np.sum(MSE)
			logy = np.log(y_class)
			CEE = -(t_mat* logy + (1-t_mat) * (1-logy))
			CEE = np.sum(CEE)
			y_ret, J_ret, acc_ret = test_classification(y_train, x_train, W_new, bias_new)
			y_ret_test, J_ret_test, acc_ret_test = test_classification(y_test, x_test, W_new, bias_new)
			fwriter.writerow([str(i+1), str(time.clock() -start), str(acc_ret), str(acc_ret_test), str(MSE),str(CEE), '', ''])
			# print 'TRAINING ACCURACY ' + str(acc_ret)
			# print 'TEST ACCURACY ' + str(acc_ret_test)
			# print 'ERROR ' + str(MSE)
			np.savetxt('Eta' + str(eta_0) + 'weights.txt', W_new)
			np.savetxt('Eta' + str(eta_0) + 'bias.txt', bias_new)

	return (W_new, bias_new)

# (weights_ret, bias_ret) = SGD(y_train, x_train, .01, 500)
# #(weights_ret, bias_ret) = SGD(labels[3], features[3], .6, 50)

# print "-----------------------------WEIGHTS----------------------------"
# print weights_ret
# print "-----------------------------BIAS----------------------------"
# print bias_ret

# np.savetxt('weights.txt', weights_ret)
# np.savetxt('bias.txt', bias_ret)


# print "-----------------------------STARTING TESTING----------------------------"
# # weights_ret = np.loadtxt('weights.txt')
# # bias_ret = np.loadtxt('bias.txt')

# y_ret, J_ret, acc_ret = test_classification(y_test, x_test, weights_ret, bias_ret)
# print "-----------------------------PREDICTED LABELS----------------------------"
# print y_ret
# print "-----------------------------ERROR----------------------------"
# print J_ret
# print "-----------------------------ACCURACY----------------------------"
# print acc_ret


if __name__ == '__main__':

	train_small = sio.loadmat('train_small.mat')
	train = sio.loadmat('train.mat')
	test = sio.loadmat('test.mat')
	train_small_data = train_small['train']
	train_data = train['train']
	test_data = test['test']
	(features, labels) = pre.prepare_train_data(train_small_data)
	(x_train, y_train) = pre.prepare_test_data(train_data)
	(x_test, y_test) = pre.prepare_test_data(test_data)


	xTrain = eval(sys.argv[1])
	yTrain = eval(sys.argv[2])
	num_epochs = int(eval(sys.argv[4]))
	learning_rate = eval(sys.argv[3])
	error_type = sys.argv[5]


	(weights_ret, bias_ret) = SGD(yTrain, xTrain, learning_rate, num_epochs, error_type)

	np.savetxt('weights.txt', weights_ret)
	np.savetxt('bias.txt', bias_ret)
	
	y_ret, J_ret, acc_ret = test_classification(y_test, x_test, weights_ret, bias_ret)
	print acc_ret



