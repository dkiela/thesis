# -*- coding: utf-8 -*-
## Bradynor Simulation series 3 - experiment 1 - 24-02-2011
## Re-integration in a single Column - Non-monotomic computations
## Refs. Zirpe 2007, Vogels & Abbott 2005, Durstewitz et al. 2000, Mehring et al, 2003
## GOAL= investigate a new architecture which includes a third layer per column where all the information converges and is integrated.
## TEST= stable spiking patter in exc5 which is an integration of activity in exc2 and exc3
## Note= version of the model with 1 column and 2 inhibitory pools. 1 for exc2&3 and 1 for exc5
  

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
brainname="BradS3_1" 		# output files begin with this name
endsim=2			# seconds to simulate
FSV=10000 			# simulation timesteps per second
timesteps=FSV*endsim            # simulated brain time
d=(0.0, endsim)                 # duration for report


## CREATE BRAIN MODEL ##

bradb=brainlab.BRAIN(simsecs=endsim, jobname=brainname,fsv = FSV)


## LIBS##

bradb.SelectLib('standard')
lib=bradb.libs['standard']
syntypes=lib['syntypes']
comptypes=lib['comptypes']
celltypes=lib['celltypes']
chantypes=lib['chantypes']
synlearn=lib['sls']         #Hebb learning
synfadep=lib['sfds']        #Facilitation - Depression
synaug=lib['sas']           #Augmentation

print "CHECK1-Libraries"

## COMPARTMENTS ##

comp=comptypes['SOMA1']
comp.parms['TAU_MEMBRANE']=['0.020,0.0']       
comp.parms['R_MEMBRANE']=['200,0.0']          # Membrane capacitance = 1 
comp.parms['LEAK_CONDUCTANCE']=['0.00005,0.0']          
comp.parms['LEAK_REVERSAL']=['-60,0.0']          
comp.parms['THRESHOLD']=['-50,0.0']          
comp.parms['VMREST']=['-60,0.0']          

#print chantypes.keys()


print "CHECK2-Compartments"


## SYNAPSES ##

esyns=syntypes['E']
isyns=syntypes['I']
esyns.parms['ABSOLUTE_USE']=['0.250, 0.0']
isyns.parms['ABSOLUTE_USE']=['0.250,0.0']
esyns.parms['TYPE']='Excsyn'
isyns.parms['TYPE']='Inhsyn'
esyns.parms['MAX_CONDUCT']=['0.07'] 
isyns.parms['MAX_CONDUCT']=['0.45'] 
esyns.parms['SYN_REVERSAL']=['0,0']
isyns.parms['SYN_REVERSAL']=['-80,0']
esyns.parms['DELAY']=['0.0000000001,0.0000000001']  #Zirpe 2007
isyns.parms['DELAY']=['0.0000000001,0.0000000001']
esyns.parms['SFD']=['None']             #'Both'
isyns.parms['SFD']=['None']
esyns.parms['LEARN_LABEL']=synlearn['0Hebb']        #BHebb
isyns.parms['LEARN_LABEL']=synlearn['0Hebb']        #BHebb
esyns.parms['HEBB_START']=['0'] # 50 ms 
esyns.parms['HEBB_END']=['0']   #time in secs
isyns.parms['HEBB_START']=['0']
isyns.parms['HEBB_END']=['0']
#esyns.parms['SYN_AUGMENTATION']=synaug['SA.E1']   #synaptic augmentation
#isyns.parms['SYN_AUGMENTATION']=synaug['SA.E1']   #synaptic augmentation

print "CHECK3-Synapses"


## CELL,LAYERS & COLUMNS ##

ecell=celltypes['E']
icell=celltypes['I']

x, y, w, h=(100, 200, 50, 80)		# columns coordinates

exc1=bradb.LAYER({"TYPE":"E1", "_UPPER":100, "_LOWER":90})		# Excitatory layer - Input P(+)
exc1.AddCellType(ecell,14)				

exc2=bradb.LAYER({"TYPE":"E2", "_UPPER":90, "_LOWER":80})		# Excitatory layer - P(+)
exc2.AddCellType(ecell,1086)

exc3=bradb.LAYER({"TYPE":"E3", "_UPPER":80, "_LOWER":70})		# Excitatory layer - P(-)
exc3.AddCellType(ecell,1086)

exc4=bradb.LAYER({"TYPE":"E4", "_UPPER":70, "_LOWER":60})		# Excitatory layer - Input P(-)
exc4.AddCellType(ecell,14)

exc5=bradb.LAYER({"TYPE":"E5", "_UPPER":60, "_LOWER":50})		# Excitatory layer - P 
exc5.AddCellType(ecell,1000)

inh1=bradb.LAYER({"TYPE":"Inh1", "_UPPER":50, "_LOWER":40})		# Inhibitory layer - Inh P(+|-)
inh1.AddCellType(icell,550)

inh2=bradb.LAYER({"TYPE":"Inh2", "_UPPER":50, "_LOWER":40})		# Inhibitory layer - Inh P
inh2.AddCellType(icell,250)


P=bradb.COLUMN({"TYPE":"P","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})

 
bradb.AddColumn(P)

P.AddLayerType(exc1)
P.AddLayerType(exc2)
P.AddLayerType(exc3)
P.AddLayerType(exc4)
P.AddLayerType(exc5)                    
P.AddLayerType(inh1)
P.AddLayerType(inh2)


print "CHECK4-Cell,Layers & Columns"

### CONNECTIONS ###

## within-layer ##

exc1.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)         #self-recurrent E1
exc2.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)         #self-recurrent E2
exc3.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)         #self-recurrent E3
exc4.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)         #self-recurrent E4
exc5.AddConnect((ecell),(ecell), esyns,prob=0.02,speed=1)         #self-recurrent E5
inh1.AddConnect((icell),(icell), isyns,prob=0.02,speed=1)         #self-recurrent I1
inh2.AddConnect((icell),(icell), isyns,prob=0.02,speed=1)         #self-recurrent I2

## between-layers ##

#P(+|-) - exc to inh
bradb.AddConnect((P,exc1,ecell),(P,inh1,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc2,ecell),(P,inh1,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc3,ecell),(P,inh1,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc4,ecell),(P,inh1,icell),esyns, prob=0.02,speed=1)

#P(+|-) - exc(input) & exc(main)               
bradb.AddConnect((P,exc2,ecell),(P,exc1,ecell),esyns, prob=0.02,speed=1)    #Connect Input assembly P(+)
bradb.AddConnect((P,exc1,ecell),(P,exc2,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc4,ecell),(P,exc3,ecell),esyns, prob=0.02,speed=1)    #Connect Input assembly P(-)
bradb.AddConnect((P,exc3,ecell),(P,exc4,ecell),esyns, prob=0.02,speed=1)

#P(+|-) - inh1 to exc
bradb.AddConnect((P,inh1,icell),(P,exc1,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((P,inh1,icell),(P,exc2,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((P,inh1,icell),(P,exc3,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((P,inh1,icell),(P,exc4,ecell),isyns, prob=0.02,speed=1)

#P(+|-) & P
bradb.AddConnect((P,exc2,ecell),(P,exc5,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc3,ecell),(P,exc5,ecell),esyns, prob=0.02,speed=1)
#bradb.AddConnect((P,exc5,ecell),(P,exc2,ecell),esyns, prob=0.02,speed=1)
#bradb.AddConnect((P,exc5,ecell),(P,exc3,ecell),esyns, prob=0.02,speed=1)

#bradb.AddConnect((P,inh1,icell),(P,inh2,icell),isyns, prob=0.02,speed=1)
#bradb.AddConnect((P,inh2,icell),(P,inh1,icell),isyns, prob=0.02,speed=1)
                 

#P - exc & inh2
bradb.AddConnect((P,exc5,ecell),(P,inh2,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,inh2,icell),(P,exc5,ecell),isyns, prob=0.02,speed=1)

print "CHECK5-Connections"

### REPORTS ###

# tell NCS to report on some voltage values:

bradb.AddSimpleReport("P1Report", (P,exc1,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("P2Report", (P,exc2,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("P3Report", (P,exc3,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("P4Report", (P,exc4,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("P5Report", (P,exc5,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("I1Report", (P,inh1,icell), reptype="v", dur=d)
bradb.AddSimpleReport("I2Report", (P,inh2,icell), reptype="v", dur=d)

# tell NCS to report on some absolute USE (synaptic efficacy) values:

#bradb.AddSimpleReport("P1USE", (P,exc1,ecell), reptype="a", dur=d, synname=esyns)
#bradb.AddSimpleReport("P1USE2", (P1,l1,icell), reptype="a", dur=d, synname=inhs)

print "CHECK5-Reports"


### SIMULATION ###


## Injected Current (Input)

#stimulus definition

s=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'})  # stimulus class
s.parms['AMP_START']='0.3'
s.parms['AMP_END']='0.3'
s.parms['TIME_START']='0.01'        # 50 ms stim injection
s.parms['TIME_END']='0.06'
s.parms['RATE']='20'
s.parms['TAU_NOISE']=['0.020']    # >0 = inhomogeneus  
s.parms['CORREL']=['0']           # >0 = correlated
s.parms['SEED']=['-11']

#stimulus inject

si=bradb.STIMULUS_INJECT()
si.parms['STIM_TYPE']=s         # Stim 1 to P(+)
si.parms['TYPE']='simple_inject1'
si.parms['INJECT']=['P E1 E SOMA1_name 1']  # cell to apply input injection

si2=bradb.STIMULUS_INJECT()
si2.parms['STIM_TYPE']=s         # Stim 1 to P(-)
si2.parms['TYPE']='simple_inject2'
si2.parms['TIME_START']='0.03'        # 30 ms stim injection
si2.parms['TIME_END']='0.06'
si2.parms['INJECT']=['P E4 E SOMA1_name 1']  # cell to apply input injection

bradb.AddStimInject(si)
bradb.AddStimInject(si2)

print "CHECK6-Input"

print bradb

## start the simulation:

brainlab.Run(bradb, verbose=True, nprocs=1)

print "CHECK6-Run"


### PLOTS ###


#Voltage plots


brainlab.ReportPlot(brainname, "P2Report",cols=[1],plottitle="P(+) spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "P5Report",cols=[1],plottitle="P spikes", xlab="Timestep", ylab="mV", dosave=".png")


#Synaptic USE plots

#brainlab.ReportPlot(brainname, "P1USE",plottitle="P1(l1) syn excs", xlab="Timestep", ylab="mV", dosave=".png")
#brainlab.ReportPlot(brainname, "P1USE2",plottitle="P1(l2) syn inhs", xlab="Timestep", ylab="mV", dosave=".png") #TO FIX
#brainlab.ReportPlot(brainname, "P1USE3",plottitle="P1(l3) syn excs", xlab="Timestep", ylab="mV", dosave=".png")

#Spyke plots

#brainlab.ReportSpikePlot(brainname, "Brad_S1-E1Report.txt", usematplotlib=True, newfigure=True, xrange=None)
