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
        'ENDSIM':0, #filled in by predicate #12
        'FSV':10000,
        'BRAINNAME':"vb-exp",
        'BRAINPREFIX':'vb-exp',
        'TAU_NOISE':0.020,
	'RATE1':73,#73
	'RATE2':5}#5

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
agent='NT'
object='NS'
rates={john:5,mary:73}
learntime=1.0
learn_preds=0

def Loves(x,y):
	global parameters
	global bradb
	global learn_preds
	parameters['RATE1']=rates[x]
	parameters['RATE2']=rates[y]
	parameters['ENDSIM']=parameters['ENDSIM']+(learntime*2) # extend simulation time

	# x as agent (rate 1) and y as object (rate 2)
	bsim.injectStim(bradb,parameters,parameters['RATE1'],learn_preds,learn_preds+learntime,agent)
	bsim.injectStim(bradb,parameters,parameters['RATE2'],learn_preds,learn_preds+learntime,object)
	learn_preds=learn_preds+1

	# Do this in run:
	#bsim.injectStim(bradb,parameters,parameters['RATE1'],0.0,parameters['ENDSIM'],x) #john?
	#bsim.injectStim(bradb,parameters,parameters['RATE2'],0.0,parameters['ENDSIM'],y) #mary?

def qLoves(x,y):
	global parameters

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
	global parameters
	bradb=bsim.simBrain(parameters)
#	return bradb

def run():
	global bradb
	global parameters
#	bsim.injectBrain(bradb,parameters)
	bsim.injectStim(bradb,parameters,parameters['RATE1'],0.0,parameters['ENDSIM'],john) #john?
	bsim.injectStim(bradb,parameters,parameters['RATE2'],0.0,parameters['ENDSIM'],mary) #mary?
	bradb.parms['DURATION']=str(parameters['ENDSIM'])
	bsim.runBrain(bradb, (0.0,parameters['ENDSIM']))

init()
#Loves(john,john)
#print qLoves(john,john)
