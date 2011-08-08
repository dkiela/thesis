#!/usr/bin/env python

import brain
import brainlab
import numpy
import scipy

#parameters = {'ESYN_MAXCONDUCTANCE':['0.05'],'ISYN_MAXCONDUCTANCE':['0.4'],'CONN_LATERAL':0.02,'CONN_INTERNAL':0.02,'ENDSIM':2,'FSV':10000,'BRAINNAME':"vb-exp1",'TAU_NOISE':['0.020']}

def initBrain(parameters):
	print "Received parameters:"
	print parameters
	brainname=parameters['BRAINNAME']
	endsim=parameters['ENDSIM']		# number of seconds the simulation runs (2)
	FSV=parameters['FSV'] 		# simulation timesteps per second
	timesteps=FSV*endsim	# simulated brain time
	d=(0.0, endsim)		# duration for reports

	bradb=brainlab.BRAIN(simsecs=endsim, jobname=brainname, fsv = FSV)

	bradb.SelectLib('standard')
	lib=bradb.libs['standard']
	syntypes=lib['syntypes']
	comptypes=lib['comptypes']
	celltypes=lib['celltypes']
	chantypes=lib['chantypes']
	synlearn=lib['sls']         #Hebb learning
	synfadep=lib['sfds']        #Facilitation - Depression
	synaug=lib['sas']           #Augmentation

	comp=comptypes['SOMA1']
	comp.parms['TAU_MEMBRANE']=['0.020,0.0']
	comp.parms['R_MEMBRANE']=['200,0.0']          # Membrane capacitance = 1 
	comp.parms['LEAK_CONDUCTANCE']=['0.00005,0.0']
	comp.parms['LEAK_REVERSAL']=['-60,0.0']
	comp.parms['THRESHOLD']=['-50,0.0']
	comp.parms['VMREST']=['-60,0.0']

	# Synapses
	esyns=syntypes['E']
	isyns=syntypes['I']
	esyns.parms['ABSOLUTE_USE']=['0.250,0.0']
	isyns.parms['ABSOLUTE_USE']=['0.250,0.0']
	esyns.parms['TYPE']='Excsyn'
	isyns.parms['TYPE']='Inhsyn'
	esyns.parms['MAX_CONDUCT']=parameters['ESYN_MAXCONDUCTANCE']
	isyns.parms['MAX_CONDUCT']=parameters['ISYN_MAXCONDUCTANCE']
	esyns.parms['SYN_REVERSAL']=['0,0']
	isyns.parms['SYN_REVERSAL']=['-80,0']
	esyns.parms['DELAY']=['0.0000000001,0.0000000001']  #Zirpe 2007
	isyns.parms['DELAY']=['0.0000000001,0.0000000001']
	esyns.parms['SFD']=['None']             #'Both' / 'None'
	isyns.parms['SFD']=['None']
	esyns.parms['LEARN_LABEL']=synlearn['BHebb']        #BHebb
	isyns.parms['LEARN_LABEL']=synlearn['BHebb']        #BHebb

	# Keep learning on for whole simulation, but stimulate only for half
	#(see stimuli below)
	esyns.parms['HEBB_START']=['0'] # 50 ms 
	esyns.parms['HEBB_END']=[parameters['LEARNING']]   #time in secs
	isyns.parms['HEBB_START']=['0']
	isyns.parms['HEBB_END']=[parameters['LEARNING']]

	### Construct the actual cell, layer and column setup
	ecell=celltypes['E']
	icell=celltypes['I']

	x, y, w, h=(100, 200, 50, 80) # columns coordinates

	col=bradb.COLUMN({"TYPE":"COLXY","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
	bradb.AddColumn(col)

	n_b = bradb.LAYER({"TYPE":"NB", "_UPPER":100, "_LOWER":67})
	n_b.AddCellType(ecell,1)
	col.AddLayerType(n_b)

	n_g = bradb.LAYER({"TYPE":"NG", "_UPPER":100, "_LOWER":67})
	n_g.AddCellType(ecell,1)
	col.AddLayerType(n_g)
	
	n_t = bradb.LAYER({"TYPE":"NT", "_UPPER":100, "_LOWER":67})
	n_t.AddCellType(ecell,1)
	col.AddLayerType(n_t)
	
	n_s = bradb.LAYER({"TYPE":"NS", "_UPPER":100, "_LOWER":67})
	n_s.AddCellType(ecell,1)
	col.AddLayerType(n_s)
	
	n_i = bradb.LAYER({"TYPE":"INHIBITOR", "_UPPER":100, "_LOWER":67})
	n_i.AddCellType(icell,1)
	col.AddLayerType(n_i)

	# Internal connections (this is not really necessary since we have only one neuron in each assembly)
	n_b.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	n_g.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	n_t.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	n_s.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	n_i.AddConnect((icell),(icell), isyns,prob=parameters['CONN_INTERNAL'])

	# Excitatory connections: blue-triangle,green-triangle,blue-square,green-square,all-inhibit
	bradb.AddConnect((col,n_b,ecell),(col,n_t,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_t,ecell),(col,n_b,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_g,ecell),(col,n_t,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_t,ecell),(col,n_g,ecell), esyns, prob=parameters['CONN_LATERAL'])

	bradb.AddConnect((col,n_b,ecell),(col,n_s,ecell),esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_s,ecell),(col,n_b,ecell),esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_g,ecell),(col,n_s,ecell),esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_s,ecell),(col,n_g,ecell),esyns, prob=parameters['CONN_LATERAL'])

	bradb.AddConnect((col,n_b,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_g,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_t,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_s,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])

	# Inhibitory connections: inhibit-all
	bradb.AddConnect((col,n_i,icell),(col,n_b,ecell), isyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_i,icell),(col,n_g,ecell), isyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_i,icell),(col,n_t,ecell), isyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_i,icell),(col,n_s,ecell), isyns, prob=parameters['CONN_LATERAL'])

	bradb.AddSimpleReport("NBReport", (col,n_b,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("NGReport", (col,n_g,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("NTReport", (col,n_t,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("NSReport", (col,n_s,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("NIReport", (col,n_i,icell), reptype="v", dur=d)

#	bradb.AddSimpleReport("BUseReport", (col,n_b,ecell), synname=esyns, reptype="a", dur=d)
#	bradb.AddSimpleReport("GUseReport", (col,n_g,ecell), synname=esyns, reptype="a", dur=d)
#	bradb.AddSimpleReport("TUseReport", (col,n_t,ecell), synname=esyns, reptype="a", dur=d)
#	bradb.AddSimpleReport("SUseReport", (col,n_s,ecell), synname=esyns, reptype="a", dur=d)

	return bradb

def injectBrain(bradb, type, rate, time_start=0.0, time_end=1.0):
	s=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
	s.parms['AMP_START']='0.3'
	s.parms['AMP_END']='0.3'
	s.parms['TIME_START']=str(time_start)
	s.parms['TIME_END']=str(time_end)
	s.parms['RATE']=str(rate)
	s.parms['TAU_NOISE']=0#0.02#parameters['TAU_NOISE']
	s.parms['CORREL']=['0']
	s.parms['SEED']=['-11']

	stim=bradb.STIMULUS_INJECT()
	stim.parms['STIM_TYPE']=s
	randomnumber=str(int(scipy.rand(1)[0]*10000))
	stim.parms['TYPE']='simple_inject_'+randomnumber
	stim.parms['INJECT']=['COLXY '+ type +' E SOMA1_name 1']

	bradb.AddStimInject(stim)

	return True

def runBrain(bradb):
	brainlab.Run(bradb, verbose=False, nprocs=1)

def loadBrain(fn):
	#f=open(fn)
	#l=len(f.readline().split())
	#f.close()
	f=open(fn)
	f.seek(0)
	dd=[]
	line=0
	for i in f.readlines():
		#print i #debug
		d=i.strip().split()

		try:
			d.pop(0)
		except IndexError:
			print "IndexError for pop() on line ", l

		try:
			n=numpy.array(map(float, d))
		except ValueError:
			print "ValueError for float(): ", i
			n=numpy.array(-80.0000)

		dapp=numpy.average(n) # only one neuron per report, so not really necessary, alternative:
		#dapp=d.pop(0)
		dd.append(dapp)
		line=line+1
	f.close()
	return dd
