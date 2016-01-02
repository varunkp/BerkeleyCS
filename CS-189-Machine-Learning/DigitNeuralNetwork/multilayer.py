import numpy as np
import random
import gradient as gr
import time
import sys
import csv

N_IN = 784
N1_HID = 300
N2_HID = 100
N_OUT = 10 


class NeuralNet(object):

	def __init__(self):
		self.w1_hid = np.zeros((N_IN, N1_HID))
		self.w2_hid = np.zeros((N1_HID, N2_HID))
		self.w_out = np.zeros((N2_HID, N_OUT))
		self.b1_hid = np.zeros((1, N1_HID))
		self.b2_hid = np.zeros((1, N2_HID))
		self.b_out = np.zeros((1, N_OUT))
		self.delta_outs = np.zeros((1, N_OUT))
		self.delta_2 = np.zeros((1, N2_HID))
		self.delta_1 = np.zeros((1, N1_HID))

	def randomly_initialize(self):
		self.w1_hid = (np.random.random((N_IN, N1_HID)) - 0.5)/10
		self.w2_hid = (np.random.random((N1_HID, N2_HID)) - 0.5)/10
		self.w_out = (np.random.random((N2_HID, N_OUT)) - 0.5)/10
		self.b1_hid = np.random.random((1, N1_HID))/10
		self.b2_hid = np.random.random((1, N2_HID))/10
		self.b_out = np.random.random((1, N_OUT))/10

	def classify(self, x):
		#change to TANH!!!!!!
		W1_bias = np.vstack((self.w1_hid, self.b1_hid))
		x1_bias = np.append(x, [1])
		y = np.tanh(np.transpose(np.dot(x1_bias,W1_bias)))

		def squash_y(el):
			if el > .999: return .999
			if el < .001: return .001
			return el 

		squash_y = np.vectorize(squash_y)
		x2 = squash_y(y)


		W2_bias = np.vstack((self.w2_hid, self.b2_hid))
		x2_bias = np.append(x2, [1])
		y = np.tanh(np.transpose(np.dot(x2_bias,W2_bias)))
		x3 = squash_y(y)

		W_out_bias = np.vstack((self.w_out, self.b_out))
		x3_bias = np.append(x3, [1])
		y = np.tanh(np.transpose(np.dot(x3_bias,W_out_bias)))

		y = squash_y(y)
		return (x, x2, x3, y)

	def train_multilayer_SGD(self, y, x, eta_0, num_epochs, test_y, test_x):
		self.randomly_initialize()
		f = open('performance.csv', 'wb')
		fwriter = csv.writer(f, delimiter=',')
		fwriter.writerow(['Epoch Number', 'Time Elapsed', 'Training Accuracy (10k set)', 'Test Accuracy', 'Mean Squared Error','Cross Entropy Error', 'Eta', 'Num_epochs'])
		fwriter.writerow(['', '', '', '', '','','','' ,str(eta_0), str(num_epochs)])
		batch_size = 200	
		indices = range(x.shape[0])
		t = [0] * 10
		t_mat = np.zeros((10, y.shape[0])) 

		x_batch = np.zeros((batch_size, x.shape[1]))
		y_batch = np.zeros((batch_size,))
		for j in xrange(t_mat.shape[1]):
			t_mat[y[j],j] = 1
		step = 0

		start = time.clock()
		for i in xrange(num_epochs):
			eta = eta_0/((i+1)**0.5)
			random.shuffle (indices)
			print "Epoch " + str(i)
			for batch in xrange(x.shape[0]/ batch_size):
				W_out_grad_sum = np.zeros((N2_HID, N_OUT))
				W2_hid_grad_sum = np.zeros((N1_HID, N2_HID))
				W1_hid_grad_sum = np.zeros((N_IN, N1_HID))
				bias_out_grad_sum = np.zeros((1,10))
				bias_h2_grad_sum = np.zeros((1, N2_HID))
				bias_h1_grad_sum = np.zeros((1, N1_HID))

				chunk = indices[batch_size * batch: batch_size * (batch + 1)]
				x_batch = x[chunk, :] 
				y_batch =  y[chunk] 
				for j in xrange(x_batch.shape[0]):
					t0 = time.clock() 
					t[y_batch[j]] = 1
					temp_x = x_batch[j,:]
					(x1, x2, x3, output) = self.classify(x_batch[j,:])

					t1 = time.clock()
					(W_out_grad, bias_out_grad) = gr.mean_squared_gradient_tanh(t,self.w_out,x3,self.b_out)
					t15 = time.clock()

					W_out_grad_sum += W_out_grad #weight updates for W_out
					bias_out_grad_sum += bias_out_grad #updates for bias terms
					temp_out_deltas = bias_out_grad #delta terms for output layer
					t[y_batch[j]] = 0

					temp_h2_deltas = np.zeros((1, N2_HID))
					temp_h2_deltas = (1-x3**2)*np.sum(self.w_out*temp_out_deltas, axis=1)
					temp_h2_deltas = np.reshape(temp_h2_deltas, (1, N2_HID))
					bias_h2_grad_sum += temp_h2_deltas #update second layer bias running sum
					W2_hid_temp_grad = np.zeros((N1_HID, N2_HID))

					W2_hid_temp_grad = temp_h2_deltas*np.transpose(np.reshape(x2, (1, x2.shape[0])))
					W2_hid_grad_sum += W2_hid_temp_grad
					temp_h1_deltas = np.zeros((1, N1_HID))

					temp_h1_deltas = (1-x2**2)*np.sum(self.w2_hid*temp_h2_deltas, axis=1)
					temp_h1_deltas = np.reshape(temp_h1_deltas, (1, N1_HID))
					W1_hid_temp_grad = np.zeros((N_IN, N1_HID))

					W1_hid_temp_grad = temp_h1_deltas*np.transpose(np.reshape(x1, (1, x1.shape[0])))
					W1_hid_grad_sum += W1_hid_temp_grad

					bias_h1_grad_sum += temp_h1_deltas #update first layer bias running sum


				W_new = self.w_out - np.multiply(eta, W_out_grad_sum)
				#print 'W_new', W_new
				self.w_out = W_new
				bias_new = self.b_out - np.multiply(eta, bias_out_grad_sum)
				self.b_out = bias_new

				W_new = self.w2_hid - np.multiply(eta, W2_hid_grad_sum)
				self.w2_hid = W_new
				bias_new = self.b2_hid - np.multiply(eta, bias_h2_grad_sum)
				self.b2_hid = bias_new

				#update first hidden layer weights + bias
				W_new = self.w1_hid - np.multiply(eta, W1_hid_grad_sum)
				self.w1_hid = W_new
				bias_new = self.b1_hid - np.multiply(eta, bias_h1_grad_sum)
				self.b1_hid = bias_new
		#y is a d by n matrix

			if i % 10 == 0:
				y_class = self.classify(x[10,:])[-1]
				print y_class, y[10]

				y_ret, J_ret, acc_ret = self.test_classification(y, x)
				test_y_ret, test_J_ret, acc_ret_test = self.test_classification(test_y, test_x)

				fwriter.writerow([str(i+1), str(time.clock() -start), str(acc_ret), str(acc_ret_test), test_J_ret,'n/a', '', ''])
					
				print 'Error', J_ret
				print 'accuracy', acc_ret
				np.savetxt('Eta' + str(eta_0) + 'w_out_weights.txt', self.w_out)
				np.savetxt('Eta' + str(eta_0) + 'w2_hid_weights.txt', self.w2_hid)
				np.savetxt('Eta' + str(eta_0) + 'w1_hid_weights.txt', self.w1_hid)
				np.savetxt('Eta' + str(eta_0) + 'bias_out.txt', self.b_out)
				np.savetxt('Eta' + str(eta_0) + 'bias_1_hidden.txt', self.b1_hid)
				np.savetxt('Eta' + str(eta_0) + 'bias_2_hidden.txt', self.b2_hid)

	def classify_majority(self, y):
		""" Take in output from classify and assign it to a digit using majority"""

		y_maj = np.zeros(y.shape)
		majority_indices = np.argmax(y, axis =0)
		for i in range(y.shape[1]):
			y_maj[majority_indices[i]][i] = 1
		return y_maj

	def test_classification(self, y, x):
		#y_class = classify(x, W, b)

		y_class = np.zeros((y.shape[0], 10))
		x_example = self.classify(x[0,:])

		for i in xrange(x.shape[0]):
			curr_x = x[i,:]
			curr_y = self.classify(curr_x)[-1]
			y_class[i, :] = curr_y
		y_class = np.transpose(y_class)
		y_class_maj= self.classify_majority(y_class)
		y_class_label = np.argmax(y_class_maj,axis = 0)					
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




