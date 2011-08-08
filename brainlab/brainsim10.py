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
	esyns.parms['HEBB_END']=['1']   #time in secs
	isyns.parms['HEBB_START']=['0']
	isyns.parms['HEBB_END']=['1']

	### Construct the actual cell, layer and column setup
	ecell=celltypes['E']
	icell=celltypes['I']

	x, y, w, h=(100, 200, 50, 80) # columns coordinates

	col=bradb.COLUMN({"TYPE":"COLXY","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
	bradb.AddColumn(col)

	# CONSTANTS
	n_1 = bradb.LAYER({"TYPE":"N1", "_UPPER":100, "_LOWER":67})
	n_1.AddCellType(ecell,1)
	col.AddLayerType(n_1)

	n_2 = bradb.LAYER({"TYPE":"N2", "_UPPER":100, "_LOWER":67})
	n_2.AddCellType(ecell,1)
	col.AddLayerType(n_2)

	n_3 = bradb.LAYER({"TYPE":"N3", "_UPPER":100, "_LOWER":67})
	n_3.AddCellType(ecell,1)
	col.AddLayerType(n_3)

	n_4 = bradb.LAYER({"TYPE":"N4", "_UPPER":100, "_LOWER":67})
	n_4.AddCellType(ecell,1)
	col.AddLayerType(n_4)
	
	# VARIABLES
	n_x = bradb.LAYER({"TYPE":"NX", "_UPPER":100, "_LOWER":67})
	n_x.AddCellType(ecell,1)
	col.AddLayerType(n_x)
	
	n_y = bradb.LAYER({"TYPE":"NY", "_UPPER":100, "_LOWER":67})
	n_y.AddCellType(ecell,1)
	col.AddLayerType(n_y)

	# POSITIONS
	# AgentP
	n_ap = bradb.LAYER({"TYPE":"NAP", "_UPPER":100, "_LOWER":67})
	n_ap.AddCellType(ecell,1)
	col.AddLayerType(n_ap)
	# ObjectP
	n_op = bradb.LAYER({"TYPE":"NOP", "_UPPER":100, "_LOWER":67})
	n_op.AddCellType(ecell,1)
	col.AddLayerType(n_op)

	# AgentQ
	n_aq = bradb.LAYER({"TYPE":"NAQ", "_UPPER":100, "_LOWER":67})
	n_aq.AddCellType(ecell,1)
	col.AddLayerType(n_aq)
	# ObjectP
	n_oq = bradb.LAYER({"TYPE":"NOQ", "_UPPER":100, "_LOWER":67})
	n_oq.AddCellType(ecell,1)
	col.AddLayerType(n_oq)

	# Inhibitor (2 cells)
	n_i = bradb.LAYER({"TYPE":"INHIBITOR", "_UPPER":100, "_LOWER":67})
	n_i.AddCellType(icell,2) #!!!!!!!!
	col.AddLayerType(n_i)

	# Internal connections (this is not really necessary since we have only one neuron in each assembly)
	n_1.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	n_2.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	n_x.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	n_y.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	n_ap.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	n_op.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	n_aq.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	n_oq.AddConnect((ecell),(ecell), esyns,prob=parameters['CONN_INTERNAL'])
	#n_i.AddConnect((icell),(icell), isyns,prob=parameters['CONN_INTERNAL'])#!!!!!!!!!

	# Excitatory connections: blue-triangle,green-triangle,blue-square,green-square,all-inhibit
	bradb.AddConnect((col,n_1,ecell),(col,n_x,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_x,ecell),(col,n_1,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_2,ecell),(col,n_x,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_x,ecell),(col,n_2,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_1,ecell),(col,n_y,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_y,ecell),(col,n_1,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_2,ecell),(col,n_y,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_y,ecell),(col,n_2,ecell), esyns, prob=parameters['CONN_LATERAL'])

	bradb.AddConnect((col,n_x,ecell),(col,n_ap,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_x,ecell),(col,n_op,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_x,ecell),(col,n_aq,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_x,ecell),(col,n_oq,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_ap,ecell),(col,n_x,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_op,ecell),(col,n_x,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_aq,ecell),(col,n_x,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_oq,ecell),(col,n_x,ecell), esyns, prob=parameters['CONN_LATERAL'])

	bradb.AddConnect((col,n_y,ecell),(col,n_ap,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_y,ecell),(col,n_op,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_y,ecell),(col,n_aq,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_y,ecell),(col,n_oq,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_ap,ecell),(col,n_y,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_op,ecell),(col,n_y,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_aq,ecell),(col,n_y,ecell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_oq,ecell),(col,n_y,ecell), esyns, prob=parameters['CONN_LATERAL'])

	# Connect to inhibit
	bradb.AddConnect((col,n_1,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_2,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_x,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_y,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_ap,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_op,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_aq,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_oq,ecell),(col,n_i,icell), esyns, prob=parameters['CONN_LATERAL'])

	# Inhibitory connections: inhibit-all
	bradb.AddConnect((col,n_i,icell),(col,n_1,ecell), isyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_i,icell),(col,n_2,ecell), isyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_i,icell),(col,n_x,ecell), isyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_i,icell),(col,n_y,ecell), isyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_i,icell),(col,n_ap,ecell), isyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_i,icell),(col,n_op,ecell), isyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_i,icell),(col,n_aq,ecell), isyns, prob=parameters['CONN_LATERAL'])
	bradb.AddConnect((col,n_i,icell),(col,n_oq,ecell), isyns, prob=parameters['CONN_LATERAL'])

	bradb.AddSimpleReport("JReport", (col,n_1,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("MReport", (col,n_2,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("XReport", (col,n_x,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("YReport", (col,n_y,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("APReport", (col,n_ap,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("OPReport", (col,n_op,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("AQReport", (col,n_aq,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("OQReport", (col,n_oq,ecell), reptype="v", dur=d)
	bradb.AddSimpleReport("IReport", (col,n_i,icell), reptype="v", dur=d)

#	bradb.AddSimpleReport("BUseReport", (col,n_b,ecell), synname=esyns, reptype="a", dur=d)
#	bradb.AddSimpleReport("GUseReport", (col,n_g,ecell), synname=esyns, reptype="a", dur=d)
#	bradb.AddSimpleReport("TUseReport", (col,n_t,ecell), synname=esyns, reptype="a", dur=d)
#	bradb.AddSimpleReport("SUseReport", (col,n_s,ecell), synname=esyns, reptype="a", dur=d)

	s1=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
	s1.parms['AMP_START']='0.3'
	s1.parms['AMP_END']='0.3'
	s1.parms['TIME_START']='0.0'
	s1.parms['TIME_END']=str(endsim) # !
	s1.parms['RATE']=str(parameters['RATE1'])
	s1.parms['TAU_NOISE']=parameters['TAU_NOISE']    # >0 = inhomogeneus  
	s1.parms['CORREL']=['0']           # >0 = correlated
	s1.parms['SEED']=['-11']

	s2=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
	s2.parms['AMP_START']='0.3'
	s2.parms['AMP_END']='0.3'
	s2.parms['TIME_START']='0.0'
	s2.parms['TIME_END']=str(endsim) # !
	s2.parms['RATE']=str(parameters['RATE2'])
	s2.parms['TAU_NOISE']=parameters['TAU_NOISE']    # >0 = inhomogeneus  
	s2.parms['CORREL']=['0']           # >0 = correlated
	s2.parms['SEED']=['-11']

	s3=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
	s3.parms['AMP_START']='0.3'
	s3.parms['AMP_END']='0.3'
	s3.parms['TIME_START']='0.0'
	s3.parms['TIME_END']='1.0' # !
	s3.parms['RATE']=str(parameters['RATE1'])
	s3.parms['TAU_NOISE']=parameters['TAU_NOISE']    # >0 = inhomogeneus  
	s3.parms['CORREL']=['0']           # >0 = correlated
	s3.parms['SEED']=['-11']

	s4=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
	s4.parms['AMP_START']='0.3'
	s4.parms['AMP_END']='0.3'
	s4.parms['TIME_START']='0.0'
	s4.parms['TIME_END']='1.0' # !
	s4.parms['RATE']=str(parameters['RATE2'])
	s4.parms['TAU_NOISE']=parameters['TAU_NOISE']    # >0 = inhomogeneus  
	s4.parms['CORREL']=['0']           # >0 = correlated
	s4.parms['SEED']=['-11']

	#si=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
	#si.parms['AMP_START']='0.3'
	#si.parms['AMP_END']='0.3'
	#si.parms['TIME_START']='0.0'
	#si.parms['TIME_END']='2.0' # !
	#si.parms['RATE']='33'
	#si.parms['TAU_NOISE']=parameters['TAU_NOISE']    # >0 = inhomogeneus  
	#si.parms['CORREL']=['0']           # >0 = correlated
	#si.parms['SEED']=['-11']

	# John
	stimj=bradb.STIMULUS_INJECT()
	stimj.parms['STIM_TYPE']=s3
	stimj.parms['TYPE']='simple_inject_john'
	stimj.parms['INJECT']=['COLXY NJ E SOMA1_name 1']
	# Mary
	stimm=bradb.STIMULUS_INJECT()
	stimm.parms['STIM_TYPE']=s4
	stimm.parms['TYPE']='simple_inject_mary'
	stimm.parms['INJECT']=['COLXY NM E SOMA1_name 1']

	# X
	stimx=bradb.STIMULUS_INJECT()
	stimx.parms['STIM_TYPE']=s1
	stimx.parms['TYPE']='simple_inject1_x'
	stimx.parms['INJECT']=['COLXY NX E SOMA1_name 1']
	# AgentP 2
	stimap2=bradb.STIMULUS_INJECT()
	stimap2.parms['STIM_TYPE']=s1
	stimap2.parms['TYPE']='simple_inject1_ap2'
	stimap2.parms['INJECT']=['COLXY NAP E SOMA1_name 1']
	# ObjectQ
	stimoq=bradb.STIMULUS_INJECT()
	stimoq.parms['STIM_TYPE']=s3
	stimoq.parms['TYPE']='simple_inject1_oq'
	stimoq.parms['INJECT']=['COLXY NOQ E SOMA1_name 1']

	# Y
	stimy=bradb.STIMULUS_INJECT()
	stimy.parms['STIM_TYPE']=s2
	stimy.parms['TYPE']='simple_inject1_y'
	stimy.parms['INJECT']=['COLXY NY E SOMA1_name 1']
	# Agent Q
	stimaq=bradb.STIMULUS_INJECT()
	stimaq.parms['STIM_TYPE']=s4
	stimaq.parms['TYPE']='simple_inject1_aq'
	stimaq.parms['INJECT']=['COLXY NAQ E SOMA1_name 1']
	# ObjectP 2
	stimop2=bradb.STIMULUS_INJECT()
	stimop2.parms['STIM_TYPE']=s2
	stimop2.parms['TYPE']='simple_inject1_op2'
	stimop2.parms['INJECT']=['COLXY NOP E SOMA1_name 1']

	# Inhibition
	#stimi=bradb.STIMULUS_INJECT()
	#stimi.parms['STIM_TYPE']=si
	#stimi.parms['TYPE']='simple_inject_inh1'
	#stimi.parms['INJECT']=['COLXY INHIBITOR I SOMA1_name 1']

	# Teach: Green Square & Blue Triangle
	#bradb.AddStimInject(stimi)

	bradb.AddStimInject(stimoq)
	bradb.AddStimInject(stimop2)
	bradb.AddStimInject(stimj)
	bradb.AddStimInject(stimm)
	bradb.AddStimInject(stimx)
	bradb.AddStimInject(stimy)
	bradb.AddStimInject(stimaq)
	bradb.AddStimInject(stimap2)

	brainlab.Run(bradb, verbose=True, nprocs=1)

def loadBrain(fn,folder=''):
	#f=open(fn)
	#l=len(f.readline().split())
	#f.close()
	f=open(folder+fn)
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
