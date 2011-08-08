# More elaborate version of test-sync1
import numpy as np
import matplotlib.pyplot as plt
from brian import statistics

trials=10
scorr=np.zeros(shape=(trials,trials))
esyn=0.0
isyn=1.0

while esyn <= 0.1:
	while isyn >= 0.0:
		# pseudocode
		#parameters[esyn]=esyn
		#parameters[isyn]=isyn
		scorr[esyn][isyn]=get_corr(parameters)
		jj=jj-(1/trials)
	ii=ii+(1/trials*10)
plt.plot(scorr, 'bx')
plt.show()

def get_corr():
	#run simulation/analyze results
	return 0
