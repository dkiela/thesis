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
	esyns.parms['HEBB_START']=['0'] # 50 ms 
	esyns.parms['HEBB_END']=['0']   #time in secs
	isyns.parms['HEBB_START']=['0']
	isyns.parms['HEBB_END']=['0']

	### Construct the actual cell, layer and column setup
	ecell=celltypes['E']
	icell=celltypes['I']

	x, y, w, h=(100, 200, 50, 80) # columns coordinates

	col=bradb.COLUMN({"TYPE":"COLXY","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
	bradb.AddColumn(col)

	n_x = bradb.LAYER({"TYPE":"NX", "_UPPER":100, "_LOWER":67})
	n_x.AddCellType(ecell,1)
	col.AddLayerType(n_x)
	n_y = bradb.LAYER({"TYPE":"NY", "_UPPER":100, "_LOWER":67})
	n_y.AddCellType(ecell,1)
	col.AddLayerType(n_y)

	n_x.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'],speed=1)
	n_y.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'],speed=1)

	bradb.AddConnect((col,n_x,ecell),(col,n_y,ecell), esyns, prob=parameters['CONN_LATERAL'],speed=1)
	bradb.AddConnect((col,n_y,ecell),(col,n_x,ecell),esyns, prob=parameters['CONN_LATERAL'],speed=1)

	bradb.AddSimpleReport("XReport", (col,n_x,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("YReport", (col,n_y,ecell), reptype="v", dur=d)

	s1=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
	s1.parms['AMP_START']='0.3'
	s1.parms['AMP_END']='0.3'
	s1.parms['TIME_START']='0.0'
	s1.parms['TIME_END']=endsim # !
	s1.parms['RATE']='20'
	s1.parms['TAU_NOISE']=parameters['TAU_NOISE']    # >0 = inhomogeneus  
	s1.parms['CORREL']=['0']           # >0 = correlated
	s1.parms['SEED']=['-11']

	stimx=bradb.STIMULUS_INJECT()
	stimx.parms['STIM_TYPE']=s1
	stimx.parms['TYPE']='simple_inject1'
	stimx.parms['INJECT']=['COLXY NX E SOMA1_name 1']

	stimy=bradb.STIMULUS_INJECT()
	stimy.parms['STIM_TYPE']=s1
	stimy.parms['TYPE']='simple_inject2'
	stimy.parms['INJECT']=['COLXY NY E SOMA1_name 1']

	bradb.AddStimInject(stimx)
#	bradb.AddStimInject(stimy)

	brainlab.Run(bradb, verbose=True, nprocs=1)

def loadBrain(fn):
    f=open(fn)
    l=len(f.readline().split())
    f.close()
    f=open(fn)
    dd=[]
    for i in f.readlines():
        d=i.strip().split()
        d.pop(0)
        n=numpy.array(map(float, d))
        dapp=numpy.average(n)
        #dapp=d.pop(0) #for now,just take the one remaining value, because n_neurons=1
        dd.append(dapp)
    f.close()
    return dd
