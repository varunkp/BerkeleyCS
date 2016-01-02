from rpy2 import robjects
from rpy2.robjects.packages import importr
from upgma import run

fn = 'upgma_data.txt'

#fn = 'upgma_Sarich_data.txt'
names = { 'A':'dog','B':'bear','C':'raccoon','D':'weasel', 
          'E':'seal','F':'sea_lion','G':'cat','H':'monkey' }

node_dict = run(fn)
L = [k for k in node_dict.keys() if len(k) == 1]
otus = sorted(L)

debug = True
if debug:
    for k in node_dict:
        print k, node_dict[k]
    
for k in otus:
    tD = node_dict[k]
    if len(k) > 1:
        name = k
    if fn == 'upgma_Sarich_data.txt':
        name = names[k]
    else:  name = k
    tD['node_repr'] = name + ':' + '%d' % tD['up']

# build up the internal nodes by
# sorting on the length of the labels
def sort_key(s):
    return len(s)
L = sorted(node_dict.keys(), key=sort_key)
L = [k for k in L if len(k) > 1]

for k in L:
    print k
    tD = node_dict[k]
    left = node_dict[tD['left']]['node_repr']
    right = node_dict[tD['right']]['node_repr']
    try:
        up = ':%d' % tD['up']
    except KeyError:
        up = ';'
    node_repr = '(' + left + ', ' + right + ')' + up
    tD['node_repr'] = node_repr

root = ''.join(otus)
tree_text = node_dict[root]['node_repr']
#tree_text += ';'
print root, tree_text

ape = importr('ape')
grdevices = importr('grDevices')
tr = ape.read_tree(text=tree_text)
pL = fn.split('.')
ofn = '.'.join(pL[:-1]) + '.pdf'

grdevices.pdf(ofn)
# for Sarich data, manually adjusted x-axis
ape.plot_phylo(tr,cex=2,edge_width=2)
#ape.plot_phylo(tr,cex=2,edge_width=2,x_lim=100)
ape.axisPhylo()
grdevices.dev_off()