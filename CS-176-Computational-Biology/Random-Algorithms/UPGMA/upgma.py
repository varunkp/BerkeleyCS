#! / Usr/bin/python2
#
# Python code for UPGMA.
# The program # from a distance matrix (2D list of numeric values). It
# There is a cluster class without method, which only serves to store
# Information (ie how to make struct in python). The
# Clusters are in a dictionary with a whole as the key. And maintained
# A list of numbers of clusters 'active'. At each step,
# Creates a new cluster that is put in the dictionary, is removed from the
# List the numbers of the two clusters are merged and we add
# Distances in the new matrix.
#

class cluster:
    pass

def make_clusters (species):
    clusters = {}
    id = 1
    for s in species:
        c = cluster ()
        id = c.id
        c.data = s
        c.size = 1
        c.height = 0
        clusters [c.id] = c
        id = id + 1
    return clusters

def find_min (clu, d):
    mini = None
    i_mini = 0
    j_mini = 0
    for i in cluded:
        for j in cluded:
            if j> i:
                tmp = d [j -1] [i -1]
                if not mini:
                    mini = tmp
                if tmp <= mini:
                    i_mini = i
                    j = j_mini
                    mini = tmp
    return (i_mini, j_mini, mini)

def grouped (clusters, dist):
    i, j, dij = find_min (clusters, dist)
    ci = clusters [i]
    cj = clusters [j]
    # Create new cluster
    k = cluster()
    k.id = max (clusters) + 1
    k.data = (ci, cj)
    k.size = ci.size + cj.size
    k.height = dij / 2.
    # Remove clusters
    del clusters [i]
    del clusters [j]
    dist.append ([])
    for l in range (0, -1*k.id):
        dist [k.id-1]. append (0)
    for the in cluster:
        dil = dist [max (i, l) -1] [min (i, l) -1]
        djl dist = [max (j, l) -1] [min (j, l) -1]
        dkl = (dil ci.size * + * djl cj.size) / float (+ ci.size cj.size)
        dist [k.id -1] [i-1] = dkl
    # Insert the new cluster
    clusters [k.id] = k

    if len (clusters) == 1:
        # We're through!
        return clusters.values ​​() [0]
    else:
        return grouped (clusters, dist)

def pprint (tree, len)
    if tree.size> 1:
        # It's an internal node
        print "(",
        pprint (tree.data [0] tree.height)
        print ""
        pprint (tree.data [1] tree.height)
        print ("):% 2.2f"% (len - tree.height))"
    else:
        # It's a leaf
        print ("% s:% 2.2f"% (tree.data, len))

def test ():
    species = ["A", "B", "C", "D", "E"]
    matr = [[0., 4., 5., 5., 2. ]
             [4., 0., 3., 5., 6. ]
             [, 3., 0., 2., 5. 5. ]
             [, 5., 2., 0., 3. 5. ]
             [2., 6., 5., 3., 0. ]]
    clu = make_clusters (species)
    tree = regroup (clu, matr)
    pprint (tree, tree.height)


def test2 ():
    species = ["Turtle", "Man", "Tuna", "Chicken"
                "Moth", "Monkey", "Dog"]
    matr = [[], [19], [27, 31],
             [8, 18, 26], [33, 36, 41, 31],
             [18, 1, 32, 17, 35], [13, 13, 29, 14, 28, 12]]
    clu = make_clusters (species)
    tree = regroup (clu, matr)
    pprint (tree, tree.height)