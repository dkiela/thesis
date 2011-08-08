import brainsim
import brainalyze
import scipy
import numpy
import matplotlib.pyplot as plt
from brian import *

parameters = {
	'ESYN_MAXCONDUCTANCE':0, #0.05 ['']
	'ISYN_MAXCONDUCTANCE':0, #0.4
	'CONN_LATERAL':1, #0.02
	'CONN_INTERNAL':1, #0.02
	'ENDSIM':2, 
	'FSV':10000,
	'BRAINNAME':"prefix+num",#filled in by code
	'BRAINPREFIX':'vb-exp',
	'TAU_NOISE':0.020} #0.020

# Starting values
trials=20
esynval=0.1
esynval_step=0.001
isynval=0.0
isynval_step=0

def run_simulations():
	global esynval
	global esynval_step
	runs=0
	while runs < trials:
		parameters['ESYN_MAXCONDUCTANCE']=esynval
		parameters['ISYN_MAXCONDUCTANCE']=isynval
		parameters['BRAINNAME']='vb-exp'+str(int(runs))
		brainsim.simBrain(parameters)
		esynval=esynval+esynval_step
		runs=runs+1
	return True

def run_analysis():
	exp=0
	spikecorr=[]
	correlations=[]
	frateX=[]
	frateY=[]
	bsCorr=[]
	while exp < trials:
		(listX,cntX,spikesX),(listY,cntY,spikesY)=brainalyze.loadExperiment(parameters['BRAINPREFIX'],exp)
		#(listX,cntX,spikesX),(listY,cntY,spikesY)=brainalyze.loadExperiment('vb-exp',8)
		print "cntX,spikesX: ", cntX, spikesX
		print "cntY,spikesY: ", cntY, spikesY
		sxcorr = scipy.correlate(spikesX, spikesY)
		spikecorr.append(sxcorr[sxcorr.argmax()])
		xcorr = scipy.correlate(listX,listY)
		correlations.append(xcorr[xcorr.argmax()])
		# convert to Brian-style spike trains
		bsSpikesX=map(lambda x: float(x)/10000, spikesX)
		frateX.append(statistics.firing_rate(bsSpikesX))
		# only if we have more than 1 spike in Y can we calculate firing rate
		if cntY > 1:
			bsSpikesY=map(lambda x: float(x)/10000, spikesY)
			frateY.append(statistics.firing_rate(bsSpikesY))
			bsCorr.append(statistics.total_correlation(bsSpikesX,bsSpikesY))
		else:
			bsCorr.append(-1.0)
			frateY.append(0.0)
		exp=exp+1
	print "Done"
	return (frateX,frateY,bsCorr)

run_simulations()
rx,ry,c = run_analysis()
# Store for later use
#numpy.save("correlations500-0.0-0.5.npy", np.array(c))

axis=numpy.linspace(0.0,esynval_step*trials,len(c))
plt.subplot(211)
plt.title('Firing rates of X and Y')
plt.plot(axis,rx,'r',axis,ry,'g')
plt.subplot(212)
plt.title('Correlation')
plt.plot(axis,c,'b')
plt.show()
