# -*- coding: utf-8 -*-
## Bradynor Simulation series 2 - experiment 2 - 26-08-2010
## Bistable Neuronal Memory
## Refs. Zirpe 2007, Vogels & Abbott 2005, Durstewitz
## GOAL: test functioning of a single neuronal column as a bistable memory switch.
## TEST: stimulation of 50 msec in either E1 or E4 (input groups)
## will trigger a stable spiking activity (at least 1 sec) in either E2 or E3.
## Note: duration of stimulus inject has been increased (100msec) to compensate for the stronger inhibition.
## Also synaptic conductances have been readjusted to compensate for the higher spiking activity.


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
brainname="Brad_S2_2" 		# output files begin with this name
endsim=1			# seconds to simulate
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
#esyns.parms['MAX_CONDUCT']=['0.00001'] #silent
#isyns.parms['MAX_CONDUCT']=['0.0001'] #silent
#esyns.parms['MAX_CONDUCT']=['0.0067'] #very low freq
#isyns.parms['MAX_CONDUCT']=['0.06']  #very low freq
#esyns.parms['MAX_CONDUCT']=['0.01'] #low freq
#isyns.parms['MAX_CONDUCT']=['0.1']  #low freq
#esyns.parms['MAX_CONDUCT']=['0.042'] #low freq
#isyns.parms['MAX_CONDUCT']=['0.245']  #low freq
#esyns.parms['MAX_CONDUCT']=['0.067'] #STABLE High freq. SI
#isyns.parms['MAX_CONDUCT']=['0.60']  #STABLE High freq. SI
esyns.parms['MAX_CONDUCT']=['0.07']   #Silent
isyns.parms['MAX_CONDUCT']=['0.15']    #Silent

esyns.parms['SYN_REVERSAL']=['0,0']
isyns.parms['SYN_REVERSAL']=['-80,0']
esyns.parms['DELAY']=['0.0000000001,0.0000000001']  #Zirpe 2007
isyns.parms['DELAY']=['0.0000000001,0.0000000001']

#esyns.parms['SFD']=['Both']
#isyns.parms['SFD']=['Both']
#esyns.parms['SYN_AUGMENTATION']=synaug['SA.E1']   #synaptic augmentation
#isyns.parms['SYN_AUGMENTATION']=synaug['SA.E1']   #synaptic augmentation

esyns.parms['LEARN_LABEL']=synlearn['BHebb']
isyns.parms['LEARN_LABEL']=synlearn['BHebb']
esyns.parms['HEBB_START']=['0'] #time in secs
esyns.parms['HEBB_END']=['0']   #time in secs
isyns.parms['HEBB_START']=['0']
isyns.parms['HEBB_END']=['0']


print "CHECK3-Syns"

            


## CELL,COLUMNS & LAYERS ##



#33,7967,200
x, y, w, h=(100, 200, 50, 80)		# columns coordinates

exc1=bradb.LAYER({"TYPE":"E1", "_UPPER":100, "_LOWER":90})		# Excitatory layer
exc1.AddCellType(ecell,14)				

exc2=bradb.LAYER({"TYPE":"E2", "_UPPER":90, "_LOWER":60})		# Excitatory layer
exc2.AddCellType(ecell,1586)
#exc2.AddCellType(ecell,600)


#3186
#1593

exc3=bradb.LAYER({"TYPE":"E3", "_UPPER":60, "_LOWER":30})		# Excitatory layer
exc3.AddCellType(ecell,1586)
#exc3.AddCellType(ecell,600)


exc4=bradb.LAYER({"TYPE":"E4", "_UPPER":10, "_LOWER":0})		# Excitatory layer
exc4.AddCellType(ecell,14)

inh=bradb.LAYER({"TYPE":"Inh", "_UPPER":30, "_LOWER":10})		        # Inhibitory layer
inh.AddCellType(icell,400)
#800
#400

P=bradb.COLUMN({"TYPE":"Pre","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})

 
bradb.AddColumn(P)

P.AddLayerType(exc1)
P.AddLayerType(exc2)
P.AddLayerType(exc3)
P.AddLayerType(exc4)
P.AddLayerType(inh)




### CONNECTIONS ###

## within-layer ##

exc1.AddConnect((ecell),(ecell), esyns,prob=0.02)         #self-recurrent E1
exc2.AddConnect((ecell),(ecell), esyns,prob=0.02)         #self-recurrent E2
exc3.AddConnect((ecell),(ecell), esyns,prob=0.02)
exc4.AddConnect((ecell),(ecell), esyns,prob=0.02)
inh.AddConnect((icell),(icell),isyns,prob=0.02)            #self-recurrent I


print "CHECK3-Cells"

## between-layers ##


bradb.AddConnect((P,exc1,ecell),(P,inh,icell),esyns, prob=0.02,speed=0)
bradb.AddConnect((P,exc2,ecell),(P,inh,icell),esyns, prob=0.02,speed=0)
bradb.AddConnect((P,exc3,ecell),(P,inh,icell),esyns, prob=0.02,speed=0)
bradb.AddConnect((P,exc4,ecell),(P,inh,icell),esyns, prob=0.02,speed=0)
                 
bradb.AddConnect((P,exc2,ecell),(P,exc1,ecell),esyns, prob=0.02,speed=0)
bradb.AddConnect((P,exc1,ecell),(P,exc2,ecell),esyns, prob=0.02,speed=0)

bradb.AddConnect((P,exc4,ecell),(P,exc3,ecell),esyns, prob=0.02,speed=0)
bradb.AddConnect((P,exc3,ecell),(P,exc4,ecell),esyns, prob=0.02,speed=0)


# Mutual Support
#bradb.AddConnect((P,exc2,ecell),(P,exc3,ecell),esyns, prob=0.02,speed=0)
#bradb.AddConnect((P,exc3,ecell),(P,exc2,ecell),esyns, prob=0.02,speed=0

bradb.AddConnect((P,inh,icell),(P,exc1,ecell),isyns, prob=0.02,speed=0)
bradb.AddConnect((P,inh,icell),(P,exc2,ecell),isyns, prob=0.02,speed=0)
bradb.AddConnect((P,inh,icell),(P,exc3,ecell),isyns, prob=0.02,speed=0)
bradb.AddConnect((P,inh,icell),(P,exc4,ecell),isyns, prob=0.02,speed=0)

d=(0.0, endsim)

print "CHECK4-Cons"

### REPORTS ###

# tell NCS to report on some voltage values:

#bradb.AddSimpleReport("E1Report", (P,exc1,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("E2Report", (P,exc2,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("E3Report", (P,exc3,ecell), reptype="v", dur=d)
#bradb.AddSimpleReport("E4Report", (P,exc4,ecell), reptype="v", dur=d)
#bradb.AddSimpleReport("IReport", (P,inh,icell), reptype="v", dur=d)


# tell NCS to report on some absolute USE (synaptic efficacy) values:

#bradb.AddSimpleReport("P1USE", (P,exc1,ecell), reptype="a", dur=d, synname=esyns)
#bradb.AddSimpleReport("P1USE2", (P1,l1,icell), reptype="a", dur=d, synname=inhs)

print "CHECK5-Reps"

print bradb

### SIMULATION ###


# SIMPLE INPUT

#stimulus definition

s=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'})  # stimulus class
s.parms['AMP_START']='0.3'
s.parms['AMP_END']='0.3'
s.parms['TIME_START']='0.001'
s.parms['TIME_END']='0.101'
s.parms['RATE']='25'
s.parms['TAU_NOISE']=['0.020']    # >0 = inhomogeneus  
s.parms['CORREL']=['0']           # >0 = correlated
s.parms['SEED']=['-11']

#stimulus inject

si=bradb.STIMULUS_INJECT()
si.parms['STIM_TYPE']=s         # reference to the stim class
si.parms['TYPE']='simple_inject'
si.parms['INJECT']=['Pre E1 E SOMA1_name 1']  # cell to apply input injection

bradb.AddStimInject(si)


## start the simulation:

brainlab.Run(bradb, verbose=True, nprocs=1)

print "CHECK6-Run"


### PLOTS ###


#Voltage plots

#brainlab.ReportPlot(brainname, "E1Report",cols=[1],plottitle="E1e spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "E2Report",cols=[1,2,3],plottitle="E2e spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "E3Report",cols=[1,2,3],plottitle="E3e spikes", xlab="Timestep", ylab="mV", dosave=".png")
#brainlab.ReportPlot(brainname, "E4Report",cols=[1],plottitle="E3e spikes", xlab="Timestep", ylab="mV", dosave=".png")
#brainlab.ReportPlot(brainname, "IReport",cols=[1], plottitle="I spikes",xlab="Timestep", ylab="mV", dosave=".png")


#Synaptic USE plots

#brainlab.ReportPlot(brainname, "P1USE",plottitle="P1(l1) syn excs", xlab="Timestep", ylab="mV", dosave=".png")
#brainlab.ReportPlot(brainname, "P1USE2",plottitle="P1(l2) syn inhs", xlab="Timestep", ylab="mV", dosave=".png") #TO FIX
#brainlab.ReportPlot(brainname, "P1USE3",plottitle="P1(l3) syn excs", xlab="Timestep", ylab="mV", dosave=".png")

#Spyke plots

#brainlab.ReportSpikePlot(brainname, "Brad_S1-E1Report.txt", usematplotlib=True, newfigure=True, xrange=None)
