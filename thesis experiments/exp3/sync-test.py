# NOOOOO
# THIS IS NOT!!! THE RIGHT FILE, IT WAS OVERWRITTEN ACCIDENTALLY
# 

# Fixed ESYN at 0.058 (highest correlation in exp3)

import brainsim
import brainalyze
import scipy
import numpy
import matplotlib.pyplot as plt
from brian import *

parameters = {
	'ESYN_MAXCONDUCTANCE':0.058, #0.05 ['']
	'ISYN_MAXCONDUCTANCE':0, #0.4
	'CONN_LATERAL':1, #0.02
	'CONN_INTERNAL':1, #0.02
	'ENDSIM':5, 
	'FSV':10000,
	'BRAINNAME':"prefix+num",#filled in by code
	'BRAINPREFIX':'vb-exp',
	'TAU_NOISE':0.020} #0.020

# Starting values
isynval_start=0.0
isynval_end=1.0
isynval_step=0.01
y_max=(isynval_end-isynval_start)/isynval_step

def run_simulations():
	isynval=isynval_start
	cnt=0
	while isynval < isynval_end:
		parameters['ISYN_MAXCONDUCTANCE']=isynval
		parameters['BRAINNAME']='vb-exp'+str(cnt)
		brainsim.simBrain(parameters)
		isynval=isynval+isynval_step
		cnt=cnt+1
	return True

def run_analysis():
	scorr=[]
	sratex=[]
	sratey=[]
	y=0
	global y_max

	while y < y_max:
		(listX,cntX,spikesX),(listY,cntY,spikesY)=brainalyze.loadExperimentXYl('vb-exp', y)
		bsSpikesX=map(lambda x: float(x)/10000, spikesX)
		sratex.append(statistics.firing_rate(bsSpikesX))

		if cntY > 1:
			bsSpikesY=map(lambda x: float(x)/10000, spikesY)
			sratey.append(statistics.firing_rate(bsSpikesY))
			scorr.append(statistics.total_correlation(bsSpikesX,bsSpikesY))
		else:
			sratey.append(0.0)
			scorr.append(-1.0)
		y=y+1

	return (sratex,sratey,scorr)

run_simulations()
rx,ry,c = run_analysis()

# Store for later use
numpy.save("scorr-learning.npy", np.array(c))
numpy.save("sratex-learning.npy", np.array(rx))
numpy.save("sratey-learning.npy", np.array(ry))

#data = c

#fig = plt.figure()
#ax = fig.add_subplot(111)
#cax = ax.imshow(data, interpolation='nearest')
#ax.set_title('Correlation over ESYN and ISYN')
#cbar = fig.colorbar(cax, ticks=[-1, 0, 1])
#cbar.ax.set_yticklabels(['< -1', '0', '> 1'])
#plt.show()

#print c

axis=numpy.linspace(0.0,y_max,len(c))
plt.subplot(211)
plt.title('Firing rates of X and Y')
plt.plot(rx,'r',ry,'g')
plt.subplot(212)
plt.title('Correlation')
plt.plot(c,'b')
plt.show()
