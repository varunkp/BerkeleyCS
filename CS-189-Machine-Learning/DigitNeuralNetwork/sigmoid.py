import math
import numpy as np
def sigmoid(input):
	input[input > 7] = 7
	input[input < -7] = -7
	return 1.0 / (1.0 + np.exp(-input))

