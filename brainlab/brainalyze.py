import brainsim
import numpy
import scipy
from brian import *

# Count the number of spikes that exceed the threshold and
# return a list of spike times (equivalent to Brian spike train * FSV)
# l = the output list from a single-neuron assembly
# startcount = the timestep when we start counting spikes (i.e., after learning)
def countSpikes (l, startcount=0):
	a = numpy.array (l)
	count = 0 
	i = startcount
	thres = -50.0 #THIS THRESHOLD HAS TO BE RETRIEVED FROM BRAINLAB
	exceed = False 
	spikeindices =[]
	while i<len (l):
		if (exceed == False and a[i] > thres):
			count = count + 1
			exceed = True
		if (a[i] < thres and exceed):
			spikeindices.append (i)
			exceed = False
		i = i + 1
	return count, spikeindices 

def loadExperimentXY (prefix, exp):
	listX = brainsim.loadBrain (prefix + str (exp) + "-XReport.txt")
	listY = brainsim.loadBrain (prefix + str (exp) + "-YReport.txt")
	cntX, spikesX = countSpikes (listX)
	cntY, spikesY = countSpikes (listY)
	return (listX,cntX,spikesX),(listY,cntY,spikesY)

def loadExperimentXYI (prefix, esynval, isynval):
	listX = brainsim.loadBrain (prefix + str (esynval) + "-" + str(isynval) + "-XReport.txt")
	listY = brainsim.loadBrain (prefix + str (esynval) + "-" + str(isynval) + "-YReport.txt")
	cntX, spikesX = countSpikes (listX)
	cntY, spikesY = countSpikes (listY)
	return (listX,cntX,spikesX),(listY,cntY,spikesY)

def loadExperimentBind4 (prefix, x, y):
	startcount = 1 * 10000 # (learning time in s * FSV)
	listB = brainsim.loadBrain (prefix + str (x) + "-" + str(y) + "-BReport.txt")
	listG = brainsim.loadBrain (prefix + str (x) + "-" + str(y) + "-GReport.txt")
	listT = brainsim.loadBrain (prefix + str (x) + "-" + str(y) + "-TReport.txt")
	listS = brainsim.loadBrain (prefix + str (x) + "-" + str(y) + "-SReport.txt")
	cntB, spikesB = countSpikes (listB, startcount)
	cntG, spikesG = countSpikes (listG, startcount)
	cntT, spikesT = countSpikes (listT, startcount)
	cntS, spikesS = countSpikes (listS, startcount)
	return (spikesB,spikesG,spikesT,spikesS)

def corr(spikesA,spikesB):
	if len(spikesA) <= 1 or len(spikesB) <= 1:
		return -1

	# Convert to Brian-style spike train
	bsSpikesA=map(lambda x: float(x)/10000, spikesA)
	bsSpikesB=map(lambda x: float(x)/10000, spikesB)

	return statistics.total_correlation(bsSpikesA,bsSpikesB)

def frate(spikes):
	if len(spikes) <= 1:
		return -1
	bsSpikes=map(lambda x: float(x)/10000, spikes)
	return statistics.firing_rate(bsSpikes)
