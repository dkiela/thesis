# 
# Filename:	varbind-exp1.py
# Author:	Douwe Kiela
# Date:		20-3-2011
# Description:	This is the initial test setup.

# Import relevant modules
#from braindiagram import *

import brainlab
import pylab
import numpy
import netplot
import matplotlib
import brain
#import scipy
import random

# General settings
brainname="vb-sync"
endsim=2		# number of seconds the simulation runs (2)
FSV=10000 		# simulation timesteps per second
timesteps=FSV*endsim	# simulated brain time
d=(0.0, endsim)		# duration for reports

# Construct the BRAIN
bradb=brainlab.BRAIN(simsecs=endsim, jobname=brainname, fsv = FSV)

# Libraries
bradb.SelectLib('standard')
lib=bradb.libs['standard']
syntypes=lib['syntypes']
comptypes=lib['comptypes']
celltypes=lib['celltypes']
chantypes=lib['chantypes']
synlearn=lib['sls']         #Hebb learning
synfadep=lib['sfds']        #Facilitation - Depression
synaug=lib['sas']           #Augmentation

# Compartments
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
esyns.parms['ABSOLUTE_USE']=['0.250, 0.0']
isyns.parms['ABSOLUTE_USE']=['0.250,0.0']
esyns.parms['TYPE']='Excsyn'
isyns.parms['TYPE']='Inhsyn'
esyns.parms['MAX_CONDUCT']=['0.05']    #0.06
isyns.parms['MAX_CONDUCT']=['0.4']      #0.35
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

constants=bradb.COLUMN({"TYPE":"CONSTANTS","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
bradb.AddColumn(constants)

c_john = bradb.LAYER({"TYPE":"JOHN", "_UPPER":100, "_LOWER":67})
c_john.AddCellType(ecell,100)
constants.AddLayerType(c_john)
c_mary = bradb.LAYER({"TYPE":"MARY", "_UPPER":100, "_LOWER":67})
c_mary.AddCellType(ecell,100)
constants.AddLayerType(c_mary)
c_bob = bradb.LAYER({"TYPE":"BOB", "_UPPER":100, "_LOWER":67})
c_bob.AddCellType(ecell,100)
constants.AddLayerType(c_bob)

variables=bradb.COLUMN({"TYPE":"VARIABLES","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
bradb.AddColumn(variables)

v_x = bradb.LAYER({"TYPE":"VAR_X", "_UPPER":100, "_LOWER":67})
v_x.AddCellType(ecell,100)
variables.AddLayerType(v_x)
v_y = bradb.LAYER({"TYPE":"VAR_Y", "_UPPER":100, "_LOWER":67})
v_y.AddCellType(ecell,100)
variables.AddLayerType(v_y)

truth=bradb.COLUMN({"TYPE":"TRUTH","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
bradb.AddColumn(truth)
t_true = bradb.LAYER({"TYPE":"T_TRUE", "_UPPER":100, "_LOWER":67})
t_true.AddCellType(ecell,100)
truth.AddLayerType(t_true)

c_john.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
c_mary.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
c_bob.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
v_x.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
v_y.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
t_true.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)

bradb.AddConnect((constants,c_john,ecell),(variables,v_x,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((constants,c_bob,ecell),(variables,v_y,ecell),esyns, prob=0.02,speed=1)

bradb.AddConnect((variables,v_x,ecell),(truth,t_true,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((variables,v_y,ecell),(truth,t_true,ecell),esyns, prob=0.02,speed=1)

bradb.AddSimpleReport("JohnReport", (constants,c_john,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("BobReport", (constants,c_bob,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("XReport", (variables,v_x,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("YReport", (variables,v_y,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("TrueReport", (truth,t_true,ecell), reptype="v", dur=d)

s1=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
s1.parms['AMP_START']='0.3'
s1.parms['AMP_END']='0.3'
s1.parms['TIME_START']='0.0'
s1.parms['TIME_END']='2'
s1.parms['RATE']='20'
s1.parms['TAU_NOISE']=['0.020']    # >0 = inhomogeneus  
s1.parms['CORREL']=['0']           # >0 = correlated
s1.parms['SEED']=['-11']

s2=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
s2.parms['AMP_START']='0.3'
s2.parms['AMP_END']='0.3'
s2.parms['TIME_START']='0.0'
s2.parms['TIME_END']='2'
s2.parms['RATE']='30'
s2.parms['TAU_NOISE']=['0.020']    # >0 = inhomogeneus  
s2.parms['CORREL']=['0']           # >0 = correlated
s2.parms['SEED']=['-11']

stim_john=bradb.STIMULUS_INJECT()
stim_john.parms['STIM_TYPE']=s1
stim_john.parms['TYPE']='simple_inject1'
stim_john.parms['INJECT']=['CONSTANTS JOHN E SOMA1_name 1']

stim_x=bradb.STIMULUS_INJECT()
stim_x.parms['STIM_TYPE']=s1
stim_x.parms['TYPE']='simple_inject2'
stim_x.parms['INJECT']=['VARIABLES VAR_X E SOMA1_name 1']

stim_bob=bradb.STIMULUS_INJECT()
stim_bob.parms['STIM_TYPE']=s2
stim_bob.parms['TYPE']='simple_inject3'
stim_bob.parms['INJECT']=['CONSTANTS BOB E SOMA1_name 1']

stim_y=bradb.STIMULUS_INJECT()
stim_y.parms['STIM_TYPE']=s2
stim_y.parms['TYPE']='simple_inject4'
stim_y.parms['INJECT']=['VARIABLES VAR_Y E SOMA1_name 1']

bradb.AddStimInject(stim_john)
bradb.AddStimInject(stim_x)
bradb.AddStimInject(stim_bob)
bradb.AddStimInject(stim_y)

brainlab.Run(bradb, verbose=True, nprocs=1)

brainlab.ReportPlot(brainname, "JohnReport",cols=[1],plottitle="John spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "BobReport",cols=[1],plottitle="Bob spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "XReport",cols=[1],plottitle="X spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "YReport",cols=[1],plottitle="Y spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "TrueReport",cols=[1],plottitle="True spikes", xlab="Timestep", ylab="mV", dosave=".png")
