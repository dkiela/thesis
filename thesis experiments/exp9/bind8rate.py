import brainsim8
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
        'ENDSIM':2,
        'FSV':10000,
        'BRAINNAME':"vb-exp",
        'BRAINPREFIX':'vb-exp',
        'TAU_NOISE':0.020,
	'RATE1':0,
	'RATE2':0}

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

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
rates = np.array(primes)
store = np.zeros((len(rates),len(rates)))
x=0
y=0
while x < len(rates):
	while y < len(rates):
		parameters['RATE1']=rates[x]
		parameters['RATE2']=rates[y]
		parameters['BRAINNAME']='vb-exp'+str(rates[x])+'-'+str(rates[y])
		brainsim8.simBrain(parameters)
		y=y+1
	y=0 #reset
	x=x+1

x=0
y=0
while x < len(rates):
	while y < len(rates):
		print rates[x],rates[y]
		lJ=brainsim8.loadBrain('vb-exp-JReport.txt')
		lM=brainsim8.loadBrain('vb-exp-MReport.txt')
		lX=brainsim8.loadBrain('vb-exp-XReport.txt')
		lY=brainsim8.loadBrain('vb-exp-YReport.txt')
		lAP=brainsim8.loadBrain('vb-exp-APReport.txt')
		lOP=brainsim8.loadBrain('vb-exp-OPReport.txt')
		lAQ=brainsim8.loadBrain('vb-exp-AQReport.txt')
		lOQ=brainsim8.loadBrain('vb-exp-OQReport.txt')
		lI=brainsim8.loadBrain('vb-exp-IReport.txt')
		_,spikesJ=brainalyze.countSpikes(lJ,10000*(parameters['ENDSIM']/2))
		_,spikesM=brainalyze.countSpikes(lM,10000*(parameters['ENDSIM']/2))
		_,spikesX=brainalyze.countSpikes(lX,10000*(parameters['ENDSIM']/2))
		_,spikesY=brainalyze.countSpikes(lY,10000*(parameters['ENDSIM']/2))
		_,spikesAP=brainalyze.countSpikes(lAP,10000*(parameters['ENDSIM']/2))
		_,spikesOP=brainalyze.countSpikes(lOP,10000*(parameters['ENDSIM']/2))
		_,spikesAQ=brainalyze.countSpikes(lAQ,10000*(parameters['ENDSIM']/2))
		_,spikesOQ=brainalyze.countSpikes(lOQ,10000*(parameters['ENDSIM']/2))
		cJX=brainalyze.corr(spikesJ,spikesX)
		cMX=brainalyze.corr(spikesM,spikesX)
		cJY=brainalyze.corr(spikesJ,spikesY)
		cMY=brainalyze.corr(spikesM,spikesY)

		cXAP=brainalyze.corr(spikesX,spikesAP)
		cXOP=brainalyze.corr(spikesX,spikesOP)
		cXAQ=brainalyze.corr(spikesX,spikesAQ)
		cXOQ=brainalyze.corr(spikesX,spikesOQ)

		cYAP=brainalyze.corr(spikesY,spikesAP)
		cYOP=brainalyze.corr(spikesY,spikesOP)
		cYAQ=brainalyze.corr(spikesY,spikesAQ)
		cYOQ=brainalyze.corr(spikesY,spikesOQ)

		avg = (abs(cJX - cJY) + abs(cMY - cMX) + abs(cXAP - cXAQ) + abs(cXOQ - cXOP) + abs(cXAQ - cXAP) + abs(cXOP - cXOQ))/6

		# John is x, Mary is y, x is AP,OQ, y is AQ,OP
		if cJX > cJY and cMY > cMX and cXAP > cXAQ and cXOQ > cXOP and cYAQ > cYAP and CYOP > CYOQ:
			store[x][y]=avg
		else:
			store[x][y]=-1*avg
		y=y+1
	y=0 #reset
	x=x+1

np.save('rate8store.npy', store)

print "Done"

data=np.load('rate8store.npy')
(x,y) = np.unravel_index(data.argmax(), data.shape)
max=data[x][y]
(x,y) = np.unravel_index(data.argmin(), data.shape)
min=data[x][y]

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.imshow(data, interpolation='nearest')
ax.set_title('Correlation Difference (ESYN=0.085 ISYN=0.55)')
plt.ylabel('Rate1 (primes 2-97)')
plt.xlabel('Rate2 (primes 2-97)')
cbar = fig.colorbar(cax, ticks=[min, 0, max])
#       cbar.ax.set_yticklabels([str(-max), '0', str(max)])
plt.show()

# OPTIMUM: 5/73


#cBS=cBS+10
#cGS=cGS+10
#cBS=(cBS/cGS)*cBT
#cGS=cBT

#print "Blue Triangle", cBT*100
#print "Green Triangle", cGT*100
#print "Blue Square", cBS*100
#print "Green Square", cGS*100


#plotUse()
#plotVoltage()
