# -*- coding: utf-8 -*-
## Bradynor Simulation series 2 - experiment 3 - 24-02-2011
## Modus Ponens 
## Refs. Zirpe 2007, Vogels & Abbott 2005, Durstewitz
## GOAL: investigate how a 2-column system with usual structure would process inputs given at 2 different time points in 2 different columns.
## in other words, how does input integration take place in such a system.
## TEST: Final stable spiking state is a mixture of inputs.
## NOte: connections  between columns are only between excitatory assemblies
## Input protol: input to P(exc2), Input to Q(exc2) then inout to P(exc3)


## Modules

import brainlab
import pylab
import numpy
import netplot
import matplotlib
import brain
import scipy
import random

## Parameters

# simulation
brainname="Brad_S2_3" 		# output files begin with this name
endsim=2			# seconds to simulate
FSV=10000 			# simulation timesteps per second
timesteps=FSV*endsim


## CREATE BRAIN MODEL ##

bradb=brainlab.BRAIN(simsecs=endsim, jobname=brainname,fsv = FSV)


## LIBS##
print "CHECK1-Input"

bradb.SelectLib('standard')
lib=bradb.libs['standard']
syntypes=lib['syntypes']
comptypes=lib['comptypes']
celltypes=lib['celltypes']
chantypes=lib['chantypes']
synlearn=lib['sls']         #Hebb learning
synfadep=lib['sfds']        #Facilitation - Depression
synaug=lib['sas']           #Augmentation

## COMPARTMENTS ##

comp=comptypes['SOMA1']
comp.parms['TAU_MEMBRANE']=['0.020,0.0']       
comp.parms['R_MEMBRANE']=['200,0.0']          # Membrane capacitance = 1 
comp.parms['LEAK_CONDUCTANCE']=['0.00005,0.0']          
comp.parms['LEAK_REVERSAL']=['-60,0.0']          
comp.parms['THRESHOLD']=['-50,0.0']          
comp.parms['VMREST']=['-60,0.0']          

#print chantypes.keys()


print "CHECK2-Libs"

## CELLS ##


ecell=celltypes['E']
icell=celltypes['I']



## SYNAPSES ##

esyns=syntypes['E']
isyns=syntypes['I']
esyns.parms['ABSOLUTE_USE']=['0.250, 0.0']
isyns.parms['ABSOLUTE_USE']=['0.250,0.0']
esyns.parms['TYPE']='Excsyn'
isyns.parms['TYPE']='Inhsyn'
esyns.parms['MAX_CONDUCT']=['0.05']   #Silent
isyns.parms['MAX_CONDUCT']=['0.25']    #Silent
esyns.parms['SYN_REVERSAL']=['0,0']
isyns.parms['SYN_REVERSAL']=['-80,0']
esyns.parms['DELAY']=['0.0000000001,0.0000000001']  #Zirpe 2007
isyns.parms['DELAY']=['0.0000000001,0.0000000001']
esyns.parms['SFD']=['None']             #'Both'
isyns.parms['SFD']=['None']
esyns.parms['LEARN_LABEL']=synlearn['BHebb']
isyns.parms['LEARN_LABEL']=synlearn['BHebb']
esyns.parms['HEBB_START']=['0'] #time in secs
esyns.parms['HEBB_END']=['0']   #time in secs
isyns.parms['HEBB_START']=['0']
isyns.parms['HEBB_END']=['0']
#esyns.parms['SYN_AUGMENTATION']=synaug['SA.E1']   #synaptic augmentation
#isyns.parms['SYN_AUGMENTATION']=synaug['SA.E1']   #synaptic augmentation




print "CHECK3-Syns"

            


## CELL,COLUMNS & LAYERS ##



#33,7967,200
x, y, w, h=(100, 200, 50, 80)		# columns coordinates

exc1=bradb.LAYER({"TYPE":"E1", "_UPPER":100, "_LOWER":90})		# Excitatory layer
exc1.AddCellType(ecell,14)				

exc2=bradb.LAYER({"TYPE":"E2", "_UPPER":90, "_LOWER":60})		# Excitatory layer
exc2.AddCellType(ecell,1593)
#3186
#1593

exc3=bradb.LAYER({"TYPE":"E3", "_UPPER":60, "_LOWER":30})		# Excitatory layer
exc3.AddCellType(ecell,1593)

exc4=bradb.LAYER({"TYPE":"E4", "_UPPER":10, "_LOWER":0})		# Excitatory layer
exc4.AddCellType(ecell,14)

inh=bradb.LAYER({"TYPE":"Inh", "_UPPER":30, "_LOWER":10})		        # Inhibitory layer
inh.AddCellType(icell,400)
#800
#400

P=bradb.COLUMN({"TYPE":"P","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
Q=bradb.COLUMN({"TYPE":"Q","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})

 
bradb.AddColumn(P)
bradb.AddColumn(Q)

P.AddLayerType(exc1)
P.AddLayerType(exc2)
P.AddLayerType(exc3)
P.AddLayerType(exc4)
P.AddLayerType(inh)

Q.AddLayerType(exc1)
Q.AddLayerType(exc2)
Q.AddLayerType(exc3)
Q.AddLayerType(inh)


### CONNECTIONS ###

## within-layer ##

exc1.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)         #self-recurrent E1
exc2.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)         #self-recurrent E2
exc3.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
exc4.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)
inh.AddConnect((icell),(icell),isyns,prob=0.02,speed=1)            #self-recurrent I


print "CHECK3-Cells"

## between-layers ##

## P ##
bradb.AddConnect((P,exc1,ecell),(P,inh,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc2,ecell),(P,inh,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc3,ecell),(P,inh,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc4,ecell),(P,inh,icell),esyns, prob=0.02,speed=1)
                 
bradb.AddConnect((P,exc2,ecell),(P,exc1,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc1,ecell),(P,exc2,ecell),esyns, prob=0.02,speed=1)

bradb.AddConnect((P,exc4,ecell),(P,exc3,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc3,ecell),(P,exc4,ecell),esyns, prob=0.02,speed=1)


bradb.AddConnect((P,inh,icell),(P,exc1,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((P,inh,icell),(P,exc2,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((P,inh,icell),(P,exc3,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((P,inh,icell),(P,exc4,ecell),isyns, prob=0.02,speed=1)


## Q ##
bradb.AddConnect((Q,exc1,ecell),(Q,inh,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((Q,exc2,ecell),(Q,inh,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((Q,exc3,ecell),(Q,inh,icell),esyns, prob=0.02,speed=1)

bradb.AddConnect((Q,exc1,ecell),(Q,exc2,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((Q,exc2,ecell),(Q,exc1,ecell),esyns, prob=0.02,speed=1)

bradb.AddConnect((Q,inh,icell),(Q,exc1,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((Q,inh,icell),(Q,exc2,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((Q,inh,icell),(Q,exc3,ecell),isyns, prob=0.02,speed=1)

## between-columns ##

bradb.AddConnect((P,exc2,ecell),(Q,exc2,ecell),esyns, prob=0.01,speed=1)
bradb.AddConnect((P,exc2,ecell),(Q,exc3,ecell),esyns, prob=0.01,speed=1)
bradb.AddConnect((P,exc3,ecell),(Q,exc2,ecell),esyns, prob=0.01,speed=1)
bradb.AddConnect((P,exc3,ecell),(Q,exc3,ecell),esyns, prob=0.01,speed=1)

bradb.AddConnect((Q,exc2,ecell),(P,exc2,ecell),esyns, prob=0.01,speed=1)
bradb.AddConnect((Q,exc2,ecell),(P,exc3,ecell),esyns, prob=0.01,speed=1)
bradb.AddConnect((Q,exc3,ecell),(P,exc2,ecell),esyns, prob=0.01,speed=1)
bradb.AddConnect((Q,exc3,ecell),(P,exc3,ecell),esyns, prob=0.01,speed=1)



d=(0.0, endsim)

print "CHECK4-Cons"

### REPORTS ###

# tell NCS to report on some voltage values:

bradb.AddSimpleReport("P1Report", (P,exc1,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("P2Report", (P,exc2,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("P3Report", (P,exc3,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("P4Report", (P,exc4,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("IReport", (P,inh,icell), reptype="v", dur=d)

bradb.AddSimpleReport("Q2Report", (Q,exc2,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("Q3Report", (Q,exc3,ecell), reptype="v", dur=d)

# tell NCS to report on some absolute USE (synaptic efficacy) values:

#bradb.AddSimpleReport("P1USE", (P,exc1,ecell), reptype="a", dur=d, synname=esyns)
#bradb.AddSimpleReport("P1USE2", (P1,l1,icell), reptype="a", dur=d, synname=inhs)

print "CHECK5-Reps"


### SIMULATION ###


# SIMPLE INPUT

## Injected Current (Input)

#stimulus definition

s1=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'})  # stimulus class
s1.parms['AMP_START']='0.3'
s1.parms['AMP_END']='0.3'
s1.parms['TIME_START']='0.001'        # 50 ms stim injection
s1.parms['TIME_END']='0.051'
s1.parms['RATE']='20'
s1.parms['TAU_NOISE']=['0.020']    # >0 = inhomogeneus  
s1.parms['CORREL']=['0']           # >0 = correlated
s1.parms['SEED']=['-11']

s2=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'})  # stimulus class
s2.parms['AMP_START']='0.3'
s2.parms['AMP_END']='0.3'
s2.parms['TIME_START']='0.001'        # 50 ms stim injection
s2.parms['TIME_END']='0.051'
s2.parms['RATE']='20'
s2.parms['TAU_NOISE']=['0.020']    # >0 = inhomogeneus  
s2.parms['CORREL']=['0']           # >0 = correlated
s2.parms['SEED']=['-11']

s3=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'})  # stimulus class
s3.parms['AMP_START']='0.3'
s3.parms['AMP_END']='0.3'
s3.parms['TIME_START']='0.091'        # 50 ms stim injection
s3.parms['TIME_END']='0.141'
s3.parms['RATE']='20'
s3.parms['TAU_NOISE']=['0.020']    # >0 = inhomogeneus  
s3.parms['CORREL']=['0']           # >0 = correlated
s3.parms['SEED']=['-11']
#stimulus inject

si1=bradb.STIMULUS_INJECT()
si1.parms['STIM_TYPE']=s1         # Stim 1 to P(+)
si1.parms['TYPE']='simple_inject1'
si1.parms['INJECT']=['P E1 E SOMA1_name 1']  # cell to apply input injection

si2=bradb.STIMULUS_INJECT()
si2.parms['STIM_TYPE']=s2         # Stim 1 to P(-)
si2.parms['TYPE']='simple_inject2'
#si2.parms['TIME_START']='1.01'        # 50 ms stim injection
#si2.parms['TIME_END']='1.06'
si2.parms['INJECT']=['Q E1 E SOMA1_name 1']  # cell to apply input injection

si3=bradb.STIMULUS_INJECT()
si3.parms['STIM_TYPE']=s3         # Stim 1 to P(+)
si3.parms['TYPE']='simple_inject3'
si3.parms['INJECT']=['P E4 E SOMA1_name 1']  # cell to apply input injection

bradb.AddStimInject(si1)
bradb.AddStimInject(si2)
bradb.AddStimInject(si3)

print bradb

## start the simulation:

brainlab.Run(bradb, verbose=True, nprocs=1)

print "CHECK6-Run"


### PLOTS ###


#Voltage plots

#brainlab.ReportPlot(brainname, "E1Report",cols=[1],plottitle="E1e spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "P2Report",cols=[1],plottitle="P2e spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "P3Report",cols=[1],plottitle="P3e spikes", xlab="Timestep", ylab="mV", dosave=".png")
#brainlab.ReportPlot(brainname, "IReport",cols=[1], plottitle="I spikes",xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "Q2Report",cols=[1],plottitle="Q2e spikes", xlab="Timestep", ylab="mV", dosave=".png")


#Synaptic USE plots

#brainlab.ReportPlot(brainname, "P1USE",plottitle="P1(l1) syn excs", xlab="Timestep", ylab="mV", dosave=".png")
#brainlab.ReportPlot(brainname, "P1USE2",plottitle="P1(l2) syn inhs", xlab="Timestep", ylab="mV", dosave=".png") #TO FIX
#brainlab.ReportPlot(brainname, "P1USE3",plottitle="P1(l3) syn excs", xlab="Timestep", ylab="mV", dosave=".png")

#Spyke plots

#brainlab.ReportSpikePlot(brainname, "Brad_S1-E1Report.txt", usematplotlib=True, newfigure=True, xrange=None)
