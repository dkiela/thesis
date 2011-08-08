import brainsim
import numpy
import scipy

def countSpikes (l):
	a = numpy.array (l)
	count = 0 
	i = 0 
	thres = 0.0 
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

def run ():
	exp = 99
	listX = brainsim.loadBrain ("vb-exp" + str (exp) + "-XReport.txt")
	listY = brainsim.loadBrain ("vb-exp" + str (exp) + "-YReport.txt")
	cntX, spikesX = countSpikes (listX)
	cntY, spikesY = countSpikes (listY)
	print cntX
	print cntY
	print spikesX
	print spikesY
	print "SIGNAL CORRELATION: ", scipy.correlate (spikesX, spikesY)
	print "MAX: ",  scipy.correlate (spikesX, spikesY).argmax()
	print "Total spike correlation (Brian func.): ", totalCorrelation(spikesX,spikesY,cntX,cntY)

	from matplotlib import pyplot

	pyplot.subplot (211)
	pyplot.plot (numpy.linspace (0.0, len (listX), len (listX)), listX)
	pyplot.subplot (212)
	pyplot.plot (numpy.linspace (0.0, len (listY), len (listY)), listY)
	pyplot.show ()

ms=0.001

def totalCorrelation (T1, T2, Cnt1, Cnt2, width = 20 * ms, T = None):
	if (T1 ==[]) or (T2 ==[]):
		# empty spike train
		#return nan
		return "EMPTY"
	# Remove units
	width = float (width) 
	T1 = numpy.array (T1) 
	T2 = numpy.array (T2)
	# Divide by time to get rate
	if T is None:
		T = max(T1[-1], T2[-1]) - min(T1[0], T2[0])
	i = 0
	j = 0
	x = 0
	for t in T1:
		while i < len(T2) and T2[i] < t - width: # other possibility use searchsorted
			i += 1
		while j < len(T2) and T2[j] < t + width:
			j += 1
		x += sum(1. / (T - abs(T2[i:j] - t))) # counts coincidences with windowing (probabilities)

	return float(x / Cnt1) - float(Cnt2 * 2 * width)

#run()
