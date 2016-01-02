import numpy as np
import utils

fn = 'data/nj_data.txt'
data = utils.load_data(fn,split_lines=True)
N = len(data)
A = list()
for line in data:
    A.append([float(n) for n in line.split()])
otus = list(utils.letters[:N])
node_dict = dict()

def one_round(A,otus,count):
    print otus
    print A
    print
    div = np.sum(A,axis=1)
    print div
    n = A.shape[0]
    
    # two nodes only:  we're done
    if n == 2:
        dist = A[1][0]
        nD = node_dict[otus[0]]
        nD['up'] = otus[1]
        nD['d_up'] = dist
        return None,otus

    # find the i,j to work on using divergence
    i,j = 0,0
    low_value = A[i][j]
    for r,row in enumerate(A):
        if r == 0:  continue
        for c,col in enumerate(row):
            if c >= r:  continue
            dist = A[r][c]
            first = div[c]
            second = div[r]
            correction = (first + second)/(n-2)
            value = dist - correction
            print r, c, dist, first, second, correction, value
            if value < low_value:
                i,j,low_value = r,c,value
                
    # merge i and j entries
    # calculate distance of new node from tips
    new_name = utils.digits[count]
    print
    print 'merge:', i, otus[i], j, otus[j], 'to', new_name
    
    # dist from node[i]
    dist =  A[i][j]
    diff = div[i] - div[j]
    print 'orig dist', dist, 'div diff', diff
    dist_i = dist/2.0 + diff/(2*(n-2))
    dist_j = dist - dist_i
    print dist_i, dist_j
    node = { 'L':otus[i], 'dL':dist_i, 
             'R':otus[j], 'dR':dist_j }
    node_dict[new_name] = node
    print node
    
    # calculate distances to new node
    # i,j assigned above
    tL = list()
    ij_dist = A[i][j]
    for k in range(len(A[0])):
        if k == i or k == j:  continue
        print 'node', otus[k], A[i][k], A[j][k], ij_dist,
        dist = (A[i][k] + A[j][k] - ij_dist)/2
        print dist
        tL.append(dist)
    print 'to new node:', tL
    
    print
    print A
    print

    # remove columns and rows involving i or j
    if i < j:  i,j = j,i
    assert j < i
    print 'i', i, 'j', j
    sel = range(n)
    for k in [j,i]:    # larger first
        sel.remove(k)
        print 'sel', sel
        A1 = A[sel,:]
        A2 = A1[:,sel]
        print A2
    A = A2
    print
    # correct the otu names:
    otus = [new_name] + otus[:j] + otus[j+1:i] + otus[i+1:]
    
    # add col at left and row at top for new node
    new_col = np.array(tL)
    new_col.shape = (n-2,1)
    A = np.hstack([new_col,A])

    new_row = np.array([0] + tL)
    new_row.shape = (1,n-1)
    A = np.vstack([new_row,A])
    print A
    print
    return A,otus
    
A = np.array(A)
A.shape = (N,N)
print A

count = 0

while True:
    print 'round', count
    A,otus = one_round(A,otus,count)
    if A is None:  break
    count += 1
    print A
    print
print

kL = ['L','dL','R','dR','up','d_up']
for node in sorted(node_dict.keys()):
    print node, ':   ',
    for k in kL:
        nD = node_dict[node]
        if not k in nD:
            continue
        v = nD[k]
        if k in ['dL','dR']:
            v = '%3.3f' % v
        print v, ' ',
    print
