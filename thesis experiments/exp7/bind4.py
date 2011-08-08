import brainsim
import brainalyze
import scipy
import numpy as np
import matplotlib.pyplot as plt

parameters = {
        'ESYN_MAXCONDUCTANCE':0.085,
        'ISYN_MAXCONDUCTANCE':0.55,
        'CONN_LATERAL':1,
        'CONN_INTERNAL':1,
        'ENDSIM':12,
        'FSV':10000,
        'BRAINNAME':"vb-exp",
        'BRAINPREFIX':'vb-exp',
        'TAU_NOISE':0.020}

def plotUse():
	global parameters
	sp=np.linspace(0.0,parameters['ENDSIM'],
		1 + parameters['ENDSIM'] * parameters['FSV'])
	lB=brainsim.loadBrain('vb-exp-BUseReport.txt')
	lG=brainsim.loadBrain('vb-exp-GUseReport.txt')
	lT=brainsim.loadBrain('vb-exp-TUseReport.txt')
	lS=brainsim.loadBrain('vb-exp-SUseReport.txt')
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
	lB=brainsim.loadBrain('vb-exp-BReport.txt')
	lG=brainsim.loadBrain('vb-exp-GReport.txt')
	lT=brainsim.loadBrain('vb-exp-TReport.txt')
	lS=brainsim.loadBrain('vb-exp-SReport.txt')
	lI=brainsim.loadBrain('vb-exp-IReport.txt')
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

brainsim.simBrain(parameters)
lB=brainsim.loadBrain('vb-exp-BReport.txt')
lG=brainsim.loadBrain('vb-exp-GReport.txt')
lT=brainsim.loadBrain('vb-exp-TReport.txt')
lS=brainsim.loadBrain('vb-exp-SReport.txt')
_,spikesB=brainalyze.countSpikes(lB,10000*(parameters['ENDSIM']/2))
_,spikesG=brainalyze.countSpikes(lG,10000*(parameters['ENDSIM']/2))
_,spikesT=brainalyze.countSpikes(lT,10000*(parameters['ENDSIM']/2))
_,spikesS=brainalyze.countSpikes(lS,10000*(parameters['ENDSIM']/2))
cBT=brainalyze.corr(spikesB,spikesT)/(brainalyze.corr(spikesT,spikesS)/1)
cGT=brainalyze.corr(spikesG,spikesT)/(brainalyze.corr(spikesT,spikesS)/1)
cBS=brainalyze.corr(spikesB,spikesS)/(brainalyze.corr(spikesS,spikesT)/1)
cGS=brainalyze.corr(spikesG,spikesS)/(brainalyze.corr(spikesS,spikesT)/1)

#cBS=cBS+10
#cGS=cGS+10
#cBS=(cBS/cGS)*cBT
#cGS=cBT

print "Blue Triangle", cBT*100
print "Green Triangle", cGT*100
print "Blue Square", cBS*100
print "Green Square", cGS*100


#plotUse()
plotVoltage()
