import brain
import brainlab
import brainsim
import numpy
from numpy import pi
import scipy
from matplotlib import pyplot

# for external use
def genSpikePlotXY(prefix, num):
	listX = brainsim.loadBrain(prefix + str(num) + '-XReport.txt')
	listY = brainsim.loadBrain(prefix + str(num) + '-YReport.txt')
	c = numpy.linspace(0.0, len(listX), len(listX), endpoint=False)
	d = numpy.linspace(0.0, len(listY), len(listY), endpoint=False)
	pyplot.subplot(211)
	pyplot.title("Neuron X")
	pyplot.plot(c,listX)
	pyplot.subplot(212)
	pyplot.title("Neuron Y")
	pyplot.plot(d,listY)
	pyplot.show()

# for in-file use
def showSpikePlotXY():
	pyplot.subplot(211)
	pyplot.title("Neuron X")
	pyplot.plot(t,A)
	pyplot.subplot(212)
	pyplot.title("Neuron Y")
	pyplot.plot(t,B)
	pyplot.show()

def showCorrPlot():
	c = numpy.linspace(0.0, len(correlations), len(correlations), endpoint=False)
#	pyplot.subplot(211)
	pyplot.title("Correlations")
	pyplot.plot(c, numpy.array(correlations).astype(float), 'bo', c, numpy.array(spikecorr).astype(float), 'r')
#	pyplot.subplot(212)
#	pyplot.title("Phase shift")
#	pyplot.plot(c, numpy.array(totalcorr).astype(float), 'b')
	pyplot.show()

def giveCorrelation():
	xcorr = scipy.correlate(A, B)
	return xcorr

def givePhaseShift(xcorr):
	period=1.0
	dt = numpy.linspace(-t[-1], t[-1], 2*nsamples-1)
	recovered_time_shift = dt[sxcorr.argmax()]
	recovered_phase_shift = 2*pi*(((0.5 + recovered_time_shift/period) % 1.0) - 0.5)
	print 'Phase shift: ', recovered_phase_shift
	print 'Correlation: ', xcorr
	return recovered_phase_shift

from countspikes import countSpikes,totalCorrelation

spikecorr=[]
correlations=[]
totalcorr=[]
phases=[]
ii=float(0)
trials=10
esynval=0.0
isynval=1.0
while ii < trials:
	parameters = {
	'ESYN_MAXCONDUCTANCE':0, #0.05 ['']
	'ISYN_MAXCONDUCTANCE':0, #0.4
	'CONN_LATERAL':1, #0.02
	'CONN_INTERNAL':1, #0.02
	'ENDSIM':2, 
	'FSV':10000,
	'BRAINNAME':"vb-exp1",
	'TAU_NOISE':0.020} #0.020

#	parameters['CONN_INTERNAL']=i/100
#	parameters['CONN_LATERAL']=i/100
	parameters['ESYN_MAXCONDUCTANCE']=esynval
	parameters['ISYN_MAXCONDUCTANCE']=isynval
	esynval=esynval+0.01
	isynval=isynval-0.1
#	parameters['TAU_NOISE']=(trials-i)/trials

	parameters['BRAINNAME']='vb-exp'+str(int(ii))
	brainsim.simBrain(parameters)
	listX = brainsim.loadBrain(parameters['BRAINNAME']+'-XReport.txt')
	listY = brainsim.loadBrain(parameters['BRAINNAME']+'-YReport.txt')

	nsamples=len(listX)
	t = numpy.linspace(0.0, parameters['ENDSIM'], nsamples, endpoint=False)
	A=numpy.array(listX).astype(float)
	B=numpy.array(listY).astype(float)

	# Purely spike correlation
	cntX,spikesX = countSpikes(listX)
	cntY,spikesY = countSpikes(listY)
	print "cntX,spikesX: ", cntX, spikesX
	print "cntY,spikesY: ", cntY, spikesY
	sxcorr = scipy.correlate(spikesX, spikesY)
	spikecorr.append(sxcorr[sxcorr.argmax()])

	# Overall correlation
	xcorr = giveCorrelation()
	correlations.append(xcorr[xcorr.argmax()])

	# Total_correlation from Brian Simulator
	#totalcorr.append(-1*totalCorrelation(spikesX,spikesY,cntX,cntY)*100000)

	# Phase shift
	phases.append(givePhaseShift(xcorr))
#	showSpikePlotXY()
	ii=ii+1

print "Spike Correlations:", spikecorr
print "Total Correlation Coeff's:",totalcorr
print "Correlations:", correlations
print "Phases", phases

showCorrPlot()

# This doesn't work yet, fix me
def show3DPlot():
	from mpl_toolkits.mplot3d import Axes3D
	from matplotlib import cm
	from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
	import matplotlib.pyplot as plt
	import numpy as np
	import scipy as sp
	import brainsim
	from countspikes import countSpikes

	fig = plt.figure()
	ax = fig.gca(projection='3d')
	vals=np.array(range(0,10))
	X = map(lambda x: float(x)/100, vals)
	Y = map(lambda x: float(x)/10, vals[::-1]) # ISYN

	X, Y = np.meshgrid(X, Y)
	#R = np.sqrt(X**2 + Y**2)
	#Z = np.sin(R)
	listX=brainsim.loadBrain("vb-exp77-XReport.txt")
	listY=brainsim.loadBrain("vb-exp77-YReport.txt")
	cntX,spikesX=countSpikes(listX)
	cntY,spikesY=countSpikes(listY)
	Z=np.array(spikecorr)
	Z=np.array([Z, Z, Z, Z, Z, Z, Z, Z, Z, Z])

	surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet,
		linewidth=0, antialiased=False)
	ax.set_zlim3d(np.argmin(Z), np.argmax(Z))

	ax.w_zaxis.set_major_locator(LinearLocator(10))
	ax.w_zaxis.set_major_formatter(FormatStrFormatter('%.03f'))

	fig.colorbar(surf, shrink=0.5, aspect=5)

	plt.show()
