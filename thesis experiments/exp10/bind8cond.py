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
	'RATE1':73,
	'RATE2':5}

# (rates = conductances)
rates = np.array(range(0,100))
store = np.zeros((len(rates),len(rates)))
#x=0
#y=0
#while x < len(rates):
#	while y < len(rates):
#		parameters['ESYN_MAXCONDUCTANCE']=float(rates[x])/1000.0
#		parameters['ISYN_MAXCONDUCTANCE']=float(rates[y])/100.0
#		parameters['BRAINNAME']='vb-exp'+str(x)+'-'+str(y)
#		brainsim8.simBrain(parameters)
		# For speed:
		# - move associated Report files to separate folder
		# - remove associated files
#		y=y+1
#	y=0 #reset
#	x=x+1

x=0
y=0
while x < len(rates):
	while y < len(rates):
		print rates[x],rates[y]
		lJ=brainsim8.loadBrain('vb-exp'+str(x)+'-'+str(y)+'-JReport.txt')
		lM=brainsim8.loadBrain('vb-exp'+str(x)+'-'+str(y)+'-MReport.txt')
		lX=brainsim8.loadBrain('vb-exp'+str(x)+'-'+str(y)+'-XReport.txt')
		lY=brainsim8.loadBrain('vb-exp'+str(x)+'-'+str(y)+'-YReport.txt')
		lAP=brainsim8.loadBrain('vb-exp'+str(x)+'-'+str(y)+'-APReport.txt')
		lOP=brainsim8.loadBrain('vb-exp'+str(x)+'-'+str(y)+'-OPReport.txt')
		lAQ=brainsim8.loadBrain('vb-exp'+str(x)+'-'+str(y)+'-AQReport.txt')
		lOQ=brainsim8.loadBrain('vb-exp'+str(x)+'-'+str(y)+'-OQReport.txt')
		lI=brainsim8.loadBrain('vb-exp'+str(x)+'-'+str(y)+'-IReport.txt')
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

np.save('conduct8store.npy', store)

print "Done"

data=np.load('conduct8store.npy')
data=np.array(map(lambda x: x+0.5, data)) #added
blah=np.vsplit(data,2)
data=blah[1]
(x,y) = np.unravel_index(data.argmax(), data.shape)
max=data[x][y]
(x,y) = np.unravel_index(data.argmin(), data.shape)
min=data[x][y]

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.imshow(data, interpolation='nearest')
ax.set_title('Correlation Difference (over conductances)')
plt.ylabel('ESYN')
plt.xlabel('ISYN')
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
