import scipy.io as sio
import numpy
import math
import preprocess as pp
import decisiontree as dt

def id3(examples, attributes):

	root = dt.TreeNode()

	one_count = sum([int(y) for X, y in examples]) 

	if one_count == len(examples):
		root.label = 1
		return root

	if one_count == 0:
		root.label = 0
		return root

	if not attributes:
		if one_count >= len(examples) / 2.0:
			root.label = 1
		else:
			root.label = 0
		return root

	best_attribute, best_value, info_gain = pp.split(examples, attributes)
	
	if info_gain == 0:
		if one_count >= len(examples) / 2.0:
			root.label = 1
		else:
			root.label = 0
		return root
	root.attribute = best_attribute
	root.split_value = best_value
	left_exs = []
	right_exs = []
	for ex in examples:
		if ex[0][root.attribute] <= root.split_value:
			left_exs.append(ex)
		else:
			right_exs.append(ex)
	new_attributes = attributes.copy()
	new_attributes.remove(best_attribute)
	root.left_child = id3(left_exs, new_attributes)
	root.right_child = id3(right_exs, new_attributes)

	return root


def id3_depth_limited(examples, attributes, depth):

	root = dt.TreeNode()

	if sum([y for X, y in examples]) == len(examples):
		root.label = 1
		return root

	if sum([y for X, y in examples]) == 0:
		root.label = 0
		return root

	if not attributes or depth == 0:
		if sum([y for X, y in examples]) >= len(examples) / 2.0:
			root.label = 1
		else:
			root.label = 0
		return root
	best_attribute, best_value, info_gain = pp.split(examples, attributes)
	if info_gain == 0:
		if sum([y for X, y in examples]) >= len(examples) / 2.0:
			root.label = 1
		else:
			root.label = 0
		return root
	root.attribute = best_attribute
	root.split_value = best_value
	left_exs = []
	right_exs = []
	for ex in examples:
		if ex[0][root.attribute] <= root.split_value:
			left_exs.append(ex)
		else:
			right_exs.append(ex)
	new_attributes = attributes.copy()
	new_attributes.remove(best_attribute)
	root.left_child = id3_depth_limited(left_exs, new_attributes, depth-1)
	root.right_child = id3_depth_limited(right_exs, new_attributes, depth-1)

	return root

def classify(tree_node, example):
	if tree_node.label is not None:
		return tree_node.label
	if example[tree_node.attribute] <= tree_node.split_value:
		return classify(tree_node.left_child, example)
	else:
		return classify(tree_node.right_child, example)

if __name__ == '__main__':
	### the following  3 lines can be modified as needed to input the test set ###
	file_name = sys.argv[1]
	data = sio.loadmat(file_name)
	Xtest = data['Xtest']
	########################################################################
	output_file = sys.argv[2]
	if len(sys.argv) > 3:
		rounds = int(sys.argv[3])
	else:
		rounds = 100

	print 'Learning...'
	attributes = set(range(57))
	tree = id3(training_examples, attributes)
	print 'Classifying...'
	classifications = [classify(tree, X) for X in Xtest]


	print 'Writing to', output_file
	with open(output_file, 'wb') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow(['Id', 'Category'])
		for index, classification in enumerate(classifications):
			filewriter.writerow([index+1, '|', classification])
	print 'Done writing to', output_file


