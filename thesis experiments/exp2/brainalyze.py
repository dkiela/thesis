import brain
import brainlab
import brainsim
import numpy
from numpy import pi
import scipy
from matplotlib import pyplot

# This is not really used anymore, for now
def givePhaseShift(xcorr):
	period=1.0
	dt = numpy.linspace(-t[-1], t[-1], 2*nsamples-1)
	recovered_time_shift = dt[sxcorr.argmax()]
	recovered_phase_shift = 2*pi*(((0.5 + recovered_time_shift/period) % 1.0) - 0.5)
	print 'Phase shift: ', recovered_phase_shift
	print 'Correlation: ', xcorr
	return recovered_phase_shift

def countSpikes (l):
	a = numpy.array (l)
	count = 0 
	i = 0
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

def loadExperiment (prefix, exp):
	listX = brainsim.loadBrain (prefix + str (exp) + "-XReport.txt")
	listY = brainsim.loadBrain (prefix + str (exp) + "-YReport.txt")
	cntX, spikesX = countSpikes (listX)
	cntY, spikesY = countSpikes (listY)
	return (listX,cntX,spikesX),(listY,cntY,spikesY)
