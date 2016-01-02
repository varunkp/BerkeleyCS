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
import multilayer
train_small = sio.loadmat('train_small.mat')
train = sio.loadmat('train.mat')
test = sio.loadmat('test.mat')

train_small_data = train_small['train']
train_data = train['train']
test_data = test['test']

(features, labels) = pre.prepare_train_data(train_small_data)
(x_test, y_test) = pre.prepare_test_data(test_data)

if __name__ == '__main__':
	ann = multilayer.NeuralNet()
	(weights_ret, bias_ret) = ann.train_multilayer_SGD(labels[6], features[6], .01, 500, y_test, x_test)

