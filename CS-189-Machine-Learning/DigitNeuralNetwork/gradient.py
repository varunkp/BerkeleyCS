import numpy as np
import sigmoid
import math

n_out = 10

def mean_error(y, t):
	loss = 0.0
	for k in range(0, n_out):
		loss += np.square((t[k] - y[k]))
	return loss * 0.5

def cross_entropy_error(y, t):
	loss = 0.0
	for k in range(0, n_out):
		yk = y[k]
		tk = t[k]
		loss -= (tk * math.log(yk) + (1-tk) * math.log(1-yk))
	return loss

def mean_squared_gradient(t, W, x, bias):
	# W is d by k
	# x is n by d
	# y should be k by n (k is the number of classes)
	# W_grad is d by k
	# bias is k by 1
	# t is k by n
	t = np.transpose(t)
	W_grad = np.zeros(W.shape)
	bias_grad = np.zeros(bias.shape)
	inp = np.transpose(np.dot(x, W)) + np.transpose(bias)
	sig = sigmoid.sigmoid(inp)
	coeff = (sig-t)*(sig*(1-sig))
	W_grad = np.dot(np.transpose(x),np.transpose(coeff))
	bias_grad = np.sum(coeff,axis =1)
	return W_grad, bias_grad

def cross_entropy_gradient(t, W, x, bias):
	# W is d by k
	# x is n by d
	# y should be k by n (k is the number of classes)
	# W_grad is d by k
	# bias is k by 1
	# t is k by n
	t = np.transpose(t)
	W_grad = np.zeros(W.shape)
	bias_grad = np.zeros(bias.shape)
	inp = np.transpose(np.dot(x, W)) + np.transpose(bias)
	sig = sigmoid.sigmoid(inp)
	coeff = sig - t
	W_grad = np.dot(np.transpose(x),np.transpose(coeff))
	bias_grad = np.sum(coeff,axis =1)
	return W_grad, bias_grad

def mean_squared_gradient_tanh(t, W, x, bias):
	W_grad = np.zeros(W.shape)
	bias_grad = np.zeros(bias.shape)
	for i in range(W.shape[1]):
		w = W[:,i]
		inp = sum(w*x) + bias[0,i]
		if inp > 10: inp = 10
		if inp < -10: inp = -10 
		y = math.tanh(inp)
		if y > .999: y = .999
		if y < .001: y = .001
		coeff = -(t[i]-y)*(1-y**2)
		#print coeff
		W_grad[:, i] = coeff*x
		bias_grad[:, i] = coeff
	'''
	t = np.transpose(t)
	W_grad = np.zeros(W.shape)
	bias_grad = np.zeros(bias.shape)
	inp = np.transpose(np.dot(x, W)) + np.transpose(bias)
	y = np.tanh(inp)
	y[y>10] = 10
	y[y<-10] = -10
	coeff = (t-y)*(1-y**2)
	W_grad = np.dot(np.transpose(x),np.transpose(coeff))
	bias_grad = np.sum(coeff,axis =1)
	'''
	return W_grad, bias_grad

def cross_squared_gradient_tanh(t, W, x, bias):
	W_grad = np.zeros(W.shape)
	bias_grad = np.zeros(bias.shape)
	for i in range(W.shape[1]):
		w = W[:,i]
		inp = sum(w*x) + bias[0,i]
		if inp > 10: inp = 10
		if inp < -10: inp = -10 
		y = math.tanh(inp)
		if y > .999: y = .999
		if y < .001: y = .001
		coeff = -1*(t[i](1-y**2)/y - (1-t[i])*(1+y))
		W_grad[:, i] = coeff*x
		bias_grad[:, i] = coeff
	return W_grad, bias_grad		

