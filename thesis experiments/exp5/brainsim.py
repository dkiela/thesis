#!/usr/bin/env python

import brain
import brainlab
import numpy

#parameters = {'ESYN_MAXCONDUCTANCE':['0.05'],'ISYN_MAXCONDUCTANCE':['0.4'],'CONN_LATERAL':0.02,'CONN_INTERNAL':0.02,'ENDSIM':2,'FSV':10000,'BRAINNAME':"vb-exp1",'TAU_NOISE':['0.020']}

def simBrain(parameters):
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
	esyns.parms['HEBB_END']=['2']   #time in secs
	isyns.parms['HEBB_START']=['0']
	isyns.parms['HEBB_END']=['2']

	### Construct the actual cell, layer and column setup
	ecell=celltypes['E']
	icell=celltypes['I']

	x, y, w, h=(100, 200, 50, 80) # columns coordinates

	col=bradb.COLUMN({"TYPE":"COLXY","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
	bradb.AddColumn(col)

	# Blue
	n_b = bradb.LAYER({"TYPE":"NB", "_UPPER":100, "_LOWER":67})
	n_b.AddCellType(ecell,1)
	col.AddLayerType(n_b)

	# Green
	n_g = bradb.LAYER({"TYPE":"NG", "_UPPER":100, "_LOWER":67})
	n_g.AddCellType(ecell,1)
	col.AddLayerType(n_g)
	
	# Triangle
	n_t = bradb.LAYER({"TYPE":"NT", "_UPPER":100, "_LOWER":67})
	n_t.AddCellType(ecell,1)
	col.AddLayerType(n_t)
	
	# Square
	n_s = bradb.LAYER({"TYPE":"NS", "_UPPER":100, "_LOWER":67})
	n_s.AddCellType(ecell,1)
	col.AddLayerType(n_s)
	
	# Inhibitor
	n_i = bradb.LAYER({"TYPE":"INHIBITOR", "_UPPER":100, "_LOWER":67})
	n_i.AddCellType(icell,1)
	col.AddLayerType(n_i)

	# Internal connections (this is not really necessary since we have only one neuron in each assembly)
	n_b.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'],speed=1)
	n_g.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'],speed=1)
	n_t.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'],speed=1)
	n_s.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'],speed=1)
	n_i.AddConnect((icell),(icell), isyns,prob=parameters['CONN_INTERNAL'],speed=1)

	# Excitatory connections: blue-triangle,green-triangle,blue-square,green-square,all-inhibit
	bradb.AddConnect((col,n_b,ecell),(col,n_t,ecell), esyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_t,ecell),(col,n_b,ecell), esyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_g,ecell),(col,n_t,ecell), esyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_t,ecell),(col,n_g,ecell), esyns, prob=parameters['CONN_LATERAL'],speed=1)

	bradb.AddConnect((col,n_b,ecell),(col,n_s,ecell),esyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_s,ecell),(col,n_b,ecell),esyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_g,ecell),(col,n_s,ecell),esyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_s,ecell),(col,n_g,ecell),esyns, prob=parameters['CONN_LATERAL'],speed=1)

	bradb.AddConnect((col,n_b,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_g,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_t,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_s,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'],speed=1)
	
	# Inhibitory connections: inhibit-all
	bradb.AddConnect((col,n_i,icell),(col,n_b,ecell), isyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_i,icell),(col,n_g,ecell), isyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_i,icell),(col,n_t,ecell), isyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_i,icell),(col,n_s,ecell), isyns, prob=parameters['CONN_LATERAL'],speed=1)

	bradb.AddSimpleReport("BReport", (col,n_b,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("GReport", (col,n_g,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("TReport", (col,n_t,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("SReport", (col,n_s,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("IReport", (col,n_i,icell), reptype="v", dur=d)

	s1=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
	s1.parms['AMP_START']='0.3'
	s1.parms['AMP_END']='0.3'
	s1.parms['TIME_START']='0.0'
	s1.parms['TIME_END']=endsim # !
	s1.parms['RATE']='20'
	s1.parms['TAU_NOISE']=parameters['TAU_NOISE']    # >0 = inhomogeneus  
	s1.parms['CORREL']=['0']           # >0 = correlated
	s1.parms['SEED']=['-11']

	s2=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
	s2.parms['AMP_START']='0.3'
	s2.parms['AMP_END']='0.3'
	s2.parms['TIME_START']='0.0'
	s2.parms['TIME_END']=endsim # !
	s2.parms['RATE']='30'
	s2.parms['TAU_NOISE']=parameters['TAU_NOISE']    # >0 = inhomogeneus  
	s2.parms['CORREL']=['0']           # >0 = correlated
	s2.parms['SEED']=['-11']

	s3=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
	s3.parms['AMP_START']='0.3'
	s3.parms['AMP_END']='0.3'
	s3.parms['TIME_START']='0.0'
	s3.parms['TIME_END']=endsim/2 # !
	s3.parms['RATE']='20'
	s3.parms['TAU_NOISE']=parameters['TAU_NOISE']    # >0 = inhomogeneus  
	s3.parms['CORREL']=['0']           # >0 = correlated
	s3.parms['SEED']=['-11']

	s4=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
	s4.parms['AMP_START']='0.3'
	s4.parms['AMP_END']='0.3'
	s4.parms['TIME_START']='0.0'
	s4.parms['TIME_END']=endsim/2 # !
	s4.parms['RATE']='30'
	s4.parms['TAU_NOISE']=parameters['TAU_NOISE']    # >0 = inhomogeneus  
	s4.parms['CORREL']=['0']           # >0 = correlated
	s4.parms['SEED']=['-11']

	stimb=bradb.STIMULUS_INJECT()
	stimb.parms['STIM_TYPE']=s1
	stimb.parms['TYPE']='simple_inject1a'
	stimb.parms['INJECT']=['COLXY NB E SOMA1_name 1']

	stimt=bradb.STIMULUS_INJECT()
	stimt.parms['STIM_TYPE']=s3
	stimt.parms['TYPE']='simple_inject1b'
	stimt.parms['INJECT']=['COLXY NT E SOMA1_name 1']
	
	stimg=bradb.STIMULUS_INJECT()
	stimg.parms['STIM_TYPE']=s2
	stimg.parms['TYPE']='simple_inject2a'
	stimg.parms['INJECT']=['COLXY NG E SOMA1_name 1']
	
	stims=bradb.STIMULUS_INJECT()
	stims.parms['STIM_TYPE']=s4
	stims.parms['TYPE']='simple_inject2b'
	stims.parms['INJECT']=['COLXY NS E SOMA1_name 1']

	# Teach: Blue Square
	bradb.AddStimInject(stimb)
	bradb.AddStimInject(stimt)
	
	# Teach: Green Triangle
	bradb.AddStimInject(stimg)
	bradb.AddStimInject(stims)

	brainlab.Run(bradb, verbose=True, nprocs=1)

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
