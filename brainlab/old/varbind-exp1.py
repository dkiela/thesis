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
brainname="vb-exp1"
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
esyns.parms['HEBB_END']=['1']   #time in secs
isyns.parms['HEBB_START']=['0']
isyns.parms['HEBB_END']=['1']

### Construct the actual cell, layer and column setup
ecell=celltypes['E']
icell=celltypes['I']

x, y, w, h=(100, 200, 50, 80) # columns coordinates

# Terms and Predicates
# These represent our basic 'input building blocks'
terms=bradb.COLUMN({"TYPE":"TERMS","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
bradb.AddColumn(terms)

term_john = bradb.LAYER({"TYPE":"JOHN", "_UPPER":100, "_LOWER":67})
term_john.AddCellType(ecell,100)
terms.AddLayerType(term_john)

predicate_loves = bradb.LAYER({"TYPE":"LOVES", "_UPPER":66, "_LOWER":33})
predicate_loves.AddCellType(ecell,100)
terms.AddLayerType(predicate_loves)

term_mary = bradb.LAYER({"TYPE":"MARY", "_UPPER":32, "_LOWER":1})
term_mary.AddCellType(ecell,100)
terms.AddLayerType(term_mary)

# Positions
# For a binary predicate there are three positions: agent, action and object
positions=bradb.COLUMN({"TYPE":"POSITIONS","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
bradb.AddColumn(positions)

position_agent = bradb.LAYER({"TYPE":"AGENT", "_UPPER":100, "_LOWER":67})
position_agent.AddCellType(ecell,40)
positions.AddLayerType(position_agent)

position_action = bradb.LAYER({"TYPE":"ACTION", "_UPPER":66, "_LOWER":33})
position_action.AddCellType(ecell,40)
positions.AddLayerType(position_action)

position_object = bradb.LAYER({"TYPE":"OBJECT", "_UPPER":32, "_LOWER":1})
position_object.AddCellType(ecell,40)
positions.AddLayerType(position_object)

# Truth
# There are three truth values that we can represent: true, false and unknown
# True and false are mutually exclusive thanks to the inhibitory layer
truth=bradb.COLUMN({"TYPE":"TRUTH","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
bradb.AddColumn(truth)

formula_true = bradb.LAYER({"TYPE":"FORMULA_TRUE"})
formula_true.AddCellType(ecell,40)
truth.AddLayerType(formula_true)

truth_inhibit=bradb.LAYER({"TYPE":"Inhibit", "_UPPER":66, "_LOWER":33})
truth_inhibit.AddCellType(icell,40)
truth.AddLayerType(truth_inhibit)

formula_false = bradb.LAYER({"TYPE":"FORMULA_FALSE", "_UPPER":32, "_LOWER":1})
formula_false.AddCellType(ecell,40)
truth.AddLayerType(formula_false)

### Connections

# Self-recurrent connections
term_john.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
predicate_loves.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
term_mary.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
position_agent.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
position_action.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
position_object.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
formula_true.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
formula_false.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
truth_inhibit.AddConnect((icell),(icell), isyns,prob=0.02,speed=1)

# Connections between layers within a single column

# Terms column (should these be interconnected?)

# Positions column (should these be interconnected?)

# Truth column
# Connect inhibitor:
bradb.AddConnect((truth,formula_true,ecell),(truth,truth_inhibit,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((truth,formula_false,ecell),(truth,truth_inhibit,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((truth,truth_inhibit,icell),(truth,formula_true,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((truth,truth_inhibit,icell),(truth,formula_false,ecell),isyns, prob=0.02,speed=1)
# Connect to each other:
bradb.AddConnect((truth,formula_true,ecell),(truth,formula_false,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((truth,formula_false,ecell),(truth,formula_true,ecell),esyns, prob=0.02,speed=1)

# Connections between layers between columns

# Terms to Positions
# John and Mary are terms and can be in agent or object position, Loves can only be an action
bradb.AddConnect((terms,term_john,ecell),(positions,position_agent,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((terms,term_john,ecell),(positions,position_object,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((terms,term_mary,ecell),(positions,position_agent,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((terms,term_mary,ecell),(positions,position_object,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((terms,predicate_loves,ecell),(positions,position_action,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((terms,predicate_loves,ecell),(positions,position_action,ecell),esyns, prob=0.02,speed=1)

# Terms && Positions to Truth
# We do this for all cases, because we will teach the network later and then have it decide which case is true or false
bradb.AddConnect((terms,term_john,ecell),(truth,formula_true,ecell),esyns,prob=0.02,speed=1)
bradb.AddConnect((terms,term_john,ecell),(truth,formula_false,ecell),esyns,prob=0.02,speed=1)
bradb.AddConnect((terms,term_mary,ecell),(truth,formula_true,ecell),esyns,prob=0.02,speed=1)
bradb.AddConnect((terms,term_mary,ecell),(truth,formula_false,ecell),esyns,prob=0.02,speed=1)
bradb.AddConnect((terms,predicate_loves,ecell),(truth,formula_true,ecell),esyns,prob=0.02,speed=1)
bradb.AddConnect((terms,predicate_loves,ecell),(truth,formula_false,ecell),esyns,prob=0.02,speed=1)
bradb.AddConnect((positions,position_agent,ecell),(truth,formula_true,ecell),esyns,prob=0.02,speed=1)
bradb.AddConnect((positions,position_agent,ecell),(truth,formula_false,ecell),esyns,prob=0.02,speed=1)
bradb.AddConnect((positions,position_object,ecell),(truth,formula_true,ecell),esyns,prob=0.02,speed=1)
bradb.AddConnect((positions,position_object,ecell),(truth,formula_false,ecell),esyns,prob=0.02,speed=1)
bradb.AddConnect((positions,position_action,ecell),(truth,formula_true,ecell),esyns,prob=0.02,speed=1)
bradb.AddConnect((positions,position_action,ecell),(truth,formula_false,ecell),esyns,prob=0.02,speed=1)

## Reports
bradb.AddSimpleReport("JohnReport", (terms,term_john,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("MaryReport", (terms,term_mary,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("LovesReport", (terms,predicate_loves,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("AgentReport", (positions,position_agent,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("ObjectReport", (positions,position_object,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("ActionReport", (positions,position_action,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("TrueReport", (truth,formula_true,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("FalseReport", (truth,formula_false,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("InhibitReport", (truth,truth_inhibit,icell), reptype="v", dur=d)

bradb.AddSimpleReport("SynEffReportJohn", (terms,term_john,ecell), reptype="a", dur=d, synname=esyns)
bradb.AddSimpleReport("SynEffReportAgent", (positions,position_agent,ecell), reptype="a", dur=d, synname=esyns)
bradb.AddSimpleReport("SynEffReportTrue", (truth,formula_true,ecell), reptype="a", dur=d, synname=esyns)

## Stimulus
# What will we teach the network?
# - John loves Mary

# Initial stimulus
s1=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'}) 
s1.parms['AMP_START']='0.3'
s1.parms['AMP_END']='0.3'
s1.parms['TIME_START']='0.0'
s1.parms['TIME_END']='2'
s1.parms['RATE']='20'
s1.parms['TAU_NOISE']=['0.020']    # >0 = inhomogeneus  
s1.parms['CORREL']=['0']           # >0 = correlated
s1.parms['SEED']=['-11']

import copy

s2=copy.deepcopy(s1)
s2.parms['RATE']='30'
s3=copy.deepcopy(s1)
s3.parms['RATE']='30'
s4=copy.deepcopy(s1)
s4.parms['RATE']='50'
s4.parms['TIME_END']='0.5'

# s1: John = agent
# s2: Loves = action
# s3: Mary = object
# s4: True

john=bradb.STIMULUS_INJECT()
john.parms['STIM_TYPE']=s1
john.parms['TYPE']='simple_inject1'
john.parms['INJECT']=['TERMS JOHN E SOMA1_name 1']

agent=bradb.STIMULUS_INJECT()
agent.parms['STIM_TYPE']=s1
agent.parms['TYPE']='simple_inject2'
agent.parms['INJECT']=['POSITIONS AGENT E SOMA1_name 1']

formula_true=bradb.STIMULUS_INJECT()
formula_true.parms['STIM_TYPE']=s4
formula_true.parms['TYPE']='simple_inject3'
formula_true.parms['INJECT']=['TRUTH FORMULA_TRUE E SOMA1_name 1']

#loves=bradb.STIMULUS_INJECT()
#loves.parms['STIM_TYPE']=s1
#loves.parms['TYPE']='simple_inject1'
#loves.parms['INJECT']=['terms predicate_loves E SOMA1_name 1']

#mary=bradb.STIMULUS_INJECT()
#mary.parms['STIM_TYPE']=s1
#mary.parms['TYPE']='simple_inject1'
#mary.parms['INJECT']=['terms term_mary E SOMA1_name 1']

bradb.AddStimInject(john)
bradb.AddStimInject(agent)
bradb.AddStimInject(formula_true)
#bradb.AddStimInject(inhibit)
#bradb.AddStimInject(loves)
#bradb.AddStimInject(mary)

## First, verify that it looks alright
#bd = BrainlabDiagram(bradb)
#bd.show()

## Run the simulation
brainlab.Run(bradb, verbose=True, nprocs=1)

brainlab.ReportPlot(brainname, "JohnReport",cols=[1],plottitle="John spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "AgentReport",cols=[1],plottitle="Agent spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "TrueReport",cols=[1],plottitle="Formula true spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "FalseReport",cols=[1],plottitle="Formula false spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "SynEffReportJohn",cols=[1], plottitle="Synaptic Efficacy on John", xlab="Timestep", ylab="USE", linelab=["John"],dosave=".png")
brainlab.ReportPlot(brainname, "SynEffReportAgent",cols=[1], plottitle="Synaptic Efficacy on Agent", xlab="Timestep", ylab="USE", linelab=["[John] to Agent"],dosave=".png")
brainlab.ReportPlot(brainname, "SynEffReportTrue",cols=[1], plottitle="Synaptic Efficacy on True", xlab="Timestep", ylab="USE", linelab=["[John,Agent] to True"],dosave=".png")
