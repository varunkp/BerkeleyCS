import sys
from cogent.draw import dendrogram
from cogent.phylo import nj
import utils

fn = 'data/nj_data.txt'
data = utils.load_data(fn,split_lines=True)
otus = utils.letters[:len(data)]
dists = dict()
for t1,line in zip(otus,data):
    L = line.strip().split()
    L = [float(n) for n in L]
    for t2,e in zip(otus,L):
        dists[(t1,t2)] = e
        
tr = nj.nj(dists)
print tr.asciiArt()
print

for n in tr.iterTips():
    print n.ancestors()[0].Name, n

def show_edge_children(node):
    children = node.iterNontips()
    for child in children:
        print node.Name,
        print child.Name, 
        print node.distance(child),

edges = list(tr.iterNontips())
for e in edges:
    print
    show_edge_children(e)
root = tr.getNodeMatchingName('root')
show_edge_children(root)

print tr

sys.exit()
from cogent.draw import dendrogram
h, w = 500, 500
np = dendrogram.ContemporaneousDendrogram(tr)
np.drawToPDF('cogent_tree.pdf', w, h, font_size=14)

'''
setwd('Desktop')
library(ape)
tr = read.tree(text = 
'((((A:1.0,B:4.0):1.0,C:2.0):1.25,F:4.75):0.75,D:2.75,E:2.25);')
plot(tr,type='unrooted',edge.width=2)
'''