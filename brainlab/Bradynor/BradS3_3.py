# -*- coding: utf-8 -*-
## Bradynor Simulation series 3 - experiment 3 - 8-10-2010
## Re-integration in a two Column system - Non-monotomic computations for Modus Ponens
## Refs. Zirpe 2007, Vogels & Abbott 2005, Durstewitz et al. 2000, Mehring et al, 2003
## GOAL= investigate a new architecture which includes a third layer per column where all the information converges and is integrated.
## TEST= stable spiking patter in exc5 which is an integration of activity in exc2 and exc3
## Note= version of the model with 2 columns and 3 inhibitory pools per column. 1 for exc2, 1for exc3 and 1 for exc5

   

## Modules

import brainlab
import pylab
import numpy
import netplot
import matplotlib
import brain
#import scipy
import random

## Parameters

# simulation
brainname="BradS3-3" 		# output files begin with this name NB: Must be different froms script name or it will delete it!!!
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
esyns.parms['MAX_CONDUCT']=['0.05']    #0.06
isyns.parms['MAX_CONDUCT']=['0.4']      #0.35
esyns.parms['SYN_REVERSAL']=['0,0']
isyns.parms['SYN_REVERSAL']=['-80,0']
esyns.parms['DELAY']=['0.0000000001,0.0000000001']  #Zirpe 2007
isyns.parms['DELAY']=['0.0000000001,0.0000000001']
esyns.parms['SFD']=['None']             #'Both' / 'None'
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

inh1=bradb.LAYER({"TYPE":"Inh1", "_UPPER":50, "_LOWER":40})		# Inhibitory layer - Inh P(+)
inh1.AddCellType(icell,275)

inh2=bradb.LAYER({"TYPE":"Inh2", "_UPPER":40, "_LOWER":30})		# Inhibitory layer - Inh P(-)
inh2.AddCellType(icell,275)

inh3=bradb.LAYER({"TYPE":"Inh3", "_UPPER":30, "_LOWER":20})		# Inhibitory layer - Inh P
inh3.AddCellType(icell,250)

P=bradb.COLUMN({"TYPE":"P","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
Q=bradb.COLUMN({"TYPE":"Q","_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
 
bradb.AddColumn(P)
bradb.AddColumn(Q)

P.AddLayerType(exc1)
P.AddLayerType(exc2)
P.AddLayerType(exc3)
P.AddLayerType(exc4)
P.AddLayerType(exc5)                    
P.AddLayerType(inh1)
P.AddLayerType(inh2)
P.AddLayerType(inh3)

Q.AddLayerType(exc1)
Q.AddLayerType(exc2)
Q.AddLayerType(exc3)
Q.AddLayerType(exc4)
Q.AddLayerType(exc5)                    
Q.AddLayerType(inh1)
Q.AddLayerType(inh2)
Q.AddLayerType(inh3)
               
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
inh3.AddConnect((icell),(icell), isyns,prob=0.02,speed=1)         #self-recurrent I2

## between-layers ##

##P

#P(+|-) - exc to inh
bradb.AddConnect((P,exc1,ecell),(P,inh1,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc2,ecell),(P,inh1,icell),esyns, prob=0.02,speed=1)

bradb.AddConnect((P,exc3,ecell),(P,inh2,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc4,ecell),(P,inh2,icell),esyns, prob=0.02,speed=1)

#P(+|-) - exc(input) & exc(main)               
bradb.AddConnect((P,exc2,ecell),(P,exc1,ecell),esyns, prob=0.02,speed=1)    #Connect Input assembly P(+)
bradb.AddConnect((P,exc1,ecell),(P,exc2,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc4,ecell),(P,exc3,ecell),esyns, prob=0.02,speed=1)    #Connect Input assembly P(-)
bradb.AddConnect((P,exc3,ecell),(P,exc4,ecell),esyns, prob=0.02,speed=1)

#P(+|-) - inh1 to exc
bradb.AddConnect((P,inh1,icell),(P,exc3,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((P,inh1,icell),(P,exc4,ecell),isyns, prob=0.02,speed=1)

bradb.AddConnect((P,inh2,icell),(P,exc1,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((P,inh2,icell),(P,exc2,ecell),isyns, prob=0.02,speed=1)

#P(+|-) & P
bradb.AddConnect((P,exc2,ecell),(P,exc5,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,exc3,ecell),(P,exc5,ecell),esyns, prob=0.02,speed=1)

#bradb.AddConnect((P,exc5,ecell),(P,exc2,ecell),esyns, prob=0.02,speed=1)
#bradb.AddConnect((P,exc5,ecell),(P,exc3,ecell),esyns, prob=0.02,speed=1)

#bradb.AddConnect((P,inh1,icell),(P,inh2,icell),isyns, prob=0.02,speed=1)
#bradb.AddConnect((P,inh2,icell),(P,inh1,icell),isyns, prob=0.02,speed=1)
                 

#P - exc & inh2
bradb.AddConnect((P,exc5,ecell),(P,inh3,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((P,inh3,icell),(P,exc5,ecell),isyns, prob=0.02,speed=1)

##Q

#Q(+|-) - exc to inh
bradb.AddConnect((Q,exc1,ecell),(Q,inh1,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((Q,exc2,ecell),(Q,inh1,icell),esyns, prob=0.02,speed=1)

bradb.AddConnect((Q,exc3,ecell),(Q,inh2,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((Q,exc4,ecell),(Q,inh2,icell),esyns, prob=0.02,speed=1)

#Q(+|-) - exc(input) & exc(main)               
bradb.AddConnect((Q,exc2,ecell),(Q,exc1,ecell),esyns, prob=0.02,speed=1)    #Connect Input assembly P(+)
bradb.AddConnect((Q,exc1,ecell),(Q,exc2,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((Q,exc4,ecell),(Q,exc3,ecell),esyns, prob=0.02,speed=1)    #Connect Input assembly P(-)
bradb.AddConnect((Q,exc3,ecell),(Q,exc4,ecell),esyns, prob=0.02,speed=1)

#Q(+|-) - inh1 to exc
bradb.AddConnect((Q,inh1,icell),(Q,exc3,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((Q,inh1,icell),(Q,exc4,ecell),isyns, prob=0.02,speed=1)

bradb.AddConnect((Q,inh2,icell),(Q,exc1,ecell),isyns, prob=0.02,speed=1)
bradb.AddConnect((Q,inh2,icell),(Q,exc2,ecell),isyns, prob=0.02,speed=1)

#Q(+|-) & Q
bradb.AddConnect((Q,exc2,ecell),(Q,exc5,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((Q,exc3,ecell),(Q,exc5,ecell),esyns, prob=0.02,speed=1)

#bradb.AddConnect((P,exc5,ecell),(P,exc2,ecell),esyns, prob=0.02,speed=1)
#bradb.AddConnect((P,exc5,ecell),(P,exc3,ecell),esyns, prob=0.02,speed=1)

#bradb.AddConnect((P,inh1,icell),(P,inh2,icell),isyns, prob=0.02,speed=1)
#bradb.AddConnect((P,inh2,icell),(P,inh1,icell),isyns, prob=0.02,speed=1)
                 

#Q - exc & inh2
bradb.AddConnect((Q,exc5,ecell),(Q,inh3,icell),esyns, prob=0.02,speed=1)
bradb.AddConnect((Q,inh3,icell),(Q,exc5,ecell),isyns, prob=0.02,speed=1)



##P&Q

bradb.AddConnect((P,exc5,ecell),(Q,exc5,ecell),esyns, prob=0.02,speed=1)
bradb.AddConnect((Q,exc5,ecell),(P,exc5,ecell),esyns, prob=0.02,speed=1)

bradb.AddConnect((P,inh3,icell),(Q,inh3,icell),isyns, prob=0.02,speed=1)
bradb.AddConnect((Q,inh3,icell),(P,inh3,icell),isyns, prob=0.02,speed=1)

print "CHECK5-Connections"

### REPORTS ###

# tell NCS to report on some voltage values:

##P
bradb.AddSimpleReport("P1Report", (P,exc1,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("P2Report", (P,exc2,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("P3Report", (P,exc3,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("P4Report", (P,exc4,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("P5Report", (P,exc5,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("PI1Report", (P,inh1,icell), reptype="v", dur=d)
bradb.AddSimpleReport("PI2Report", (P,inh2,icell), reptype="v", dur=d)
bradb.AddSimpleReport("PI3Report", (P,inh3,icell), reptype="v", dur=d)

##Q
bradb.AddSimpleReport("Q1Report", (Q,exc1,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("Q2Report", (Q,exc2,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("Q3Report", (Q,exc3,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("Q4Report", (Q,exc4,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("Q5Report", (Q,exc5,ecell), reptype="v", dur=d)
bradb.AddSimpleReport("QI1Report", (Q,inh1,icell), reptype="v", dur=d)
bradb.AddSimpleReport("QI2Report", (Q,inh2,icell), reptype="v", dur=d)
bradb.AddSimpleReport("QI3Report", (Q,inh3,icell), reptype="v", dur=d)

# tell NCS to report on some absolute USE (synaptic efficacy) values:

#bradb.AddSimpleReport("P1USE", (P,exc1,ecell), reptype="a", dur=d, synname=esyns)
#bradb.AddSimpleReport("P1USE2", (P1,l1,icell), reptype="a", dur=d, synname=inhs)

print "CHECK5-Reports"


### SIMULATION ###


## Injected Current (Input)

#stimulus definition

s1=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'})  # stimulus class 1
s1.parms['AMP_START']='0.3'
s1.parms['AMP_END']='0.3'
s1.parms['TIME_START']='0.01'        # 50 ms stim injection
s1.parms['TIME_END']='0.06'
s1.parms['RATE']='20'
s1.parms['TAU_NOISE']=['0.020']    # >0 = inhomogeneus  
s1.parms['CORREL']=['0']           # >0 = correlated
s1.parms['SEED']=['-11']

s2=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'})  # stimulus class 2
s2.parms['AMP_START']='0.3'
s2.parms['AMP_END']='0.3'
s2.parms['TIME_START']='0.01'        # 50 ms stim injection
s2.parms['TIME_END']='0.06'
s2.parms['RATE']='20'
s2.parms['TAU_NOISE']=['0.020']    # >0 = inhomogeneus  
s2.parms['CORREL']=['0']           # >0 = correlated
s2.parms['SEED']=['-11']

s3=bradb.STIMULUS(parms={'MODE': 'VOLTAGE', 'PATTERN':'NOISE'})  # stimulus class 2
s3.parms['AMP_START']='0.3'
s3.parms['AMP_END']='0.3'
s3.parms['TIME_START']='1.01'        # 50 ms stim injection
s3.parms['TIME_END']='1.06'
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
si2.parms['STIM_TYPE']=s2         # Stim 1 to Q(+)
si2.parms['TYPE']='simple_inject2'
si2.parms['INJECT']=['Q E1 E SOMA1_name 1']  # cell to apply input injection

si3=bradb.STIMULUS_INJECT()
si3.parms['STIM_TYPE']=s3         # Stim 1 to P(-)
si3.parms['TYPE']='simple_inject3'
si3.parms['INJECT']=['P E4 E SOMA1_name 1']  # cell to apply input injection

bradb.AddStimInject(si1)
bradb.AddStimInject(si2)
bradb.AddStimInject(si3)
                    
print "CHECK6-Input"

print bradb

## start the simulation:

brainlab.Run(bradb, verbose=True, nprocs=1)

print "CHECK6-Run"


### PLOTS ###


#Voltage plots


brainlab.ReportPlot(brainname, "P2Report",cols=[1],plottitle="P(+) spikes", xlab="Timestep", ylab="mV", dosave=".png")
#brainlab.ReportPlot(brainname, "P3Report",cols=[1],plottitle="P(-) spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "P5Report",cols=[1],plottitle="P spikes", xlab="Timestep", ylab="mV", dosave=".png")
brainlab.ReportPlot(brainname, "Q5Report",cols=[1],plottitle="Q spikes", xlab="Timestep", ylab="mV", dosave=".png")


#Synaptic USE plots

#brainlab.ReportPlot(brainname, "P1USE",plottitle="P1(l1) syn excs", xlab="Timestep", ylab="mV", dosave=".png")
#brainlab.ReportPlot(brainname, "P1USE2",plottitle="P1(l2) syn inhs", xlab="Timestep", ylab="mV", dosave=".png") #TO FIX
#brainlab.ReportPlot(brainname, "P1USE3",plottitle="P1(l3) syn excs", xlab="Timestep", ylab="mV", dosave=".png")

#Spyke plots

#brainlab.ReportSpikePlot(brainname, "Brad_S1-E1Report.txt", usematplotlib=True, newfigure=True, xrange=None)
