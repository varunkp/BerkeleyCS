from scipy import stats
import numpy as np
xk = np.arange(1000)
pk = np.ones(1000) * 1.0 / 1000
custm = stats.rv_discrete(name='custm', values=(xk, pk))

R = custm.rvs(size=3000)
print R