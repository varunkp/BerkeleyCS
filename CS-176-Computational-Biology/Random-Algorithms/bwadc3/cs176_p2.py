import sys
class Triple(object):
	def __init__(self,T,ind,length):
		self.triple = []
		for i in range(3):	
			if ind+i > length-1:
				self.triple.append(0)
			else:
				self.triple.append( int(T[ind+i]))
		self.T_index = ind
		self.rank = None
		self.R_index = None
		self.alpha_size_cap = length
	def getIndex(self):
		return self.T_index
	def getTriple(self):
		return self.triple
	def getRIndex(self):
		return self.R_index
	def setRIndex(self, index):
		self.R_index = index
	def getRank(self):
		return self.rank
	def setRank(self, rank):
		self.rank = rank
	def getAlphaCap(self):
		return self.alpha_size_cap
	
class Pair(object):
	def __init__(self,T,index, rank):
		self.pair = []
		self.pair.append(T[index]);
		self.pair.append(rank);
		self.index = index 
		self.rank = None
		self.R_index = None
		self.tripObj = Triple
	def getIndex(self):
		return self.index
	def getPair(self):
		return self.pair
	def getRIndex(self):
		return self.R_index
	def setRIndex(self, index):
		self.R_index = index
	def getRank(self):
		return self.rank
	def setRank(rank):
		self.rank = rank

def decode(input):
	return ibwt(input)	
def encode(input):
	alphabet = {}
	for i in range(53):
		if i ==0:
			alphabet['$'] = 0
		elif i < 27:
			alphabet[chr(i+64)] = i
		else:
			alphabet[chr(i+70)] = i
	integerInput = []
	for letter in input:
		integerInput.append(alphabet[letter])
	As = DC3(integerInput)
	return bwt(input, As)
def split(list,index,length):
	if index > length-1:
		return list
	buckets = {}
	for tripleObj in list:
		if type(tripleObj) is tuple:
			if tripleObj not in buckets:
				buckets[tripleObj] = []
			buckets[tripleObj].append(tripleObj)
		else:
			if tripleObj.triple[index] not in buckets:
				buckets[tripleObj.triple[index]] = []
			buckets[tripleObj.triple[index]].append(tripleObj)
	currList = sorted(buckets.iteritems()) 
	"""	for i in range(length):
		if len(buckets[i]) > 0:
			currList.append(buckets[i])"""
	newList = []
	for item in currList:
		newList = newList + split(item[1],index+1,length)
	return newList 
		
def radix(list, length):
	newList = list
	newList =split(newList, 0,length)		
	return newList 
	
def parse(inputFile):
	input = open(inputFile,'r').readlines()	
	if ('>' in input[0]):
		del input[0]
	return "".join("".join(input).split())
def DC3(input):
	length = len(input)
	S0 = []
	S1 = [] 
	S2 = []
	B0 = range(0,length,3)
	B1 = range(1,length,3)
	B2 = range(2,length,3)
	
	RIndex = 0
	for index in B1:
		if index < length:
			triple = Triple(input,index,length)
			triple.setRIndex(RIndex)
			S1.append(triple)
			RIndex+=1
			
	for index in B2:
		if index < length:
			triple = Triple(input,index,length)
			triple.setRIndex(RIndex)
			S2.append(triple)
			RIndex+=1
	R_old_to_new = {} 
		
	R = S1 + S2
	for triple in R:
		R_old_to_new[triple.getIndex()] = triple.getRIndex() 
	R_old_to_new[len(input)] = len(R)
	R_old_to_new[len(input)+1] = len(R) + 1	
				
	Rprime = []
	Rprime_SA = []
	Rsorted = sorted(R, key =lambda tripObj:tripObj.triple)
	tripleRank = 1
	def suff_rank (input):
		rank = 1
		for index, tripleObject in enumerate(input):
			if index > 0 and tripleObject.triple != input[index-1].triple:
				rank += 1
			tripleObject.setRank(rank)
		return rank
	
	tripleRank = suff_rank(Rsorted)
	Rprime = [triple.rank for triple in R]
			

	# Now, sort R via radix or recursive DC3.
		
	if tripleRank < len(R):
		#sort R recursively, since there are repeats
		Rprime_SA = DC3(Rprime)
		#TO DO LINE 100 OF GIT
	else:
		for tripObj in Rsorted:
			Rprime_SA.append(tripObj.getRIndex())
	#TO DO
	#Now, we have sort of R'. We need to sort S0 relative to R.
	Rprime_SA_inverse = {}
	Rprime_SA_inverse[len(R)] = -1
	Rprime_SA_inverse[len(R) + 1] = -1
	#TO DO
	for i, index in list(enumerate(Rprime_SA)):
		Rprime_SA_inverse[index] = i+1
	#	Rsorted = [R[i] for i in Rprime_SA[1:]]
	for index in B0:
		if index + 1 > len(input)-1:
			S0.append(Pair(input,index, -1))
		else:
			S0.append(Pair(input, index, Rprime_SA_inverse[R_old_to_new[index+1]]))
	# def nonsamplesort(B): (STEP 2) TO DO

	# S0_pairs = []
	# for index in B0:
	# 	S0_pairs.append(Pair(input, index, Rprime_SA_inverse))
	 	 
	#S0_pairs = [Pair(input, S0[idx], Rprime_SA_inverse) for idx in B0]		
	# S0_sorted = radix(B0_pairs,2)
	S0_sorted = sorted(S0, key =lambda p: p.getPair())


	# def merge(R12, R0): (STEP 2) TO DO
	
 	temp = []

	for Rindex in Rprime_SA:
		temp.append(R[Rindex])
	Rsorted = temp



	#merge step
	Si, Sj = 0,0
	pairs = []
	while Si < len(S0_sorted) and Sj < len(Rsorted): # WHERE I LEFT OFF 
		j = Rsorted[Sj].getIndex()
		i = S0_sorted[Si].getIndex()

		if j % 3 == 1:
			rankComp = 0
			if j +1 > len(input):
				rankComp = -1
			else:
				rankComp = Rprime_SA_inverse[R_old_to_new[j+1]]

			if i >=len(input)-1:
				pairs.append(S0_sorted[Si])
				Si+=1
			elif (input[i], Rprime_SA_inverse[R_old_to_new[i+1]]) < (input[j],rankComp):
				pairs.append(S0_sorted[Si])
				Si += 1
			else:
				pairs.append(Rsorted[Sj])
				Sj += 1
		
		else:
			
			rankComp1 = 0
			rankComp2 = 0
			if j+1 >=len(input):
				rankComp1 = -1
			else:
				rankComp1 = input[j+1]
			if j+2 > len(input):
				rankComp2 = -1
			else:
				rankComp2 = Rprime_SA_inverse[R_old_to_new[j+2]]
			if i >=len(input)-1:
				pairs.append(S0_sorted[Si])
				Si+=1
			elif (input[i], input[i+1], Rprime_SA_inverse[R_old_to_new[i+2]]) < (input[j],rankComp1,rankComp2):
				pairs.append(S0_sorted[Si])
				Si += 1
			else:
				pairs.append(Rsorted[Sj])
				Sj += 1
	pairs += Rsorted[Sj:]
	pairs += S0_sorted[Si:]
	suffix_array = [suffix.getIndex() for suffix in pairs]
	return suffix_array

def bwt(input, suffix_array):
    result = len(input) * [0]
    output=[]
    length = len(input)

    for i in range(length):
	    j = 0
	    if suffix_array[i] < 1:
		j = length-1
	    else:
		j = suffix_array[i] - 1	
            result[i] = input[j]
    output = formatOutput('>BWT', result, 'bwt')

    # output += '>BWT'
    # for i in range(0,length(result)):
    #     if (i % 80 == 0):
    #         output += '\n'
    #     output += output[i]
    # output += '\n'
    return output

def ibwt(bwtinput):
    L = bwtinput
    Lc = []
    letterCounter =1
    for index in range(len(L)):
	Lc.append((L[index], index))
    Fc = []
    Fc = radix(Lc,2)
    backString = []
    i = Fc.index(Lc[0])
    while len(backString) < len(bwtinput)-1:
	nextLetter = Fc[i][0]
	i = Fc.index(Lc[i])
	backString.append(nextLetter)
    print backString
    backString.reverse()
    print backString
    output = formatOutput('>iBWT', backString,'ibwt')
    return output
     
def formatOutput(header, result, i):
    output = header
    for x in range(len(result)):
        if (x % 80 == 0):
            output += '\n'
        output += result[x]
	
    if i == 'ibwt':
        output += '$'
    output += '\n'
    return output
        
flag = sys.argv[1]
input = sys.argv[2] 
out = open(sys.argv[3], 'w')
input = parse(input)
if flag == 'bwt':
	output = encode(input)
	out.write(output)
	
elif flag == 'ibwt':
	out.write(decode(input))

