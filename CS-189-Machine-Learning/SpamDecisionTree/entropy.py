import math
import numpy as np

"""
Returns the information gain of an attribute by calculating the entropy
The choose an attribute, we will be taking argmax over all attributes of calculate_IG.
"""



"""
Training Examples: (feature_vector, classification)
feature_vector is R57, classification is {0, 1}
3450 training examples and 57 vectors for each

attributes is a set from 1 to 57 that we remove from

"""



"""
for each attribute, calculate entropy and return the min
"""

def calculate_entropy(examples, attribute):
	"""
	Calculate entropies (as a list) from a set of attributes from the features,
	and return a tuple of min_attribute, min_entropy.

	Inputs: - examples is a list of (x,y) pairs where x is numpy (1 x 57) and y is scalar
	Returns: min_attribute (float), min_entropy (float)
	"""
	entropy = 0.0
	count_0 = 0
	for x, y in examples:
		for elem in np.nditer(x):
			if elem <= attribute:
				count_0 += 1
		p1 = count_0 / len(examples)
		entropy -= p1 * math.log(p1, 2)

