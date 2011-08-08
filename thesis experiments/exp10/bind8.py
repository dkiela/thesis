import brainsim8
import brainalyze
import scipy
import numpy as np
import matplotlib.pyplot as plt

parameters = {
        'ESYN_MAXCONDUCTANCE':0.068,
        'ISYN_MAXCONDUCTANCE':0.09,
        'CONN_LATERAL':1,
        'CONN_INTERNAL':1,
        'ENDSIM':2,
        'FSV':10000,
        'BRAINNAME':"vb-exp",
        'BRAINPREFIX':'vb-exp',
        'TAU_NOISE':0.020,
	'RATE1':73,
	'RATE2':5}

def plotVoltage(lJ,lM,lX,lY,lAP,lOP,lAQ,lOQ,lI):
	global parameters
	sp=np.linspace(0.0,parameters['ENDSIM'],parameters['ENDSIM']*parameters['FSV'])
	plt.title('Sequence: J,M,X,Y,AP,OP,AQ,OQ,I')
	plt.subplot(911)
	plt.plot(sp,lJ,'b')
	plt.subplot(912)
	plt.plot(sp,lM,'b')
	plt.subplot(913)
	plt.plot(sp,lX,'b')
	plt.subplot(914)
	plt.plot(sp,lY,'b')
	plt.subplot(915)
	plt.plot(sp,lAP,'b')
	plt.subplot(916)
	plt.plot(sp,lOP,'b')
	plt.subplot(917)
	plt.plot(sp,lAQ,'b')
	plt.subplot(918)
	plt.plot(sp,lOQ,'b')
	plt.subplot(919)
	plt.plot(sp,lI,'b')
	plt.show()

brainsim8.simBrain(parameters)
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

print "(John,x):", cJX
print "(John,y):", cJY
if cJX > cJY:
	print "(John = x)"
else:
	print "(John = y)"
print "(Mary,x):", cMX
print "(Mary,y):", cMY
if cMX > cMY:
	print "(Mary = x)"
else:
	print "(Mary = y)"

print "(x,AgentP):",cXAP
print "(x,AgentQ):",cXAQ
if cXAP > cXAQ:
	print "(x = AgentP)"
else:
	print "(x = AgentQ)"
print "(x,ObjectP):",cXOP
print "(x,ObjectQ):",cXOQ
if cXOP > cXOQ:
	print "(x = ObjectP)"
else:
	print "(x = ObjectQ)"

print "(y,AgentP):",cYAP
print "(y,AgentQ):",cYAQ
if cYAP > cYAQ:
	print "(y = AgentP)"
else:
	print "(y = AgentQ)"
print "(y,ObjectP):",cYOP
print "(y,ObjectQ):",cYOQ
if cYOP > cYOQ:
	print "(y = ObjectP)"
else:
	print "(y = ObjectQ)"

plotVoltage(lJ,lM,lX,lY,lAP,lOP,lAQ,lOQ,lI)
