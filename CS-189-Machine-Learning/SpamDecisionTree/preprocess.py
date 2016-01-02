import scipy.io as sio
import numpy
import math

def split(training_examples, attributes):
	def create_sorter(attr):
		return lambda el: el[0][attr]

	max_info_gain = float("-inf")
	best_attr = 0
	best_attr_val = 0
	best_index = 0
	best_H1 = 0
	best_H2 = 0
	best_inf_g = 0
	for attr in attributes:
		sorted_examples = sorted(training_examples, key=create_sorter(attr)) #sorts on desired attribute
		attr_values = [el[0][attr] for el in sorted_examples]
		values = sorted(list(set(attr_values))) #list of unique values

		if len(values) == 1:
			info_gain = 0.0
			if info_gain > max_info_gain:
				max_info_gain = 0.0
			continue
		i = 0
		last_index_of_val = [0]*len(values) #gives last index of given value 
		y_s = [int(el[1]) for el in sorted_examples]
		#ex: [0, 0, 0, 1, 1] we get [(0, 2), (1, 4)]
		for j in range(len(values)):
			val = values[j]
			while i+1 < len(attr_values) and attr_values[i+1] == val:
				i = i+1
			last_index_of_val[j] = (val, i)
		# cumulative positive examples through sorted list

		positive_examples_so_far = y_s[:]

		for i in range(1, len(y_s)):
			positive_examples_so_far[i] += positive_examples_so_far[i-1]


		p = float(positive_examples_so_far[-1])/len(positive_examples_so_far)

		H = -p*math.log(p, 2) - (1-p)*math.log(1-p, 2)


		for value, index in last_index_of_val[:-1]:
			p_1 = float(positive_examples_so_far[index])/(index + 1)
			p_2 = float(positive_examples_so_far[-1] - positive_examples_so_far[index])/(len(positive_examples_so_far) - index - 1)
			H_1 = -p_1*math.log(p_1) - (1-p_1)*math.log(1-p_1, 2) if p_1 not in (0, 1) else 0.0
			H_2 = -p_2*math.log(p_2) - (1-p_2)*math.log(1-p_2, 2) if p_2 not in (0, 1) else 0.0

			information_gain = H - ((index + 1)*H_1 + (len(positive_examples_so_far) - index - 1)*H_2)/len(positive_examples_so_far)
			if information_gain > max_info_gain:
				max_info_gain = information_gain
				best_attr = attr
				best_attr_val = value
				best_index = index
	return (best_attr, best_attr_val, max_info_gain)

