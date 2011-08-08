from vbstore import *
import brainalyze
import numpy as np
import matplotlib.pyplot as plt

john="NB"
mary="NG"
agent = "NT"
object = "NS"
X = 101
Y = 102
ran = False
bradb = 1
rates={john:5, mary:73}

# Fixed nolearing parameters
ma_nl=1.0 #1.20842430845
ja_nl=1.0 #-0.0413955945683
mo_nl=1.0 #0.540109924163
jo_nl=1.0 #0.106073172277

parameters = {
        'ESYN_MAXCONDUCTANCE':0.085,
        'ISYN_MAXCONDUCTANCE':0.55,
        'CONN_LATERAL':1,
        'CONN_INTERNAL':1,
        'ENDSIM':2,
	'LEARNING':'1',
        'FSV':10000,
        'BRAINNAME':"vb-exp",
        'BRAINPREFIX':'vb-exp',
        'TAU_NOISE':0.020,
        'RATE1':5,
        'RATE2':3}

def plotVoltage():
        global parameters
        sp=np.linspace(0.0,parameters['ENDSIM'],parameters['ENDSIM']*parameters['FSV'])
        lB=loadBrain('vb-exp-'+john+'Report.txt')
        lG=loadBrain('vb-exp-'+mary+'Report.txt')
        lT=loadBrain('vb-exp-'+agent+'Report.txt')
        lS=loadBrain('vb-exp-'+object+'Report.txt')
        lI=loadBrain('vb-exp-NIReport.txt')
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

def init():
	global bradb
	global ran
	global ja_nl, ma_nl, jo_nl, mo_nl
	bradb = initBrain(parameters)
	ran = False
	print "Done"

def run():
	# run simulation
	global ran
	injectBrain(bradb, mary, rates[mary], 0.0, parameters['ENDSIM'])
	injectBrain(bradb, john, rates[john], 0.0, parameters['ENDSIM'])
	runBrain(bradb)
	ran = True
	print "Done"

def reset():
	global ran, bradb
	ran = False
	bradb = initBrain(parameters)
	print "Done"

def Loves(x,y):
	if not ran:
		if x == X or x == Y or y == X or y == Y:
			print "Error: variables not allowed in declarative phase."
			return False
		global bradb
		# inject stimulus object
		injectBrain(bradb, agent, rates[x], 0.0, parameters['LEARNING'])
		injectBrain(bradb, object, rates[y], 0.0, parameters['LEARNING'])
		print "Stored"
	else:
		lX=loadBrain(parameters['BRAINNAME']+'-'+x+'Report.txt')
		lA=loadBrain(parameters['BRAINNAME']+'-'+agent+'Report.txt')
		lY=loadBrain(parameters['BRAINNAME']+'-'+y+'Report.txt')
		lO=loadBrain(parameters['BRAINNAME']+'-'+object+'Report.txt')

		_,spikesX=brainalyze.countSpikes(lX,10000*parameters['LEARNING'])
		_,spikesA=brainalyze.countSpikes(lA,10000*parameters['LEARNING'])

		_,spikesY=brainalyze.countSpikes(lY,10000*parameters['LEARNING'])
		_,spikesO=brainalyze.countSpikes(lO,10000*parameters['LEARNING'])

		xAg = brainalyze.corr(spikesX,spikesA)
		yAg = brainalyze.corr(spikesY,spikesA)
		xObj = brainalyze.corr(spikesX,spikesO)
		yObj = brainalyze.corr(spikesY,spikesO)

                if x == mary:
                        xAgc=xAg/ma_nl
                        yAgc=yAg/ja_nl
                if x == john:
                        xAgc=xAg/ja_nl
                        yAgc=yAg/ma_nl
                if y == mary:
                        yObjc=yObj/mo_nl
                        xObjc=xObj/jo_nl
                if y == john:
                        yObjc=yObj/jo_nl
                        xObjc=xObj/mo_nl

		print "X Agent, Y Agent ", xAg,yAg
		print "X Object, Y Object ", xObj,yObj
#		print "Coeff xAg/yAg ", xAg/yAg
#		print "Coeff yObj/xObj", yObj/xObj
		print "(Corrected) X Agent, Y Agent ", xAgc,yAgc
		print "(Corrected) X Object, Y Object ", xObjc,yObjc

		if xAgc > yAgc and yObjc > xObjc:
			return True
		else:
			return False

def testHebb():
	global parameters
	l=[]
	i=1
	j=1
	while i <= 10:
		print i
		correct1=False
		correct2=False
		parameters['LEARNING']=float(i)/10.0
		parameters['ENDSIM']=i

		init()
		Loves(john,mary)
		run()
		if Loves(john,mary):
			correct1=True
		else:
			correct1=False

		reset()
		Loves(mary,john)
		run()
		if Loves(mary,john):
			correct2=True
		else:
			correct2=False

		l.append(correct1 and correct2)
		print correct1 and correct2
		i=i+1
	print l

def singleSample():
	init()
	Loves(john,mary)
	run()
	print Loves(john,mary)
	reset()
	Loves(mary,john)
	run()
	print Loves(mary,john)

#testHebb()
singleSample()
#print "Loves(mary,john)", Loves(mary,john)
#print "Loves(john,mary)", Loves(john,mary)
#print "Loves(john,john)"
#Loves(john,john)
#print "Loves(mary,mary)"
#Loves(mary,mary)

#plotVoltage()
