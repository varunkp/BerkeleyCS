"""
Input: Training data (x_m, y_m), t = 1...T
Given: D_i(t), initially equal weights dist'n
Output: Weak hypothesis {-1, 1}
"""

import scipy.io as sio
from scipy import stats
import numpy as np
import math
import random

array = np.array

data = sio.loadmat('spam.mat')

Xtrain = data['Xtrain']
ytrain = data['ytrain']
Xtest = data['Xtest']

mean = Xtrain.mean(axis=0)

training_examples = zip(Xtrain, [el[0] for el in ytrain])
# attributes = set(range(57))
# attributes = set(range(2))


""" ---------------------------------------------------------- """


import id3

def adaboost(training_data, rounds):

	m = len(training_data)
	weights = np.ones(m) * 1.0 / m
	strong_hypothesis = np.zeros(m)
	learners = []
	alphas = []

	attributes = set(range(57))

	for t in range(rounds):

		error = 0.0
		resampled_examples = []
		examples_index = resample(weights, m)

		for i in range(m):
			resampled_examples.append(training_data[examples_index[i]])

		weak_learner = id3.id3_depth_limited(resampled_examples, attributes, 2)
		learners.append(weak_learner)

		#classifications = [(id3.classify(weak_learner, X), y) for X, y in resampled_examples]
		classifications = [(id3.classify(weak_learner, X), y) for X, y in training_data]
		error = 0
		for i in range(len(classifications)):
			predicted, actual = classifications[i]
			error += (predicted != actual)*weights[i]

		print "Error", error

		if error == 0.0:
			alpha = 4.0
		elif error > 0.5:
			break
		else:
			alpha = 0.5 * np.log((1 - error)/error)

		alphas.append(alpha)
		learners.append(weak_learner)

		for i in range(m):
			h, y = classifications[i]
			h = -1 if h == 0 else 1
			y = -1 if y == 0 else 1
			#weights[examples_index[i]] = weights[examples_index[i]] * np.exp(-alpha * h * y)
			weights[i] = weights[i] * np.exp(-alpha * h * y)
		sum_weights = sum(weights)
		print 'Sum of weights', sum_weights
		normalized_weights = [float(w)/sum_weights for w in weights]
		weights = normalized_weights

	return zip(alphas, learners)


def classify(strong_hypothesis, example):
	classification = 0
	for weight, learner in strong_hypothesis:
		ex_class = 1 if id3.classify(learner, example) == 1 else -1
		classification += weight*ex_class

	return 1 if classification > 0 else 0



def resample(weights, m):
	xk = np.arange(m)
	pk = weights
	custm = stats.rv_discrete(name='custm', values=(xk, pk))
	R = custm.rvs(size=m)
	return R



break_point = len(training_examples)*3/4
ret = adaboost(training_examples[:break_point], 100)

print ret

classifications = [(classify(ret, X), y) for X, y in training_examples[break_point: ]]
accuracy = sum([x == y for x, y in classifications])/float(len(classifications))
print accuracy



# import random

# def resample(weights):
#     rnd = random.random()*sum(weights)
#     for i, w in enumerate(weights):
#         rnd -= w
#         if rnd < 0:
#             return i
