import bsim
import brainalyze
import scipy
import numpy as np
import matplotlib.pyplot as plt

parameters = {
        'ESYN_MAXCONDUCTANCE':0.085,
        'ISYN_MAXCONDUCTANCE':0.55,
        'CONN_LATERAL':1,
        'CONN_INTERNAL':1,
        'ENDSIM':2, #12
        'FSV':10000,
        'BRAINNAME':"vb-exp",
        'BRAINPREFIX':'vb-exp',
        'TAU_NOISE':0.020,
	'RATE1':73,#73
	'RATE2':5}#5

def plotUse():
	global parameters
	sp=np.linspace(0.0,parameters['ENDSIM'],
		1 + parameters['ENDSIM'] * parameters['FSV'])
	lB=bsim.loadBrain('vb-exp-BUseReport.txt')
	lG=bsim.loadBrain('vb-exp-GUseReport.txt')
	lT=bsim.loadBrain('vb-exp-TUseReport.txt')
	lS=bsim.loadBrain('vb-exp-SUseReport.txt')
	plt.subplot(221)
	plt.title('Blue Use')
	plt.plot(sp,lB,'g')
	plt.subplot(222)
	plt.title('Green Use')
	plt.plot(sp,lG,'g')
	plt.subplot(223)
	plt.title('Triangle Use')
	plt.plot(sp,lT,'g')
	plt.subplot(224)
	plt.title('Square Use')
	plt.plot(sp,lS,'g')
	plt.show()

def plotVoltage():
	global parameters
	sp=np.linspace(0.0,parameters['ENDSIM'],parameters['ENDSIM']*parameters['FSV'])
	lB=bsim.loadBrain('vb-exp-BReport.txt')
	lG=bsim.loadBrain('vb-exp-GReport.txt')
	lT=bsim.loadBrain('vb-exp-TReport.txt')
	lS=bsim.loadBrain('vb-exp-SReport.txt')
	lI=bsim.loadBrain('vb-exp-IReport.txt')
	plt.subplot(511)
	plt.plot(sp,lB,'b')
	plt.subplot(512)
	plt.plot(sp,lG,'b')
	plt.subplot(513)
	plt.plot(sp,lT,'b')
	plt.subplot(514)
	plt.plot(sp,lS,'b')
	plt.subplot(515)
	plt.plot(sp,lI,'b')
	plt.show()

john="NB"
mary="NG"
rates={john:5,mary:73}
def Loves(x,y):
	global parameters
	parameters['RATE1']=rates[x]
	parameters['RATE2']=rates[y]

def qLoves(x,y):
	lB=bsim.loadBrain('vb-exp-BReport.txt')
	lG=bsim.loadBrain('vb-exp-GReport.txt')
	lT=bsim.loadBrain('vb-exp-TReport.txt')
	lS=bsim.loadBrain('vb-exp-SReport.txt')
	_,spikesB=brainalyze.countSpikes(lB,10000*(parameters['ENDSIM']/2))
	_,spikesG=brainalyze.countSpikes(lG,10000*(parameters['ENDSIM']/2))
	_,spikesT=brainalyze.countSpikes(lT,10000*(parameters['ENDSIM']/2))
	_,spikesS=brainalyze.countSpikes(lS,10000*(parameters['ENDSIM']/2))

	if x[1]=='B':
		spikesA=spikesB
	elif x[1]=='G':
		spikesA=spikesG
	if y[1]=='B':
		spikesO=spikesB
	elif y[1]=='G':
		spikesO=spikesG

	cBT=brainalyze.corr(spikesB,spikesT)#/(brainalyze.corr(spikesT,spikesS)/1)
	cGT=brainalyze.corr(spikesG,spikesT)#/(brainalyze.corr(spikesT,spikesS)/1)
	cBS=brainalyze.corr(spikesB,spikesS)#/(brainalyze.corr(spikesS,spikesT)/1)
	cGS=brainalyze.corr(spikesG,spikesS)#/(brainalyze.corr(spikesS,spikesT)/1)

	cAT=brainalyze.corr(spikesA,spikesT)#/(brainalyze.corr(spikesS,spikesT)/1)
	cOT=brainalyze.corr(spikesO,spikesT)#/(brainalyze.corr(spikesS,spikesT)/1)
	cAS=brainalyze.corr(spikesA,spikesS)#/(brainalyze.corr(spikesS,spikesT)/1)
	cOS=brainalyze.corr(spikesO,spikesS)#/(brainalyze.corr(spikesS,spikesT)/1)

	print "john = Lover (cBT)", cBT*100
	print "mary = Lover (cGT)", cGT*100
	print "john = Lovee (cBS)", cBS*100
	print "mary = Lovee (cGS)", cGS*100
	print "x = Lover (cAT)", cAT*100
	print "y = Lover (cOT)", cOT*100
	print "x = Lovee (cAS)", cAS*100
	print "y = Lovee (cOS)", cOS*100

	if x != y and cAT > cOT and cOS > cAS:
		return True
	elif x == y:
		# this is a bit of a hack, but can be made not to depend on x or y
		if x==john and cBT > cBS and cGT > cGS and cBT >= cGT and cBS >= cGS:
			return True
		elif x==mary and cBS > cBT and cGS > cGT and cGT >= cBT and cGS >= cBS:
			return True
		else:
			return False
	else:
		return False

bradb=0

def init():
	global bradb
	bradb=bsim.simBrain(parameters)
#	return bradb

def run():
	global bradb
	bsim.injectBrain(bradb,parameters)
	bsim.runBrain(bradb)

#Loves(john,john)
#print qLoves(john,john)
