import os, subprocess, time, sys, random
from cogent import LoadTree

prefix = '/Users/telliott_admin/Desktop/nj/'
controlfn = prefix + 'data/responses.txt'
datafn = prefix + 'data/nj_data.phylip.txt'
resultfn = prefix + 'outfile'
treefn = prefix + 'outtree'

def one_run(n):
    n = str(n)
    FH = open(controlfn, 'w')
    FH.write(datafn + '\n')
    FH.write('J\n')
    seed = random.choice(range(2,200))
    if not seed % 2: seed += 1
    FH.write(str(seed) + '\n')
    FH.write('Y\n')
    FH.close()
    cmd = 'neighbor < ' + controlfn + ' > '
    cmd += 'screenout &'
    p = subprocess.Popen(cmd, shell=True)
    pid,ecode = os.waitpid(p.pid, 0)
    print ecode
    time.sleep(1)
    os.rename(resultfn,prefix+'results/outfile' + n + '.txt')
    os.rename(treefn,prefix+'results/outtree' + n + '.txt')
    os.remove(prefix + 'screenout')

N = 50
#for i in range(1,N+1):  one_run(i)
L = list()
for i in range(1,N+1):
    tr = LoadTree(prefix + 'results/outtree' + str(i) + '.txt')
    L.append(tr)
    
for i in range(N):
    for j in range(N):
        if i == j:
            continue
        if not L[i].sameTopology(L[j]):
            print L[i]
            print L[j]
        else:
            print '.',
        
'''
R code:
library(ape)
setwd('Desktop')
tr = read.tree('nj/results/outtree1.txt')
plot(tr,edge.width=3,cex=2,type='unrooted')
axisPhylo()
'''
