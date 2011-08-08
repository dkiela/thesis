#!/usr/bin/env python

"""
    FIXME:  remove StandardStuff calls--now done automatically in BRAIN()
    20071108 resuming work.  converting all to numpy from numarray
"""

#import psyco
#psyco.full()

import matplotlib
#matplotlib.use('Agg')          # does not support jpg, tiff
matplotlib.use('WX')            # support jpg, tiff
#from brainlab import *
import brainlab
import pylab
import sys, socket
# is this from Numeric numpy or what?  for poisson:
#from numarray.random_array import *
#from numarray.random_array import *
from numpy.numarray.random_array import *
#import numarray.convolve as conv
from numpy import convolve as conv
# I believe all random functions are numarray random functions now--random.x() has
# been replaced by x() everywhere, which should use numarray.random_array fxns.
# importing basic python random package as stdrandom allows use of python's regular
# random fxns too:
import random as stdrandom
#import math

import threading        # for parallel ga evaluation

alllock=threading.Lock()

# global locking for parallel evaluation in threads by GA
def lock():
    alllock.acquire() 

def unlock():
    alllock.release()

def incthreadnum():
    global alllock
    global threadnum
    alllock.acquire() 
    threadnum+=1
    tn=threadnum
    alllock.release()
    return tn

def decthreadnum():
    global alllock
    global threadnum
    alllock.acquire() 
    threadnum-=1
    tn=threadnum
    alllock.release()
    return tn

def getthreadnum():
    global alllock
    global threadnum
    alllock.acquire() 
    tn=threadnum
    alllock.release()
    return threadnum

"""
FIXME:  all remote invocations that share a remote-invoke dir share an nlog.txt log file
FIXME:  all remote invocations that share a remote-invoke dir share a mach.txt machine file 

FIXME:  can layer's AddCellType take text name *or* variable name of a celltype?

THINK:  (move this comment to brain.py)
    When we specify a string in a connect, that string could simply be stored
    in the CONNECT tuple and then emitted during the print.  If the underlying
    variable has been added to the BRAIN already (e.g. in the lays or celltypes)
    then we could access it, but often the underlying variable won't be
    added to the BRAIN until the brain is being printed and we traverse the
    structures and add them.

    It makes it nice to have the variables rather than the strings while
    doing AddConnect() since then you can guess connection parameters
    intelligently and do intelligent connects with reduced information.

    One way to do this would be to insist on having all vars added to
    the brain "standard stuff" lists as you go along.  Make COLUMN a class
    within BRAIN?  Make LAYER a class within BRAIN or within COLUMN?

    Otherwise you get this thing where people keep their own list of layer,
    celltype, etc. objects, so that they can get the variables for names.
    This is in addition to the library lists in the BRAIN of "standard stuff".

    however when we add a column to a brain, we must have the variable,
    not just a string.
    when we add a layer to a column, we must have the layer variable,
    not just a string.
    same for celltypes etc.
    **Is it true that all object Adds require variables and not strings?
    (not AddConnects, object adds like AddColumn, AddLayer)
    Let's assume so for now.  if so, then we have
    all the information we need, it is just not summarized in list
    format (though we could make it that way . . .)
    We might have to traverse recursively to find the
    variable of interest from a text string name.
    why not have object creation be part of BRAIN:
    l=newb.LAYER()
    c=newb.COLUMN()
    ct=newb.CELLTYPE()
    this says that these types of things will be part of the brain, but
    their location in structure is not yet given until:
    then have additions be part of the sub-object:
    c.AddLayer(l)
    l.AddCellType(ct) 
    the sub-objects could access the brain as follows:  when the sub-object
    is created, it is created in the brain with self=brain, so we could
    store parent in them?  hmm, no . . . 

ANNOYANCE:
    have to create a column containing a cell just to do a simple test.
    would be most intuitive to allow a person to just connect two cells
    together without putting them into a column.  to do that, we would
    have to put them into a column ourselves . . . think about this
    There are now standard utility routines that simplify this.
    Standard1CellColumn() etc. and routines that can guess e.g.
    connections.

FIXME:
    change reporting requests to describe the desired end result:
    "voltage plot of these cells over this time range" or "spike plot
    of these cells over this time range" and don't require the user
    to make a report request and also a plot request.  Keep track of
    multiple requests for the same data range so they can share the same
    underlying report data (optional)

FIXME probably move syns, cols, etc. to BRAIN class

FIXME make geom=(x, y, w, h) in column create

request report/voltage probe 

ADD:  a gui?  draw cells, specify synapses, display in 3d, run button,
    show graphs interesting:  no channels in any of the
    ncs-current-experiments/exp*

come up with simple demo of:
    hebbian
    facilitation
    depression
        for f3, f2, f1 cells
    different channels

    USE, RSE plot evolution over time

DEMONSTRATE:  You need more than one pulse input to a cell, typically,
    to get that cell to fire.

"""

"""
    a couple of potential ways to specify stims:

    spikelist is a list of timesteps at 
    this will be converted to MODE CURRENT spikes applied via a stim file, with probability 0/1.0 . . .
    not that easy, what about DYN_RANGE? 

    AddSpikeTrain(spikelist, where)
"""

fignum=1

def RandSpikeList(duration, interspike, starttime=0.0, type=None, pmean=25):
    s=[]
    if type=='poisson': 
        pn=duration*pmean*2
        #a=RandomArray.poisson(pmean, pn)      # returns 50 int elements with poisson mean pmean (==stddev).  type 'array'
        i=0
        time=starttime
        time+=float(poisson(pmean)/1000.0)
        while time < (starttime+duration):
            s.append(time)
            i+=1
            time+=float(poisson(pmean)/1000.0)
        return s

    time=starttime
    time+=int((random() * interspike)+10.0)/1000.0
    while time < (starttime+duration):
        s.append(time)
        time+=int((random() * interspike)+10.0)/1000.0
    return s

def TestStim(brain):
    numcells=100
    maxtime=100                      # 100 ms
    s=brain.StimFile(numcells)       # 100=number of cells we will be stimulating (channels in stim)
    for c in range(0, numcells):
        time=stdrandom.randrange(0, 20)
        while time < maxtime:
            s.AddSpike(c, time)
            time+=stdrandom.randrange(10, 30)

    return s

def ComposeStimSequences(brain, stimlist):
    pass

def E1MakeMiniCol():
    pass

def E1MakeBrain():
    nminicols=50
    minicols=[]

    """
    do we need to enumerate all cells in the minicols or can we use NCS
    to do probabilistic connects?
    does whether we have separate "input" areas that feed to the minicol
    input layers have bearing on the issue of whether we need to enumerate?
    benefits of separate input area:
      could have input stim file feed to just that area--otherwise would have to
      split into multiple input files, one for each minicol, since a stim can
      only go to one cell group (right?).  may not be such a big deal though
      could introduce a new brainlab stimulus operation that takes a list
      of spike times (for a list of cells! (or cell groups?)), and converts that to a pulse
      at the requested time.  and a new brainlab report option that gives a report
      for each of a list of cells . . . hmm.

    assumptions, for now:
    it is easy to create an input layer that maps one-to-one to all the L1 input cols
    for example, and then stimulate the input layer with pulses.  The input layer nrns
    will pass the spike (with some delay, hmm)
    since we have neurons in L1 that accept input from thal as well as Key input,
    we can't simply force those L1 cells to fire by pulsing them according to key input
    That would override thal sequencing input.
      we WILL have an input layer for the key input that then feeds to the L1 "buss"
      we will enumerate all cells in minicol.
    To read the output "name" we will report DIRECTLY on some of L2, L3, L5
    To input the "data" we will pulse stimulate DIRECTLY all the L6s.  If it turns out
    that some other input goes into the L6s, that won't work because the direct current pulse
    would drown it out.  in that case, we could create a separate input area that feeds to
    combined L6s
    since we do need to be able to stimulate individual cells to define a pattern
    question:  is a minicolumn's activity determined by just one cell in L2, L3, or L5?
    a set of cells in that layer?  is a minicolumn considered "active" or "inactive" or
    do we need to look at each cell in L2, L3, or L5?  Even if we looked at only one
    cell in those layers, we have 50 minicols, so we would still have a vector of activation
    to look at over time . . . 
    """

    # make the main cortical column's minicolumns
    for i in range(0, nminicols):
        m=E1MakeMiniCol() 
        minicols.append(m)

    # make a simple thalamus
    thal=None

    # make the "key" input area that feeds to each layer 1
    keyin=None

    # make the "data" input area that feeds to each layer 6

    # make the intercolumn connections
    for m in minicols:
        # each layer 5 to thalamus 
        # each layer 4 inhibitory to all other layer 4s
        # thalamus to each layer 1
        # key input area to each layer1
        pass

def Experiment1():
    """
        NOT WORKING
    """
    numstims=10
    timestotrain=30             # train with this many K+T stim applications
    timestotest=10              # look at this many K only stim applications
    numsequences=10
    stimduration=100    # ms
    trainingtime=stimduration*numsequences*timestotrain
    testingtime=stimduration*numsequences *timestotest
    totalruntime=trainingtime+testingtime

    # do we need to put all stims together and run the brain just once?  yes.
    # since we are relying on hebb learning for all sequences, unless we are
    # saving brain state, we'll have to do it all in one run

    #for i in range(0, numstims):

    #brain=MakeBrain()
    #tstims=MakeTStims(10)      # the list of Test stim inputs
    #kstims=MakeKStims(10)      # the list of Key stim inputs

    # create a combined stim made up of all sequences concatenated?

    # do we always want to train with same order of (T,K) pairs?

    # add the training T,K stims
    stimapplytime=0
    for t in range(0,timestotrain): 
        # for training we apply both the training stim and the key stims:
        # if the stim we are applying contains all sequences, don't do this here
        #for s in range(0, numsequences)
        # tstims is a list of voltage or current values, one per timestep?
        brain.AddStim(tstims, stimapplytime)
        brain.AddStim(kstims, stimapplytime)
        #ADD REPORT ON LAYER 2 HERE
        #ADD REPORT ON LAYER 3 HERE
        stimapplytime+=stimduration*numsequences

    # add the test K-only stims
    # what is applied to T at this time
    for t in range(0,timestotest):
        brain.AddStim(kstims, stimapplytime) 
        #ADD REPORT ON LAYER 2 HERE
        #ADD REPORT ON LAYER 3 HERE
        stimapplytime+=stimduration*numsequences

    # to examine things in a convenient format that only considers spike times:
    GetSpikeTimes()

    brain.Run(trainingtime+testingtime)

def ICol():
    """
    """
    L1=LAYER({"TYPE":"L1"})
    L2=LAYER({"TYPE":"L2"})
    L3=LAYER({"TYPE":"L3"})
    L4=LAYER({"TYPE":"L4"})
    L5=LAYER({"TYPE":"L5"})
    L6=LAYER({"TYPE":"L6"})

    C=COLUMN()
    c.AddLayerType(L1)
    c.AddLayerType(L2)
    c.AddLayerType(L3)
    c.AddLayerType(L4)
    c.AddLayerType(L5)
    c.AddLayerType(L6)

    #c.AddConnect(L1, 

    c.AddConnect(L2, L5)

    #c.AddConnect(L2, layer 6 of next 'higher' col)
    #c.AddConnect(L3, layer 6 of next 'higher' col)

    c.AddConnect(L3, L5)

    c.AddConnect(L4, L2)
    c.AddConnect(L4, L3)

    #c.AddConnect(L5, to thalamus)
    c.AddConnect(L5, L6)    # check this

    c.AddConnect(L6, L4)
    c.AddConnect(L6, L1)    # L1 is 'common' layer, all to all connects.  connect to L1 of ALL other cols

    #ThalCol.AddConnect(

def BCol2(newb, name, emsize=10, otherlaysize=10, DoInhib=True, l1emprob=None, eremprob=None, eresprob=None,
        eri1prob=None, i1esprob=None, esi1prob=None, emesprob=None, esemprob=None, i1emprob=None, emi1prob=None, i1i1prob=None,
        esesprob=None, ememprob=None, synE="E", synI="I", synprobs=None, w=100, h=400):
    """
        this uses inhib cells in their own layer; would be more realistic to
        put them as a different cell group in all/some other layers
    """
    x, y=(0, 0)
    c=newb.COLUMN({"TYPE":name, "_WIDTH":w, "_HEIGHT":h, "_XLOC":x, "_YLOC":y})
    newb.AddColumn(c)

    # get a basic cell named cellE that is a copy of the ES type:
    # can't use just 'E' since it is also a name of standard synapse
    ecell=newb.Copy(newb.celltypes, "ES", "cellE")
    icell=newb.Copy(newb.celltypes, "I1", "cellI")

    l1=newb.LAYER({"TYPE":"layL1", "_UPPER":100, "_LOWER":80})
    c.AddLayerType(l1)
    l1.AddCellType(ecell, otherlaysize) 

    em=newb.LAYER({"TYPE":"layEM", "_UPPER":75, "_LOWER":55})
    c.AddLayerType(em)
    em.AddCellType(ecell, emsize) 

    er=newb.LAYER({"TYPE":"layER", "_UPPER":50, "_LOWER":30})
    c.AddLayerType(er)
    er.AddCellType(ecell, otherlaysize) 

    es=newb.LAYER({"TYPE":"layES", "_UPPER":25, "_LOWER":5})
    c.AddLayerType(es)
    es.AddCellType(ecell, otherlaysize) 

    # hmm, spread these out in the different layers?
    i1=newb.LAYER({"TYPE":"layI", "_UPPER":65, "_LOWER":45})          # common inhib cells for entire layer.
    c.AddLayerType(i1)
    i1.AddCellType(icell, otherlaysize) 

    bprob=.6        # .1
    iprob=.6        # .0134
    if l1emprob==None: l1emprob=bprob
    if eremprob==None: eremprob=bprob
    if eresprob==None: eresprob=bprob
    if eri1prob==None: eri1prob=bprob
    if i1esprob==None: i1esprob=iprob
    if esi1prob==None: esi1prob=bprob
    if emesprob==None: emesprob=bprob
    if esemprob==None: esemprob=bprob
    if i1emprob==None: i1emprob=iprob
    if emi1prob==None: emi1prob=bprob
    if i1i1prob==None: i1i1prob=iprob
    if esesprob==None: esesprob=bprob
    if ememprob==None: ememprob=bprob

    se=newb.syntypes[synE]
    si=newb.syntypes[synI]

    c.AddConnect(l1, em, syn=se, prob=l1emprob)
    c.AddConnect(er, em, syn=se, prob=eremprob)
    c.AddConnect(er, es, syn=se, prob=eresprob)
    c.AddConnect(er, i1, syn=se, prob=eri1prob)
    c.AddConnect(es, i1, syn=se, prob=esi1prob)
    c.AddConnect(em, es, syn=se, prob=emesprob)
    c.AddConnect(es, em, syn=se, prob=esemprob)
    c.AddConnect(em, i1, syn=se, prob=emi1prob)
    c.AddConnect(es, es, syn=se, prob=esesprob)
    c.AddConnect(em, em, syn=se, prob=ememprob)

    if DoInhib:
        print "doing inhib"
        c.AddConnect(i1, es, syn=si, prob=i1esprob)
        c.AddConnect(i1, em, syn=si, prob=iprob)
        c.AddConnect(i1, i1, syn=si, prob=iprob)

    return c

def BLayer(name, celltypes, comptypes, syntypes, emsize=10, otherlaysize=10, DoInhib=True, l1emprob=None, eremprob=None, eresprob=None,
        eri1prob=None, i1esprob=None, esi1prob=None, emesprob=None, esemprob=None, i1emprob=None, emi1prob=None, i1i1prob=None,
        esesprob=None, ememprob=None, synE="E", synI="I", synprobs=None):
    """
        define a balanced layer
        EM:  L2/3
        ER:  L4 (from thal)
        ES:  L5/6
        Note that this is putting all biological layers into one NCS
        layer, using cell groups as layers, which sort of defeats the
        purpose of NCS layers.  That's what Dr. Goodman was doing though.
        BCol2 will fix that, keeping a similar structure but putting
        each layer into its own NCS layer, which also makes things
        directly graphable more nicely.
    """
    l=LAYER({"TYPE":name})
    L1=l.AddCellType(celltypes["L1"], otherlaysize)        # separate these into a separate L1 "buss"?
    EM=l.AddCellType(celltypes["EM"], emsize)
    ER=l.AddCellType(celltypes["ER"], otherlaysize)
    ES=l.AddCellType(celltypes["ES"], otherlaysize)
    I =l.AddCellType(celltypes["I1"], otherlaysize)

    bprob=.6        # .1
    iprob=.6        # .0134
    if l1emprob==None: l1emprob=bprob
    if eremprob==None: eremprob=bprob
    if eresprob==None: eresprob=bprob
    if eri1prob==None: eri1prob=bprob
    if i1esprob==None: i1esprob=iprob
    if esi1prob==None: esi1prob=bprob
    if emesprob==None: emesprob=bprob
    if esemprob==None: esemprob=bprob
    if i1emprob==None: i1emprob=iprob
    if emi1prob==None: emi1prob=bprob
    if i1i1prob==None: i1i1prob=iprob
    if esesprob==None: esesprob=bprob
    if ememprob==None: ememprob=bprob
        
    l.AddConnect("L1", "EM", syntypes[synE], prob=l1emprob)

    l.AddConnect("ER", "EM", syntypes[synE], prob=eremprob)
    l.AddConnect("ER", "ES", syntypes[synE], prob=eresprob)
    l.AddConnect("ER", "I1", syntypes[synE], prob=eri1prob)
    if DoInhib:
        print "doing inhib"
        l.AddConnect("I1", "ES", syntypes[synI], prob=i1esprob)
    l.AddConnect("ES", "I1", syntypes[synE], prob=esi1prob)
    l.AddConnect("EM", "ES", syntypes[synE], prob=emesprob)
    l.AddConnect("ES", "EM", syntypes[synE], prob=esemprob)
    if DoInhib:
        l.AddConnect("I1", "EM", syntypes[synI], prob=iprob)
    l.AddConnect("EM", "I1", syntypes[synE], prob=emi1prob)
    if DoInhib:
        l.AddConnect("I1", "I1", syntypes[synI], prob=iprob)
    l.AddConnect("ES", "ES", syntypes[synE], prob=esesprob)
    l.AddConnect("EM", "EM", syntypes[synE], prob=ememprob)
    return l

def BCol(name, layer):
    c=COLUMN({"TYPE": name})
    c.AddLayerType(layer)
    return c

def Junk():
    for i in incols:
        #newb.AddConnect(incol[i], lays[i+"_1CELL"], celltypes["ER"], "S1", col2, lays["col2_1CELL"], celltypes["ER"], "S1", syns["C.strong"], "1.0", "10.0")
        newb.AddConnect(incol[i], i+"_1CELL", celltypes["ER"], "S1", col2, lays["col2_1CELL"], celltypes["ER"], "S1", syns["C.strong"], "1.0", "10.0")
        #newb.AddSimpleStim("stim"+i, i, i+"_1CELL", "ER", "SOMA1_name", "v", "1", "1", ".0025", "10.0", "10.0", ".001", "9999", dur=(0.0, 1.0), pattern="SINE")
        # FIXME:  when we AddSimpleStim, we specify report name, col NAME, lay NAME, cell NAME, cmp NAME
        newb.AddSimpleStim("stim"+i, i, i+"_1CELL", "ER", "SOMA1_name", "c", ampstart=10.0, ampend=10.0, width=.001, freqstart=10.0, dur=(0.0, 1.0), pattern="PULSE")

    # why is the col for AddSimpleStim a text name and not a var, as it is a var for AddConnect?
    # current injection:
    #newb.AddSimpleStim("teststim", "col1", "col1_1CELL", "ER", "SOMA1_name", "c", "1", "1", ".0025", "10.0", "10.0", ".001", "9999", "0.0", "1.0", pattern="SINE")
    # voltage input:

    newb.AddSimpleReport("Incol1", "incol1", "incol1_1CELL", "ER", "S1", "v", "1", dur=(0.0, endsim))
    newb.AddSimpleReport("Col2", "col2", "col2_1CELL", "ER", "S1", "v", "1", dur=(0.0, endsim))

    #print newb
    #newb.Plot3D()

    # does ReportPlot belong as a class of BRAIN?
    # is it good to specify explicit reports to add to brain, and then
    # plain filenames we want to plot together, rather than having
    # some more general request to "plot voltages"
    # FIXME:  bad to have to include brainname here.  make it a BRAIN class and extract name
    #ReportPlot(brainname, ["Col0", "Col1", "Col2"])
    ReportPlot(brainname, ["Incol1", "Col2"])

    # want to put input stim on same plot as output
    #r=col.VoltageProbe()

    sys.exit(0)

    #col=EnumeratedColumn("colname", "synpref", 10, 10, 10, 10, lays, celltypes, syns, comptypes, [(10,5), (5,6), (16, 5)])
    #newb.AddColumn(col)

    asize=1
    bsize=1
    csize=1
    newb.AddArea("A", asize, asize, asize, asize, 200, 200, 0, 0, StandardEnumeratedColumn, lays, celltypes, syns, comptypes)
    newb.AddArea("B", bsize, bsize, bsize, bsize, 200, 200, 0, 200, StandardEnumeratedColumn, lays, celltypes, syns, comptypes)
    newb.AddArea("C", csize, csize, csize, csize, 200, 200, 0, 400, StandardEnumeratedColumn, lays, celltypes, syns, comptypes)

    conpat="all"
    syn="E"
    prob=0.1
    # test enumerated to enumerated connections:
    newb.ConnectAreas("A", "B", conpat, syns[syn], prob, "10.0", lays, celltypes)
    newb.ConnectAreas("B", "C", conpat, syns[syn], prob, "10.0", lays, celltypes)
    # test non enumerated to enumerated:
    syn="E"
    #newb.ConnectAreas("C", "B", conpat, syns[syn], prob, "10.0", lays, celltypes)

    newb.syns=syns
    plot(newb, brainname)

    #####
    if 0:
        ReportPlot(brainname, ["L1Rep"])
        ReportPlot(brainname, ["EMRep"])
        ReportPlot(brainname, ["Key0Rep"])

        o1=LoadSpikeData(brainname, "EMRep", starttime=0.0, endtime=0.5)
        o2=LoadSpikeData(brainname, "EMRep", starttime=0.5, endtime=1.0)
        o3=LoadSpikeData(brainname, "EMRep", starttime=1.0, endtime=1.5)
        o4=LoadSpikeData(brainname, "EMRep", starttime=1.5, endtime=2.0)

        print "  L1 outputs: ", CountSpikes(brainname, "L1Rep")
        print "  EM outputs: ", CountSpikes(brainname, "EMRep")
        print "  ER outputs: ", CountSpikes(brainname, "ERRep")
        print "  ES outputs: ", CountSpikes(brainname, "ESRep")
        ks=[]
        for k in range(0, thalsize):
            ks.append(CountSpikes(brainname, "Thal"+`k`+"Rep")[0])
        print "THAL outputs: ", ks

    """
    # this does show agreement in spike counts applied to key layer and read from its output.  good.
    ReportPlot(brainname, ["Key0Rep"])
    print "These should agree:"
    for k in [0, 4]:
        print "spikes counted in report for Key cell", k, ":", CountSpikes(brainname, "Key"+`k`+"Rep")
        print "spike pulses applied on input to Key cell", k, ":", len(keyinstim[k])
    """

def TestMultiCompartment(seed=.987987):
    """ FIXME:  change to use new brain.chantypes etc.
    """
    print "FIXME:  TestMultiCompartment random seed"
    #random.seed(seed)
    endsim=1.0
    newb=BRAIN({"TYPE": "AREA-BRAIN", "FSV": "10000.00", "JOB": brainname,
                "SEED": "-99", "DURATION": `endsim`, "OUTPUT_CELLS": "YES",
                "OUTPUT_CONNECT_MAP": "YES", "DISTANCE": "YES"})

    #compartments=[("SOMA1", None)]   # compname, leak conductance
    compartments=[("SOMA1", None), ("dend1", .01), ("dend2", .02), ("dend3", .02)]   # compname, leak conductance
    # note that SOMA1 is already part of the standard cell we are using
    # we will connect these compartments in order, leading out to most distal dend3
    # the list could be extended arbitrarily, and other parameter modifications
    # supplied in the tuple for each compartment (with appropriate modifications
    # to loop below)

    chantypes=StandardChannels()
    spks=StandardSpikes()
    comptypes=StandardCompartments(spks, chantypes)
    celltypes=StandardCells(comptypes)
    spsgs=StandardPSGs(None, None)
    sfds=StandardSFDs()
    sls=StandardSLs()
    syntypes=StandardSynapses(spsgs, sls, sfds)
    lays=StandardLayers(syntypes, celltypes)

    #print comptypes["SOMA1"].parms["CHANNEL"]
    # this would clear all channels away:
    # comptypes["SOMA1"].parms["CHANNEL"]={}
    #sys.exit(0)

    c=Standard1CellColumn("col1", "synpref", 0, 0, 0, 0, lays, celltypes, syntypes, comptypes)
    newb.AddColumn(c)
    cell=celltypes["ER"]

    #print "standard compartment types are:"
    #print comptypes

    x = y = z = 0.0
    for cn in range(0, len(compartments)-1):
        cmptype, cmpparm=compartments[cn]
        nextcmptype, nextcmpparm=compartments[cn+1]
        cmp=comptypes[cmptype]
        nextcmp=newb.Copy(comptypes, "SOMA1", nextcmptype)
        # example of changing some parameter per compartment:
        nextcmp.parms["LEAK_CONDUCTANCE"]="%.4f %.4f" % (nextcmpparm, 0.0)
        cell.AddCompartment(nextcmp, x, y, z)
        #cell.AddConnect(cmp, nextcmp, 1, "0.175", "0.2")
        # this causes dend2,3 to spike a lot, dend1 a bit, soma1 subthresh bumps 
        cell.AddConnect(cmp, nextcmp, 1, "0.002", "0.000")
        # this causes dend2,3 to spike a lot, dend1 a bit, soma1 not at all, smooth
        #cell.AddConnect(cmp, nextcmp, 1, "0.000", "0.002")

    #print "available compartment types are now:"
    #print comptypes
    #sys.exit(0)

    #print "the cell ER now contains these compartments:"
    #print cell
    #sys.exit(0)

    for comptype, compparm in compartments:
        compname=comptype+"_name"
        reportname=comptype+"_report"
        newb.AddSimpleReport(reportname, "col1", "col1_1CELL", "ER", compname, "v", "1", dur=(0.0, endsim))

    # apply a pulse to the most distal compartment:
    #newb.AddSimpleStim("stimname", "col1", "col1_1CELL", "ER", "SOMA1_name", "c", ampstart=10.0, ampend=10.0, width=.001, freqstart=1.0, dur=(0.2, 1.0), pattern="PULSE")
    newb.AddSimpleStim("stimname", "col1", "col1_1CELL", "ER", "dend3_name", "c", ampstart=10.0, ampend=10.0, width=.001, freqstart=1.0, dur=(0.2, 1.0), pattern="PULSE")

    # if you want to see what the NCS .in file looks like, print it like this:
    #print newb
    #sys.exit(0)

    newb.Run()

    for comptype, compparm in compartments:
        compname=comptype+"_name"
        reportname=comptype+"_report"
        ReportPlot(brainname, [reportname], title=compname)

def TestSpikeTrainFileInput(method="File", seed=.21342342):
    """
        Demonstration of composing a stimulus in the form of a list of spike times,
        applying that stimulus to a cell in a column, and graphing the result.

        If method=="File" convert the stimulus time list to a stimulus file and
        apply that.  If method=="Pulse" then convert the stimulus time list to 
        a series of separate PULSE STIMULUS blocks.

        Status:  works
    """
    print "FIXME:  TestSpikeTrainFileInput random seed"
    #random.seed(seed)
    endsim=1.0
    newb=BRAIN({"TYPE": "AREA-BRAIN", "FSV": "10000.00", "JOB": brainname,
                "SEED": "-99", "DURATION": `endsim`, "OUTPUT_CELLS": "YES",
                "OUTPUT_CONNECT_MAP": "YES", "DISTANCE": "YES"})

    chantypes=StandardChannels()
    spks=StandardSpikes()
    comptypes=StandardCompartments(spks, chantypes)
    celltypes=StandardCells(comptypes)
    spsgs=StandardPSGs(None, None)
    sfds=StandardSFDs()
    sls=StandardSLs()
    syntypes=StandardSynapses(spsgs, sls, sfds)
    lays=StandardLayers(syntypes, celltypes)
    #print comptypes["SOMA1"].parms["CHANNEL"]
    # this would clear all channels away:
    # comptypes["SOMA1"].parms["CHANNEL"]={}
    #sys.exit(0)
    c=Standard1CellColumn("col1", "synpref", 0, 0, 0, 0, lays, celltypes, syntypes, comptypes)
    d=Standard1CellColumn("col2", "synpref", 0, 0, 0, 0, lays, celltypes, syntypes, comptypes)
    newb.AddColumn(c)
    newb.AddColumn(d)
    newb.AddConnect(c, "col1_1CELL", celltypes["ER"], "S1", d, "col2_1CELL", celltypes["ER"], "S1", syntypes["C.strong"], "1.0", "10.0")

    # create a list of spike times, in seconds, with inter-spike intervals of 25-125 ms,
    # on 2.5ms boundaries:
    s=[]
    t=((int(random()*40.0))/1000.0)*2.5
    print t
    while t < endsim:
        s.append(t)
        t+=.010+((int(random()*40.0))/1000.0)*2.5
    for p in s:
        print "%.4f" % p,
    print
    print len(s), "spikes"
    #sys.exit(0)

    #newb.AddSimpleStim("stimname", "col1", "col1_1CELL", "ER", "SOMA1_name", "c", ampstart=10.0, ampend=10.0, width=.001, freqstart=10.0, dur=(0.0, 1.0), pattern="PULSE")
    if method=="File":
        newb.AddSpikeTrainFileStim("stimname", "col1", "col1_1CELL", "ER", s)
    elif method=="Pulse":
        newb.AddSpikeTrainPulseStim("stimname", "col1", "col1_1CELL", "ER", s)
    else:
        print "method for spike injection should be File or Spike"
 
    newb.AddSimpleReport("Col1Report", "col1", "col1_1CELL", "ER", "S1", "v", "1", dur=(0.0, endsim))
    #print newb
    newb.Run()
    ReportPlot(brainname, ["Col1Report"], title=method+", random seed=%.4f" % seed)

def TestPulseInput():
    """
        Demonstration of composing a stimulus in the form of a list of spike times,
        applying that stimulus to a cell in a column, and graphing the result.
        Status:  works
    """
    endsim=1.0
    newb=BRAIN({"TYPE": "AREA-BRAIN", "FSV": "10000.00", "JOB": brainname,
                "SEED": "-99", "DURATION": `endsim`, "OUTPUT_CELLS": "YES",
                "OUTPUT_CONNECT_MAP": "YES", "DISTANCE": "YES"})

    chantypes=StandardChannels()
    spks=StandardSpikes()
    comptypes=StandardCompartments(spks, chantypes)
    celltypes=StandardCells(comptypes)
    spsgs=StandardPSGs(None, None)
    sfds=StandardSFDs()
    sls=StandardSLs()
    syntypes=StandardSynapses(spsgs, sls, sfds)
    lays=StandardLayers(syntypes, celltypes)
    c=Standard1CellColumn("col1", "synpref", 0, 0, 0, 0, lays, celltypes, syntypes, comptypes)
    newb.AddColumn(c)
    newb.AddSimpleStim("stim", "col1", "col1_1CELL", "ER", "SOMA1_name", "c", ampstart=10.0, ampend=10.0, width=.001, freqstart=10.0, dur=(0.0, 1.0), pattern="PULSE")
    newb.AddSimpleReport("Col1Report", "col1", "col1_1CELL", "ER", "S1", "v", "1", dur=(0.0, endsim))
    print newb
    newb.Run()
    ReportPlot(brainname, ["Col1Report"])

def TestFacil(showplots=False):
    """ Simple demonstration of synaptic facilitation, and then depression (separately).
        Checked RPD 11/11/2007

        What you should see:
            Facilitation only:
                USE values don't change from facilitation alone.
                RSE values don't change from facilitation alone.
                USE_New values DO increase with facilitation alone.
                Note also that USE_New is a bad name for this, but that is what is in NCS code.
                    USE_Current would be a better name for USE_New and USE_Last would be a better name
                    for USE_Old since USE_Last is just USE_Current of the last timestep (there is
                    no way of reporting on USE_Old)
                In NCS code, USE_New and USE_Old are the old and new *current* USE values, but Syn->USE
                    is the *setpoint* (which is only adjusted via Hebbian learning)
                Once facilitation stops, USE_New decays back to the initial value of USE (initialized from
                    ABSOLUTE_USE in .in file).
                Note that the decay only shows up in the report when a spike occurs;
                    the SYNAPSE_UF report continues to show the old value until there is some update.
                    (CONFIRM THIS AND REPORT THIS TO GOODMAN)
                What you should see in the example below:
                In the plots with a small facil tau time constant, you can't get a fast enough buildup of USE_New
                    to cause a spike on the output.  (You could increase the initial spike rate to compensate, but
                    in the plots shown, spikes don't happen on output until facil tau is about .25.)
                Note also that the spikes don't occur right when the input spikes start; it takes a while
                    for facilitation to build up the USE_New.
                The initial value of USE_New is taken from ABSOLUTE_USE in .in file.
                Positive Hebbian learning would permanently increase the USE setpoint to which the USE_New returns.
            Depression only:
                RSE is the parameter relating to depression.  The initial value is given by a min/max range
                    in the .in file, *not* a value/stddev pair.  The initial value is picked randomly from
                    within the min/max range.
                during spiking, RSE will deplete downward from its current value.
                Note that as with USE New for 
                in the absence of spiking, RSE will decay back up to 1.0.  So if there has been no
                    spiking for a long time, RSE will be 1.0 and there will be no attenuation of USE strength
                if spiking is rapid relative to depr tau, RSE will decay a lot; if spiking is not rapid
                    relative to depr tau, you won't get much additive reduction of RSE
                What you should see in the example below:
                the first spikes input to T cause T to fire.  however, if depression is effective
                    depr tau long relative to the frequency of spikes, so depression accumulates,
                    the output spike rate becomes reduced and eventually the current input
                    will be reduced enough that spiking will stop.

        if F is too long, we won't see much of an effect within the scope of the experiment
        if F is too short relative to our spike applications, the effect of the facil will
        be lost by the time the next spike is applied

        NOTE:  is appears that the USE_New value (the NCS and also as reported in the SYNAPSE_UF report)
        is not updated in the absence of a spike.  So its value will appear to stay constant even
        if there is no faciliation activity, but once the next spike occurs it will be recalculated correctly.
        Same for RSE--it is only updated when a spike actually occurs, so an old (really invalid) value
        will still show up in the reports until a spike causes an update.

        exercise:  back compute time constants based on height of EPSP?

    TRUE OR FALSE:
        If you start with RSE_INIT at 1.0, then no facilitation can happen since we are already
        at max.  A:  False.  RSE only applies to depression.  Facilitation will adjust upward the USE_New
        value from the USE setpoint (which comes from the ABSOLUTE_USE field in the .in file but can
        be adjusted by Hebbian learning).  Depression only adjust down, temporarily, the RSE setting.
        the RSE setting and the USE_New setting are, effectively, multiplied by the USE setting to
        get the synapses actual efficacy.  During inactivity, USE_New decays back down to the USE setpoint
        and RSE decays back up to 1.0.

    """
    t=0.3; te=t+2.0; ts=.05
    ain=[]
    while t<te:
        ain.append(t)
        t+=ts
    t+=1.0
    te=t+1.0; ts=.2
    while t<te:
        ain.append(t)
        t+=ts
    endsim=t+.1

    print "Pulses will be applied at these times:", ain

    brainname='FacilDemo'
    ft='F0'
    print "brainname is "+brainname
    FSV=10000.0
    newb=brainlab.BRAIN({"TYPE": "AREA-BRAIN", "FSV": "%.2f"%FSV, "JOB": brainname,
                    "SEED": "-99", "DURATION": `endsim`, "OUTPUT_CELLS": "YES",
                    "OUTPUT_CONNECT_MAP": "YES", "DISTANCE": "YES"})

    A=newb.Standard1CellColumn("A")
    T=newb.Standard1CellColumn("T")
    cs=newb.syntypes["C.strong"]
    cs.parms["LEARN_LABEL"]=newb.sls["0Hebb"]
    cs.parms["ABSOLUTE_USE"]='0.2   0.0'
    cs.parms["RSE_INIT"]='0.9 0.9'
    newb.AddConnect(A, T, newb.syntypes["C.strong"], "1.0", "10.0")
    cs.parms["SFD_LABEL"]=newb.sfds[ft]

    d=(0.0, endsim)

    newb.AddSpikeTrainPulseStim("Astim", "A", "A_1CELL", "ER", ain)

    lc=0
    # a time constant of 0.0 or infinity would disable the effect?  0.0, but that is not permitted as a
    # way to disable facil or depr.  instead, to disable, pick FACIL to disable DEPR or DEPR to disable FACIL
    # or NONE to disable both
    for (sfd, fac, dep) in [('FACIL', .10, 0.0), ('FACIL', .20, 0.0), ('FACIL', .25, 0.0), ('FACIL', .30, 0.0),
        ('DEPR', 0.0, .10), ('DEPR', 0.0, .20), ('DEPR', 0.0, .30), ('DEPR', 0.0, .40)]:
        # we want a higher conductivity for DEPR so that spikes happen at start and then stop when depr
        # takes over, and a lower conductivity for FACIL tests so that spikes don't happen at first
        # until facilitation builds up:
        if sfd=='DEPR':  cs.parms["MAX_CONDUCT"]='0.10'
        elif sfd=='FACIL':  cs.parms["MAX_CONDUCT"]='0.02'
        creport="TReportC-%s-%f-%f" % (sfd, fac, dep)
        vreport="TReportV-%s-%f-%f" % (sfd, fac, dep)
        ureport="TReportU-%s-%f-%f" % (sfd, fac, dep)
        freport="TReportF-%s-%f-%f" % (sfd, fac, dep)
        rreport="TReportR-%s-%f-%f" % (sfd, fac, dep)
        newb.AddSimpleReport(creport, T, "c", dur=d)
        newb.AddSimpleReport(vreport, T, "v", dur=d)
        newb.AddSimpleReport(ureport, T, "a", synname="C.strong", dur=d)
        newb.AddSimpleReport(freport, T, "f", synname="C.strong", dur=d)
        newb.AddSimpleReport(rreport, T, "r", synname="C.strong", dur=d)
        # note that for a SYN_CURRENT report, we give the name of the compartment that the synapse
        # COMES FROM, not connects to!  (FIXME:  confirm that.  doesn't seem to be working)
        #newb.AddSimpleReport(sreport, "A", "A_1CELL", "ER", "SOMA1_name", "s", "1", dur=d)
        #(fac, fsd)=newb.sfds[ft].parms["FACIL_TAU"].split()
        newb.sfds[ft].parms["SFD"]=sfd
        newb.sfds[ft].parms["FACIL_TAU"]="%f  0.0" % fac       # set stdev to 0 so we know what we're getting
        #(dep, dsd)=newb.sfds[ft].parms["DEPR_TAU"].split() 
        newb.sfds[ft].parms["DEPR_TAU"]="%f  0.0" % dep      # set stdev to 0 so we know what we're getting
        if lc==0: clearreports=True
        else: clearreports=False
        newb.Run(verbose=True, nprocs=1, clearreports=clearreports)
        if 0:
            if ft=="F0": clearreports=True      # only clear reports on first run of batch
            else: clearreports=False
            newb.Run(verbose=True, nprocs=1, clearreports=clearreports)
        if 1:
            nsp=5; csp=1
            nextfigure()

            subplot(nsp, 1, csp); csp+=1
            ReportPlot(brainname, creport, plottype=None, plottitle="Net current into Cell T, F tau=%f D tau=%f" % (fac, dep), xlab="", ylab="mA", newfigure=False)
            locs, labels=xticks()
            xticks(locs, [""]*len(locs))    # we want the tick marks, but not the labels
            #ylim(-.2, 1.0)
            xlim(-1000, endsim*FSV)

            subplot(nsp, 1, csp); csp+=1
            ReportPlot(brainname, vreport, plottype=None, plottitle="Cell T voltage, F tau=%f D tau=%f" % (fac, dep), xlab="", ylab="mV", newfigure=False)
            ylim(-80, 80)
            xlim(-1000, endsim*FSV)

            subplot(nsp, 1, csp); csp+=1
            ReportPlot(brainname, ureport, plottype=None, plottitle="", xlab="", ylab="USE", newfigure=False)
            ylim(0, 1.0)
            xlim(-1000, endsim*FSV)

            subplot(nsp, 1, csp); csp+=1
            ReportPlot(brainname, freport, plottype=None, plottitle="", xlab="", ylab="USE New", newfigure=False)
            ylim(0, 1.0)
            xlim(-1000, endsim*FSV)

            subplot(nsp, 1, csp); csp+=1
            ReportPlot(brainname, rreport, plottype=None, plottitle="", xlab="Timestep", ylab="RSE", newfigure=False)
            ylim(0, 1.0)
            xlim(-1000, endsim*FSV)

            lc+=1
            savefig("%s:%s-%f-%f.png" % (brainname, sfd, fac, dep))
        # delete the report requests from the brain, because for the next run we want to save info to a different report name
        # so that we can process reports offline later
        # this approach to clearing reports works fine, but is maybe not the cleanest way to do it.  add newb.DeleteReport()?
        newb.parms["REPORT"]=[]

    if showplots: show()

def TestHebbian(showplots=False):
    """
        Tested 20081128 RPD:  for unknown reason, when retested now, initial B spikes alone caused T spikes.
            Had to reduce B-> MAXCOND from .1 to .05

        Tested 20071111 RPD

        Simple demonstration of positive and negative Hebbian learning
        Protocol:
            facilitation and depression turned off (for simplicity, to isolate Hebbian effect)
            we have two input neurons, A and B, synapsing on a target T
            (each neuron is set up in its own 1-cell column)
            A is strongly connected to T (high USE/conductivity) so that a spike on A alone will cause T to spike
            B is weakly connected to T so that a spike on B alone will not cause T to spike 
            We start a spike train on A and look at T.  We show that T spikes with A alone.  Stop this input.
            We start a spike train on B and look at T.  We show that T does not spike with B alone.  Stop this input.
            We start a spike train on A and a spike train on B such that B spikes come shortly before A spikes (and T spikes)
            This is the condition for positive Hebbian learning.  The B->T synapse should be strengthened.
            We stop all input, then provide only B spikes.  T now spikes because the B->T synapse has been strengthened.

        Hebbian learning 'permanently' adjust endpoint of USE.  Which parameter does this correspond to?
            ABSOLUTE_USE?
            YES, CONFIRMED experimentally.  what is reported with an 'a' report does increase by Hebbian.
            Actually, ABSOLUTE_USE is just the initial value which becomes SynUSE in the NCS code.
            The USE_New is the running value that is adjusted by facilitation back to the SynUSE setpoint.
            The SynUSE is what is adjusted by Hebbian learning.

        Might make a better demo with fewere A&B Hebbian spikes but with larger effect on each.

    """
    brainname='HebbDemo'
    print "brainname is "+brainname
    #ain=[0.0, .1, .2, .3, .4]
    #bin=[ .5, .6, .7, .8, .9]
    ain=[.1, .2, .3, .4]
    bin=[.6, .7, .8, .9]
    #t=1.5; te=t+1.5; ts=0.05; p=.005   # standard, good demo  RPD20081128: now initial B spikes cause T spikes too.  why?
    #t=1.5; te=t+1.0; ts=0.05; p=.01    # this results in some negative Hebb too
    t=1.5; te=t+1.0; ts=0.30; p=.001
    #t=1.5; te=t+1.5; ts=0.05; p=.001
    while t<te:
        ain.append(t)
        bin.append(t-p)     # p is the offset to ensure Hebbian learning results
        t+=ts
    t+=0.5              # do the testing inputs later for clarity
    te=t+1.0
    while t<te:
        bin.append(t)   # final testing inputs, to see if T spikes with B input alone after Hebbian increased USE
        t+=0.2          # if this is set to .1, T will not spike with a couple of B inputs.  why?  Depression is turned off.

    print "a inputs", ain
    print "b inputs", bin

    endsim=t
    FSV=10000
    timesteps=FSV*endsim

    newb=brainlab.BRAIN({"TYPE": "AREA-BRAIN", "FSV": "10000.00", "JOB": brainname,
                    "SEED": "-99", "DURATION": `endsim`, "OUTPUT_CELLS": "YES",
                    "OUTPUT_CONNECT_MAP": "YES", "DISTANCE": "YES"})

    A=newb.Standard1CellColumn("A")
    B=newb.Standard1CellColumn("B")
    T=newb.Standard1CellColumn("T")

    # may be better way of doing this bit now:
    cs=newb.syntypes["C.strong"]
    cs.parms["LEARN_LABEL"]=newb.sls["BHebb"]
    cs.parms["SFD_LABEL"]=newb.sfds["F0"]       # disable short term facil and depres
    cs.parms["MAX_CONDUCT"]='0.10'

    cs.parms["ABSOLUTE_USE"]='0.5   0.0'
    cs.parms["RSE_INIT"]='0.9   0.9'

    cw=newb.Copy(newb.syntypes, "C.strong", "C.weak")
    cw.parms["ABSOLUTE_USE"]='0.1   0.0'
    cw.parms["MAX_CONDUCT"]='0.05'
    newb.syntypes['C.weak']=cw

    hp=newb.sls["BHebb"]
    # why do extra spikes appear (post NCS r74 or so) on T in timesteps 5000-10000 when
    # only B input is spiking, if POS_HEB_PEAK_DELTA_USE is .10 (instead of .05)?
    # behavior of code must have changed, but the new behavior might be correct.  the T
    # target cell may have been depolarized by the initial A input spikes, making the first
    # B-only input enough to cause spikes.  (But why would an increase in A->T USE cause
    # more depolarization on T if the *same number* of spikes are occurring on T in both
    # POS_HEB_PEAK_DELTA_USE=.1 and POS_HEB_PEAK_DELTA_USE=.05 cases?  isn't a spike a spike?
    # well, spikes may have happened at slightly different times, I guess.
    hp.parms["POS_HEB_PEAK_DELTA_USE"]=".20   0"

    newb.AddConnect(B, T, newb.syntypes["C.weak"], "1.0", "10.0")
    newb.AddConnect(A, T, newb.syntypes["C.strong"], "1.0", "10.0")

    d=(0.0, endsim)
    newb.AddSimpleReport("AReport", A, reptype="v", dur=d)
    newb.AddSimpleReport("BReport", B, reptype="v", dur=d)
    newb.AddSimpleReport("TReport", T, reptype="v", dur=d)

    # note that we are reporting on syanpses coming *into* this cell/cmp, not originating from this cell/cmp
    #newb.AddSimpleReport("TUSE", "T", "T_1CELL", "ER", "SOMA1_name", "a", freq=1, dur=d, synname="C.strong")
    newb.AddSimpleReport("BtoTUSE", T, reptype="a", dur=d, synname="C.weak")
    newb.AddSimpleReport("AtoTUSE", T, reptype="a", dur=d, synname="C.strong")

    newb.AddSpikeTrainPulseStim("Astim", "A", "A_1CELL", "ER", ain)
    newb.AddSpikeTrainPulseStim("Bstim", "B", "B_1CELL", "ER", bin)

    if(1):
        brainlab.Run(newb, verbose=True, nprocs=1)
        #newb.Run(verbose=True, nprocs=1)

    adata=brainlab.LoadSpikeData(brainname, "AReport")
    bdata=brainlab.LoadSpikeData(brainname, "BReport")
    tdata=brainlab.LoadSpikeData(brainname, "TReport")

    #params = {'axes.labelsize': 8,
    #        'text.fontsize': 8,
    #        'legend.fontsize': 8,
    #        'xtick.labelsize': 6,
    #        'ytick.labelsize': 6, }
    #pylab.rcParams.update(params)

    #nextfigure(figsize=(6,6), dpi=600)
    brainlab.nextfigure(figsize=(6,6))
    pylab.rc('ytick', labelsize=8)
    pylab.rc('xtick', labelsize=8)
    pylab.rc('legend', fontsize=10)
    pylab.rc('axes', labelsize=8)
    pylab.rc('legend', pad=.2)
    pylab.rc('legend', labelsep=.05)
    #rc('legend', handletextsep=.01)
    #rc('legend', shadow=True)
    pylab.subplot(3, 1, 1)
    pylab.grid(True)
    print len(adata[0]), len(bdata[0]), len(tdata[0])
    print adata[0], bdata[0], tdata[0]
    if len(adata[0]):
        pylab.scatter(adata[0], len(adata[0])*[15])
    if len(bdata[0]):
        pylab.scatter(bdata[0], len(bdata[0])*[10])
    if len(tdata[0]):
        pylab.scatter(tdata[0], len(tdata[0])*[ 5])
    #xlabel("Timestep")     # share with bottom subplot
    #ax.set_xlim([0.0, stiminterval])
    pylab.ylim(0, 20)
    pylab.xlim(0.0, endsim)
    pylab.yticks([5, 10, 15], ["Cell T", "Cell B", "Cell A"])
    #locs, labels=xticks()
    #xticks(locs, [""]*len(locs))    # we want the tick marks, but not the labels
    pylab.xlabel('Time (s)')
    pylab.title("Spikes")

    pylab.subplot(3, 1, 2)
    pylab.grid(True)
    brainlab.ReportPlot(brainname, "BtoTUSE", plottype=None, plottitle="B synapse on T", xlab="Timestep", ylab="USE", linelab=["B to T"], newfigure=False)
    pylab.xlim(0.0, timesteps)
    pylab.ylim(0.0, 1.0)

    pylab.subplot(3, 1, 3)
    pylab.grid(True)
    brainlab.ReportPlot(brainname, "AtoTUSE", plottype=None, plottitle="A synapse on T", xlab="Timestep", ylab="USE", linelab=["A to T"], newfigure=False)
    brainlab.xlim(0.0, timesteps)
    brainlab.ylim(0.0, 1.0)

    pylab.subplots_adjust(hspace=0.6)
    pylab.savefig('%s-Hebbian.png' % (brainname))
    if showplots: pylab.show()

def TestHebbianMinimal():
    """ simplified version of above for inclusion in paper """

    brainname="HebbTest"    # output files begin with this name
    endsim=3.5              # seconds to simulate
    FSV=10000               # simulation timesteps per second
    timesteps=FSV*endsim

    # set up times (in secs) for two spike inputs, a and b:
    eps=.010
    ain=[.1, .2, .3, 1.5,     1.8,     2.1]
    bin=[.6, .7, .8, 1.5-eps, 1.8-eps, 2.1-eps, 3.1, 3.2, 3.3]

    # create the brain object container:
    #newb=brainlab.BRAIN({"DURATION": `endsim`, "JOB": brainname})
    newb=brainlab.BRAIN(simsecs=endsim, jobname=brainname, fsv=FSV)

    # create three cells in the brain:
    A=newb.Standard1CellColumn("A")
    B=newb.Standard1CellColumn("B")
    T=newb.Standard1CellColumn("T")

    # customize a standard synapse profile:
    cs=newb.syntypes["C.strong"]
    cs.parms["LEARN_LABEL"]=newb.sls["BHebb"]   # BHebb refs a syn profile with pos and neg Hebbian
    cs.parms["MAX_CONDUCT"]=0.10
    cs.parms["ABSOLUTE_USE"]=(0.5, 0.0)         # synaptic efficacy parameter

    # make a copy of this synapse to a new name, then modify it further:
    cw=newb.Copy(newb.syntypes, "C.strong", "C.weak")
    cw.parms["ABSOLUTE_USE"]=(0.1, 0.0)

    # modify a Hebbian learning parameter
    hp=newb.sls["BHebb"]
    hp.parms["POS_HEB_PEAK_DELTA_USE"]=(.20, 0)

    newb.AddConnect(B, T, cw, prob=1.0, speed=10.0)
    newb.AddConnect(A, T, cs, prob=1.0, speed=10.0)

    d=(0.0, endsim)
    # tell NCS to report on some voltage values:
    newb.AddSimpleReport("AReport", A, reptype="v", dur=d)
    newb.AddSimpleReport("BReport", B, reptype="v", dur=d)
    newb.AddSimpleReport("TReport", T, reptype="v", dur=d)

    # tell NCS to report on some absolute USE (synaptic efficacy) values:
    newb.AddSimpleReport("BtoTUSE", T, reptype="a", dur=d, synname=cw)
    newb.AddSimpleReport("AtoTUSE", T, reptype="a", dur=d, synname=cs)

    # tell NCS to input our spikes:
    newb.AddSpikeTrainPulseStim("Astim", A, ain)
    newb.AddSpikeTrainPulseStim("Bstim", B, bin)

    # start the simulation:
    brainlab.Run(newb, verbose=True, nprocs=1)

    # load resulting NCS reports into Python variables:
    adata=brainlab.LoadSpikeData(brainname, "AReport")
    bdata=brainlab.LoadSpikeData(brainname, "BReport")
    tdata=brainlab.LoadSpikeData(brainname, "TReport")

    if 0:
        print "T cell spikes:", tdata
        # plot USE to show Hebbian learning on cell B:
        brainlab.ReportPlot(brainname, "BtoTUSE", plottype=None, plottitle="B synapse on T",
                xlab="Timestep", ylab="USE", linelab=["B to T"], newfigure=False)
        pylab.show()        # display the plot

        sys.exit(0)

    #brainlab.nextfigure(figsize=(6,8))
    brainlab.nextfigure(figsize=(3.3465,5), dpi=900)         # 3.3456 inches = 8.5cm = 85mm which is 1 column http://www.frontiersin.org/authorinstructions/
    pylab.rc('ytick', labelsize=7)
    pylab.rc('xtick', labelsize=7)
    pylab.rc('axes', titlesize=9)
    pylab.rc('legend', fontsize=9)
    pylab.rc('axes', labelsize=8)
    #pylab.rc('legend', pad=.2)
    #pylab.rc('legend', labelsep=.05)
    np=3; pn=1
    pylab.subplot(np, 1, pn); pn+=1
    pylab.grid(True)
    print len(adata[0]), len(bdata[0]), len(tdata[0])
    print adata[0], bdata[0], tdata[0]
    # the 5, 10, 15 is a bit confusing; just an arbitrary y axis scaling for scatter plot
    if len(adata[0]):
        pylab.scatter(adata[0], len(adata[0])*[15])
    if len(bdata[0]):
        pylab.scatter(bdata[0], len(bdata[0])*[10])
    if len(tdata[0]):
        pylab.scatter(tdata[0], len(tdata[0])*[ 5])
    pylab.ylim(0, 20)
    pylab.xlim(0.0, endsim)
    pylab.yticks([5, 10, 15], ["Cell T", "Cell B", "Cell A"])
    #locs, labels=xticks()
    #xticks(locs, [""]*len(locs))    # if we want the tick marks, but not the labels
    pylab.xlabel('Time (s)')
    pylab.title("Spikes")

    pylab.subplot(np, 1, pn); pn+=1
    pylab.grid(True)
    brainlab.ReportPlot(brainname, ["BtoTUSE", "AtoTUSE"], plottitle="Utilization of Synaptic Efficacy",
            xlab="Timestep", ylab="USE", linelab=["B to T", "A to T"], newfigure=False)
    pylab.xlim(0.0, timesteps)
    #pylab.ylim(0.0, 1.0)

    if 0:
        pylab.subplot(np, 1, pn); pn+=1
        pylab.grid(True)
        brainlab.ReportPlot(brainname, "AtoTUSE", plottitle="A to T syn USE", xlab="Timestep", ylab="USE", linelab=["A to T"], newfigure=False)
        pylab.xlim(0.0, timesteps)
        #brainlab.ylim(0.0, 1.0)

    pylab.subplot(np, 1, pn); pn+=1
    pylab.grid(True)
    brainlab.ReportPlot(brainname, "TReport", plottitle="T voltage", xlab="Timestep", ylab="mV", newfigure=False)

    pylab.subplots_adjust(hspace=0.7)
    pylab.savefig('%s-Hebbian.png' % (brainname))
    pylab.savefig('%s-Hebbian.tiff' % (brainname), dpi=900)
    pylab.savefig('Drewes_Figure_1_900dpi.jpg', dpi=900)

def LJExample1():
    pass

def MakeStimSet(ncells, intrvl, ns=8, rseed=None):
    # returns a list of ncells lists of ns stim times
    if rseed!=None: stdrandom.seed(rseed)
    stimset=[]
    st, et=intrvl
    for n in range(0, ncells):
        inp=[]
        for i in range(0, ns):
            r=stdrandom.uniform(st, et)
            inp.append(r)
        inp.sort()
        stimset.append(inp)
    return stimset

def MakeStimSet2(ncells, intrvl, rseed=None, tstp=.1, actcells=3, norepeats=3):
    """
    returns tuple:  (a list of ncells lists of ns stim times,
    list of (indx, time) of sorted spikes)
    this picks 'actcells' cells randomly in each 'stp' interval to fire
    if norepeats!=False, won't have the same cell firing in 'norepeats' consecutive time slots
    """
    if rseed!=None: stdrandom.seed(rseed)
    stimset={}
    allspikes=[]
    st, et=intrvl
    ts=st
    lastpicked=[]
    for i in range(0, ncells): stimset[i]=[]
    while ts < et:
        cls=range(0, ncells)
        if norepeats:
            # we don't want to pick the same cell twice within last nrepeats time steps
            for lastpickedn in lastpicked:
                for pc in lastpickedn:
                    cls.remove(pc)
        stdrandom.shuffle(cls)      # we don't want to pick same cell twice in same time step, so we keep a list
        lastpickedn=[]
        for cc in range(0, actcells):
            celln=cls[cc]
            stimset[celln].append(ts)
            allspikes.append((celln, ts))
            lastpickedn.append(celln)
        ts+=tstp
        lastpicked.append(lastpickedn)
        if len(lastpicked) > norepeats:
            del lastpicked[0]   # remove oldest list
    return (stimset, allspikes)

def ApplyStimSet(brain, inputs, targetcells, timeoffset=0.0):
    ncells=len(inputs)
    for n in range(0, ncells):
        i=inputs[n]
        offseti=[]
        for t in i:
            offseti.append(t+timeoffset)
        if len(offseti) > 0:
            brain.AddSpikeStim(targetcells[n], offseti)
            #print "ApplyStimSet cell %s time %s" % (targetcells[n], offseti)

def MakeTRBrain(brainname='bbb', ncells=10, numsyns=4, tstep=.05, d=(0, 1.0), douserep=False, docurrrep=False, edelay=False, phw=.02, celldelay=0.0, csuse=0.5, nochannels=False, pincmp=False, depr=False, phpt=None):
    """
        If pincmp==True, eliminate the std devs in compartment properties to reduce variation
    """
    if phpt==None:  phpt=phw/2.0
    xxx, endsim=d
    cells={}
    ain={}; bin={}; reps={}; inputs={}; usereps={}; inareps={}; inbreps={}; curreps={}

    newb=BRAIN({"TYPE": "AREA-BRAIN", "FSV": "10000.00", "JOB": brainname,
                "SEED": "-9934", "DURATION": `endsim`, "OUTPUT_CELLS": "YES",
                "OUTPUT_CONNECT_MAP": "YES", "DISTANCE": "YES"})

    for n in range(0, ncells):
        cells[n]=newb.Standard1CellColumn('cell%d'%n)
        ain[n]=newb.Standard1CellColumn('ain%d'%n)
        bin[n]=newb.Standard1CellColumn('bin%d'%n)
        reps[n]=newb.AddSimpleReport('rep%s'%n, cells[n], reptype="v", dur=d)
        if douserep:
            for de in range(1, numsyns+1):
                #usereps[n]=newb.AddSimpleReport('userep%s'%n, cells[n], reptype="a", dur=d, synname='C.strong')
                usereps[n]=newb.AddSimpleReport('userep%d-%s'%(de, n), cells[n], reptype="a", dur=d, synname='C.strongE%d' % de, freq=20)
                #usereps[n]=newb.AddSimpleReport('userep3-%s'%n, cells[n], reptype="a", dur=d, synname='C.strongE3')
        inareps[n]=newb.AddSimpleReport('inarep%s'%n, ain[n], reptype="v", dur=d)
        inbreps[n]=newb.AddSimpleReport('inbrep%s'%n, bin[n], reptype="v", dur=d)
        if docurrrep:
            cps=docurrrep; cpe=21.0
            #cps=4.9
            #cpe=5.2
            #cps=(1.0+.2*4.0)
            #cpe=cps+.15
            #curreps[n]=newb.AddSimpleReport('crep%s'%n, cells[n], reptype='c', dur=(20, 20.150))
            curreps[n]=newb.AddSimpleReport('crep%s'%n, cells[n], reptype='c', dur=(cps, cpe))

    if nochannels:
        cmp=newb.comptypes['SOMA1']
        cmp.parms['CHANNEL']=[]

    if pincmp:
        cmp=newb.comptypes['SOMA1']
        print "REMOVING STDDEV FROM COMPARTMENT PARAMETERS!"
        cmp.parms['TAU_MEMBRANE']='%f %f' % (0.015, 0.0)
        cmp.parms['R_MEMBRANE']='%f %f' % (200.0, 0.0)
        cmp.parms['THRESHOLD']='%f %f' % (-40.0, 0.0)
        cmp.parms['VMREST']='%f %f' % (-60.0, 0.0)
        cmp.parms['CA_SPIKE_INCREMENT']='%f %f' % (300.0, 0.0)
        cmp.parms['CA_TAU']='%f %f' % (0.07, 0.0)

    syndelay=tstep
    #syndelay=.025
    eps=.0005
    cs=newb.syntypes['C.strong']
    if depr:
        cs.parms['SFD_LABEL']=newb.sfds['F1']
        sf1=newb.sfds['F1']
        sf1.parms['SFD']='DEPR'
        sf1.parms['DEPR_TAU']='%f %f' % (.010, 0.0)
        del sf1.parms['FACIL_TAU']
    else:
        cs.parms['SFD_LABEL']=newb.sfds['F0']        # turn off short term facilitation and depression
    #cs.parms['SFD_LABEL']=newb.sfds['F1']        # turn off short term facilitation and depression
    cs.parms["LEARN_LABEL"]=newb.sls["BHebb"]
    #cs.parms["LEARN_LABEL"]=newb.sls["0Hebb"]
    #cs.parms["MAX_CONDUCT"]='0.012'
    #cs.parms["MAX_CONDUCT"]='0.015'
    cs.parms["MAX_CONDUCT"]='0.022'
    # want delay (min, max) to be about the time between input steps if we want the outputs in
    # this step to contribute to next step's inputs.  note that DISTANCE is disabled above, but
    # DELAY is a different delay than that arising from DISTANCE factors which are based on
    # location calculations.
    # (actually, that applies to the recurrent syns, but for simplicity make the input->target syns very low delay
    #cs.parms["DELAY"]='%f %f' % (eps, 2*eps)      # min, max
    cs.parms["DELAY"]='%f %f' % (0.0, eps/5.0)      # min, max
    cs.parms["ABSOLUTE_USE"]='%f   0.0' % csuse
    cs.parms["RSE_INIT"]='1.0   1.0'
    cs.parms["RSE_INIT"]='1.0   1.0'
    cs.parms["PREV_SPIKE_RANGE"]="0.0 0.0"
    cs.parms["SYN_REVERSAL"]="0.0 0.0"      # eliminate variability, set stdev=0.0

    sl=newb.sls['BHebb']
    #ph=.01; nh=.01
    ph=.20; nh=ph
    nhw=phw
    sl.parms["POS_HEB_PEAK_DELTA_USE"]='%f   0.0' % ph
    sl.parms["POS_HEB_WINDOW"]=        '%f   0.0' % phw
    sl.parms["POS_HEB_PEAK_TIME"]=     '%f   0.0' % phpt

    sl.parms["NEG_HEB_PEAK_DELTA_USE"]='%f   0.0' % nh
    sl.parms["NEG_HEB_WINDOW"]=        '%f   0.0' % nhw
    sl.parms["NEG_HEB_PEAK_TIME"]=     '%f   0.0' % (nhw/2)

    # a set of synapses with defined delays
    ced={}
    cid={}
    for d in range(1, numsyns+1):
        ced[d]=newb.Copy(newb.syntypes, "C.strong", "C.strongE%d"%d)
        # this delay was decreased because delayed spikes were arriving *after* the training input spikes and
        # no hebbian was happening
        #ced[d].parms["DELAY"]='%f %f' % (syndelay*d - 2*eps, syndelay*d - 0.0)      # min, max
        if edelay is not False:
            ced[d].parms["DELAY"]='%f %f' % (syndelay*d - edelay*2 - celldelay, syndelay*d - edelay - celldelay)      # min, max
        else:
            ced[d].parms["DELAY"]='%f %f' % (syndelay*d - 15*eps - celldelay, syndelay*d - 14*eps - celldelay)      # min, max

        cid[d]=newb.Copy(newb.syntypes, "C.strong", "C.strongI%d"%d)
        # no Hebbian on inhibitory syns
        cid[d].parms["LEARN_LABEL"]=newb.sls['0Hebb']
        cid[d].parms["DELAY"]='%f %f' % (syndelay*d - 2*eps, syndelay*d - 0.0)      # min, max
        #cid[d].parms["SYN_REVERSAL"]="-90.0 2.0"
        cid[d].parms["SYN_REVERSAL"]="-90.0 0.0"        # stdev=0.0 for no variability
        cid[d].parms["SYN_PSG"]=newb.spsgs["PSGinhib"]

    # a single synapse with a highly variable delay
    csv=newb.Copy(newb.syntypes, "C.strong", "C.strongv")
    csv.parms["DELAY"]='%f %f' % (syndelay*1.0 - 0.0, syndelay*4.0 - 2*eps)      # min, max

    #inpa=MakeStimSet(ncells, (0, 0.8), ns=8, rseed=23)
    #inpb=MakeStimSet(ncells, (0, 0.8), ns=5, rseed=34)
    ###inpa, aspk=MakeStimSet2(ncells, (0, 0.8), rseed=26, tstp=tstep, actcells=4)
    ###inpb, aspk=MakeStimSet2(ncells, (0, 0.8), rseed=38, tstp=tstep, actcells=4)
    #print "inpa:", inpa
    #print "inpb:", inpb
    #sys.exit(0)

    return newb, cells, ain, bin, cs, ced, cid, sl

fontbig = {'family'     : 'sans-serif',
        'color'      : 'k',
        'weight' : 'bold',
        'size'   : 14,
        }

def TestRecurrentMemoryPlot3(savefn, plotdate, vlin, ncells, data, inputspikes, inputs, partialinputs, numinputs, inputlength, tstep, plotinput=True, plotoutput=True):
    print "generating plot3"
    spn=0
    nextfigure(figsize=(7.0, 9.0))
    nsp=len(vlin)
    for (x, c, ttl, vts, vte) in vlin:
        subplot(nsp, 1, spn+1)
        if spn==0: title("Internal cells activity")
        for pn in range(0, ncells):
            dd=data[pn]
            # dd is just a list with one element, dd[0].  dd[0] is just a list of spike times
            # we make a list of y coords that is just the cell number repeated once for each spike time
            # we are plotting way more data than we need and then trimming the axes down.
            # Maybe faster to just limit the scatter to the data of interest?
            # (now we do restrict the range to what is actually displayed).  this also allows us to skip
            # tetanic spiking
            pdd=dd[0]
            pdd=[pde for pde in pdd if pde>=vts-.1 and pde<=vte]       # narrow range
            #print "vts %f vte %f len pdd %d" % (vts, vte, len(pdd))
            if len(pdd) > 100:
                print "skipping huge plot on plot3, cell %d" % pn
            else:
                if len(pdd) and plotoutput:
                    #scatter(pdd, len(pdd)*[pn])
                    scatter(pdd, len(pdd)*[pn], color='b', marker='o', alpha=0.2)               ### BLUE semi-transparent circles for actual resulting spike output
        # these are the little red + symbols that show the original input signal
        if plotinput:
            if c=='r':      # full input, training, use inputs[]
                ax=gca()
                text(.05, .5, "A"+ttl, fontbig, transform = ax.transAxes)
                thisinput=inputs[int(ttl)]
                for cn in thisinput.keys():
                    for tt in thisinput[cn]:
                        plot([vts+tt], [cn], 'r+')                                              ### RED + for actually applied inputs
            elif c=='b':    # partial input, test, use partialinputs[]
                ax=gca()
                text(.05, .5, "B"+ttl, fontbig, transform = ax.transAxes)
                thisinput=inputs[int(ttl)]
                thisprtlinput=partialinputs[int(ttl)]
                for cn in thisinput.keys():
                    #print "cell", cn
                    #print "fullinput", thisinput[cn]
                    #print "prtlinput", thisprtlinput[cn]
                    for tt in thisinput[cn]:
                        if tt not in thisprtlinput[cn]:
                            plot([vts+tt], [cn], 'kx')                                              ### BLACK x for what the missing inputs, not applied
                        else:
                            plot([vts+tt], [cn], 'r+')                                              ### RED + for the *actually applied* partial inputs
                #thisinput=partialinputs[int(ttl)]
                #for cn in thisinput.keys():
                #    for tt in thisinput[cn]:
                #        plot([vts+tt], [cn], 'k+')                                              ### BLACK + for the actually applied inputs
        if False:  # old way of plotting + markers
            #ttl is input number, but as a string, so have to convert to int
            thisinput=inputspikes[int(ttl)]
            #print "inputspikes for", ttl, ":", thisinput
            for (celno, spktim) in thisinput:
                #print "inputsignals:  celno, vts, spktim", celno, vts, spktim
                plot([vts+spktim], [celno], 'r+')
            #print "plotted along with ", dd[0]
            thisinput=partialinputs[int(ttl)]
            print "partial inputs for", ttl, ":", thisinput
            for (celno, spktim) in thisinput:
                #print "inputsignals:  celno, vts, spktim", celno, vts, spktim
                plot([vts+spktim], [celno], 'b+')
        # these are the little blue + symbols that show the ACTUAL input spikes applied, which during training is
        # the same as the input pattern, but in the test inputs, will only be *part* of the original input pattern
        #print partialinputs
        #sys.exit(0)
        #ax=gca()
        #text(.5, .5, ttl, transform = ax.transAxes)
        #text(.05, .5, ttl, fontbig, transform = ax.transAxes)
        #xlim((vts-.1, vte))
        #ylim((-.05, ncells-1+.05))
        spn+=1
        # fixup yticks to only show 5, 10, 15, ... ncells-5
        #ti,tl=yticks()
        #ntl=[]
        #for f in ti:
        #    if int(f) > 0 and int(f) % 5 == 0 and int(f) % 10 != 0:
        #        nl='%d' % int(f)
        #    else:
        #        nl=''
        #    ntl.append(nl)
        #yticks(ti, ntl)
        # fixup xticks by losing the leftmost time
        #ti,tl=xticks()
        #ntl=[]
        #ntl.append('')
        #for f in ti[1:]:
        #    ntl.append('%.2f' % float(f))
        #xticks(ti, ntl)
        xticks(arange(vts, vts+(inputlength * tstep + tstep)-.01, tstep))
        yticks(arange(5, ncells, 5))
        # if you do the xticks after the xlim, the xlim gets messed up!  so do the xlim last
        xlim((vts-.05, vts+(inputlength * tstep + tstep)))
        ylim((0, ncells-1+1))
    if spn==nsp:
        xlabel("Time (s)")
        ylabel("Cell #")
    subplots_adjust(bottom=0.05, right=0.95, top=0.96, left=0.07)
    savefig(plotdate+savefn)


def TestRecurrentMemory(dorun=True, doplot=True):
    """
        Call with dorun=False, doplot=True to replot last data set.
            NOTE!  the seed used to generate input patterns had better be the same, otherwise the
            input patterns plotted will disagree with the saved data files!

        A simple array n cells wide.  Output of each cell synapses on input of all other cells.
        We force a set of n cells in the array to spike in a pattern for t seconds

        What are we looking at as output?  The cell array spiking in response to two patterns input.

        At what size (width) does this work best (remember most)?

        Do outputs resemble inputs?

        Can we learn to remember two sequences, to correlate them?  So that presentation of one sequence
        alone will allow recall of the other, or recall of learned output sequence?

        Introduce variable delay in synapse propagation time . . . do things break down?

        Introduce facil and depres . . . do things break down?

        Role of inhib?  Will the thing work at all with no inhib?  will output cells get overdriven with
        two input signals?

        ISSUE:  want to apply spikes, not force cell to spike . . . if inputs pulse always causes
        a spike we really want to apply it to a cell that is connected to input

        Idea is to gradually add complexity to the system to add "features" (thalamic gating?  additional
        context selection?) 

        IDEA:  fundamental aspect of an organism is to 'know' that this situation has occurred before
        be able to discriminate different stimulus situations

        FIXME:  put all cells in one column so we can get a report on all with one report request?

        WACKYIDEA:  could the greater intelligence of humans be 'the width of the bus' (number of cells
        wide a representation/message is)

        ISSUE:  the t+1 delayed PSPs were arriving just a bit after the cells were being forced to spike,
        therefore poshebb was not happening.  Delay was increased.

        TestRecurrentMemory1:
        On some runs, initial few spike inputs cause tetanic spiking for first second or so,
        but then we get a very sparse pattern of outputs.
        On other runs, there is no initial tetanic response.
        Tried to arrange MAX_CONDUCT so that a single spike won't be enough to get an output;
        otherwise, network goes berserk.
        What causes initial tetanic response to subside?  Presumably, negative Hebbian learning
        reducing enough USE values.  Try disabling Neg Hebbian and see if things never go berserk.
        Occasionally, burst of tetanus occurs in middle of run.
        If Hebbian is changed from B(oth) to 0(None), when tetanus starts it never stops!
        Need some test of reproducibility, whether multiple patterns can be remembered and re-triggered.
        Increasing MAX_CONDUCT from .01 to .015 makes tetanus occur initially almost all the time.
        Question:  if MAX_CONDUCT were increased much higher, would it just take *longer* for Neg Hebb
        to shut down tetanus?  Do I need to extend runs?
        So far, so good!
        Actually, the input spikes were in the interval 0,8.0 . . . when it is reduced, the spikes
        aren't sustained for long after inputs stop (activity isn't self sustaining)

        WACKYIDEA:  does a certain minimum amount of firing have to happen in order for a sequence to
        be remembered (context).  minimum 'spike density' to sustain

        WACKYIDEA:  for empirical investigation
        in STDP (Hebbian, Spike Timing Dependent Plasticity), will the USE adjustment go up
        more for a set of synapses if there are multiple input spikes contributing to an 
        output spike than for a single synapse input that causes an output spike?

        OBSERVATION:  enabling short term facil and depres helps prevent tetanic response, which
        of course makes sense.  With facil and depres enabled, the USE curves show steady
        increase or decrease typically.  Without facil and depres, the USE curves swing
        wildly up and down, at least for a time.

        Do we need a bunch of synapses with different delays (like in Polychronization paper)
        to keep sequence going?
        Variable synapse delays could make things interesting, lead to interesting patterns.

        Self triggering sequences, as opposed to a two-input memory/recall/association
        Is a sequence triggered by a set of spikes with width but no time extent?

        Coincidence detection:  seems fairly easy

        THINK:  if an output target cell connects back to input of all cells, then that
        is dumb and uninteresting because it is not selective, it will contribute to
        all inputs in next cycle.  (Unless some of those synapses have been turned down
        with neghebbian)

        What could 'sensitize' a cell, depolarize it a bit . . .

        A single input on A probably won't cause any output spikes.  Thus there won't be any
        output->feedbackinput spikes to keep things going.  This makes it hard to do a
        straight "self triggering sequence" test, since there is no output from a single
        input.
        Gain has to be < 1 otherwise skiping will just go nuts.

        WACKYIDEA:  STDP as identification of causality
        things were like *this* (sensory input) just before *this* other thing
        (action? other sensory state)
        they then become correlated

        Where does Hawkins write about two cells firing together, each synapse strengthens
        so that later on either one can invoke same output separately?

        NOTE:  By having synaptic delays in steps, we really limit the potential flexibility of
        the network, but might make things more comprehensible.

        IDEA:  a network that recognizes novel signals.  first time signals are blocked.
        you have to see the signal a couple of times before it is passed through . . .

        IDEA:  is communication in brain with spikes or spike trains where timing is significant
        or wide spike trains where timing is significant or ???
        I think communication in the brain would look like what comes in from senses:
        (and what do those signals look like)?
        auditory:
        vidual:
        smell:
        taste:
        touch:
        propri:

        IDEA:
        inhibatory cells used to renormalize, otherwise cells just keep getting potentiated
        NO, duh, inhib spikes don't reduce Hebb learning, neg hebb does that!

        IDEA:
        fundamental unit of processing in the brain:  have I seen this signal before?
        have I seen this signal at the same time as this signal?

    """

    inadata={}; inbdata={}
    data={}
    recurrconnecttype=1    # pattern of recurrent connects
    docurrrep=9.0        # do current reports (useful to see timing of delayed PSC)
    douserep=False
    partialinputmethod=None

    #ni=5
    #ivl=4
    vlin=[]

    # this is an early, working experiment with two inputs where the pattern is stored in a single
    # trial, using very strong +hebb on initially 0 strength synapses, thereafter a single spike
    # on both inputs can recall joint pattern, or two spikes on on input can recall joint pattern
    # from that point on
    # Exp 1 {{{
    if False:
        ncells=10
        numsyns=4
        tstep=.05
        endsim=38.0
        d=(0.0, endsim)
        brainname='RecurrentMemory'
        newb, cells, ain, bin, cs, ced, cid, sl=MakeTRBrain(brainname=brainname, ncells=ncells, numsyns=numsyns, tstep=tstep, d=d, douserep=douserep, docurrrep=docurrrep, phpt=None)
        """
            THIS WORKS GREAT AND SHOULD BE WRITTEN UP
                after training, first spike of *both* trained input reproduces full stored spike pattern.
                also first *two* spikes of *one* trained input reproduced full stored spike pattern
                remaining issues:
                    a. double (triple or quadruple!) spikes on outputs when network is partially
                        trained and input is presented.
                        but first spike on its own still may not evoke pattern!  maybe first *two* spikes would!
                        fix with inhib neurons?
                    b. each neuron can only evoke one trained spike train.  neurons can't be reused, in other words,
                        in multiple sequences.  plan to fix this in next experiment.
                    c.  neg hebbian is disabled.  double spikes seem to confound learning by introducing neg hebb.
                    d.  the first spike of some patterns does evoke remainder of pattern.  but others don't.  why?
                        see if first *two* spikes does work!
            YAY!  with stim rseed 2569956, you need first *two* spikes to evoke the stored pattern!  this means that
                already, a single spike could be part of multiple stored patterns, and you need a couple of spikes to
                access the stored pattern!
                  with stim rseed 25656, the very first spike evokes the stored pattern (hopefully didn't change other parms?)
            #
            protocol:
            first test of the time delay recurrent memory
            each cell connects to each other with a syn of each delay
                these syns should require > 1 spike to evoke spike on target
                so only if two signals of *different* delays arrive at target at same time
                will a spike output occur
                issue:  will there be too many coincidences/hits?  only want to look at preceding time step,
                since each input will cause PSC on each target for t+1*tstep, t+2*tstep, ... t+maxrecurdelay*tstep
                    so set maxrecurdelay=1 to only allow contribution from preceding time step
            after training with a pattern, application of first input spike
            should evoke the same pattern that was stored (complete the pattern evocation)
            this is sort of interesting, but inflexible:  *any* subsequent activation of any cell in the
                sequence will evoke stored pattern at that point in the pattern
            need some way of storing the 'context' of a pattern to uniquely evoke it.  thinking about this,
                but wanted to test this basic thing first
            Each applied spike results in ncells recurrent spikes, but since USE is low initially, none of those
                syns can cause an output spike on target at time + delay unless the training sequence is also
                received.  When that is the case, that syn will be strengthened enough so that it can eventually cause fire
                on its own (this is in the case where an input sequence has only one cell firing per time step;
                for 2-cell-firing-per-timestep, will have to adjust . . .
            In single input test, saw Hebbian learning as expected.  After learning reached a threshold, double
                spikes on target started appearing after first spike (when *entire* original sequence was
                applied)!  good.  one spike was from the input, another as a result of delay from last spike in
                sequence that was applied.  next confirm that the single input spike will start the chain!
            #
            NOTE:  the 'double spike' phenomenon causes some neg hebb
                Ah, disabling input->target hebbian helps things.  those syns go into overdrive and cause tetanus
                WACKYIDEA:  inhibitory syns prevent double spikes during input sequence application when network
                    already trained
                WACKYIDEA:  if a dual sequence is being evoked from one of the inputs, could the outputs coming from
                    the *other* input be selected for by using inhib cells to suppress the outputs of the evoking
                    input?  in other words, could one input evoke only the output of the *other* input?
            #
            how does connect 'speed parameter' interact with 'delay' parameter?
            #
            ISSUE:  once a syn becomes potentiated, it acts any time the source cell spikes . . .
        """
        recurrconnecttype=3
        maxrecurdelay=2
        inpb=None; bspk=None
        recurmaxcond='0.020'
        absuse='0.0    0.0'
        if False:
            # the first spike is not enough to evoke a full output, but the first two spikes together 
            # are enough to evoke full output
            ph=.40
            inpa, aspk=MakeStimSet2(ncells, (0, tstep*4), rseed=25656, tstp=tstep, actcells=1)
        if False:
            # here, with stronger pos hebbian, the first spike only is enough to evoke
            # the first 3 output spikes in the stored sequence.
            # later, in the bottom two plots of the splitout plot, the first two spikes together are enough to 
            # evoke the full output sequence
            ph=.50
            inpa, aspk=MakeStimSet2(ncells, (0, tstep*4), rseed=25656, tstp=tstep, actcells=1)
        if False:
            # revalidated with new proper syn delays and no hebbian on input->target syns
            # first spike of input does not evoke full output, first two spikes do evoke full output
            #ph=.80
            ph=.2
            cs.parms["LEARN_LABEL"]=newb.sls["0Hebb"]       # no hebb on input->target cells
            inpa, aspk=MakeStimSet2(ncells, (0, tstep*4), rseed=2569956, tstp=tstep, actcells=1)
        if True:
            # trained with two inputs; output is same as input sequences superposed, can we then
            # evoke the combined output from a partial single input?  partial dual inputs?
            # complete single inputs?
            # partial (2 spike) single input (hard to get this working so far; does not evoke entire stored sequence)
            # partial (2 spike) dual input (hard to get this working so far; evokes only the one output trained with that input)
            #   why?  something is wrong.  the syns from spikes of *either* input should get +hebb potentiated
            #ph=.20
            ph=2.0
            #recurmaxcond='0.01'        # close to working!  single spike from a+b evokes output, then things go tetanic
            recurmaxcond='0.008'        # same as above
            recurmaxcond='0.006'       # works well but missing one spike at end of one test input
            recurmaxcond='0.0065'       # works OK on the last two test inputs, first one (1 spike from and and b each) get repitition
            recurmaxcond='0.00625'    # works! to evoke stored outputs
            absuse='0.0    0.0'
            inpa, aspk=MakeStimSet2(ncells, (0, tstep*4), rseed=656, tstp=tstep, actcells=1)
            inpb, bspk=MakeStimSet2(ncells, (0, tstep*4), rseed=1596, tstp=tstep, actcells=1)
            #dualtest=2      # after training, test stims will do entire a input only, then entire b input only
            #dualtest=1      # after training, stims will do first spike of a and b input, then first 2 spikes of a and b input
            dualtest=3
            cs.parms["LEARN_LABEL"]=newb.sls["0Hebb"]       # no hebb on input->target cells
        print inpa
        print inpb
        # find the first spike applied, and first and second spike applied:
        inpa1spike={}
        inpa2spike={}
        inpb1spike={}
        inpb2spike={}
        for d in range(0, ncells):
            inpa1spike[d]=[]
            inpa2spike[d]=[]
            inpb1spike[d]=[]
            inpb2spike[d]=[]
        celno, spktm=aspk[0]
        inpa1spike[celno].append(spktm)
        inpa2spike[celno].append(spktm)
        celno, spktm=aspk[1]
        inpa2spike[celno].append(spktm)
        if inpb:
            celno, spktm=bspk[0]
            inpb1spike[celno].append(spktm)
            inpb2spike[celno].append(spktm)
            celno, spktm=bspk[1]
            inpb2spike[celno].append(spktm)

        print "inpa with only first spike is:"
        print inpa1spike
        #sys.exit(0)
        sl.parms["POS_HEB_PEAK_DELTA_USE"]='%f   0.0' % ph
        # scale up input cells so single input pulse will cause target spike
        # (the recurrent connections use the ced[] cells with synapses with lower conductance):
        cs.parms["MAX_CONDUCT"]='0.035'         # at .030, sometimes cells don't fire reliably
        # start all cells in low activity
        nh=0.0       # disable neghebb because of double-spike issue
        sl.parms["NEG_HEB_PEAK_DELTA_USE"]='%f   0.0' % nh
        for d in range(1, numsyns+1):       # disable Hebbian
            #ced[d].parms["LEARN_LABEL"]=newb.sls["0Hebb"]
            ced[d].parms["MAX_CONDUCT"]=recurmaxcond
            ced[d].parms["ABSOLUTE_USE"]=absuse
        pd=1.0
        if False:       # pre stim with each input individually
            t=0.0
            ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
            vlin.append((t,   'r', 'a', t, t+pd))
            t=1.0
            ApplyStimSet(newb, inpb, bin, timeoffset=float(t))
            vlin.append((t,   'r', 'b', t, t+pd))
        if False:       # pre stim with each input individually
            t=2.0
            ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
            vlin.append((t,   'r', 'a', t, t+pd))
            t=3.0
            ApplyStimSet(newb, inpb, bin, timeoffset=float(t))
            vlin.append((t,   'r', 'b', t, t+pd))
        for t in range(4, 8, 4):
            ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
            if inpb:
                ApplyStimSet(newb, inpb, bin, timeoffset=float(t))
            vlin.append((t,   'r', 'a + b', t, t+pd))
        for t in range(24, 28, 4):
            if inpb:
                if dualtest==2:
                    #ApplyStimSet(newb, inpb1spike, bin, timeoffset=float(t))
                    ApplyStimSet(newb, inpb, bin, timeoffset=float(t))
                    vlin.append((t,   'b', 'inpb only', t, t+pd))
                elif dualtest==1:
                    ApplyStimSet(newb, inpa1spike, ain, timeoffset=float(t))
                    ApplyStimSet(newb, inpb1spike, bin, timeoffset=float(t))
                    vlin.append((t,   'b', 'both inputs, 1 spike only', t, t+pd))
                elif dualtest==3:
                    # 'spatial specificity':  two cells active at one time
                    ApplyStimSet(newb, inpa1spike, ain, timeoffset=float(t))
                    ApplyStimSet(newb, inpb1spike, bin, timeoffset=float(t))
                    vlin.append((t,   'b', 'both inputs, 1 spike only', t, t+pd))
                    t+=1.0
                    # 'temporal specificity':  two spikes of one sequence
                    ApplyStimSet(newb, inpa2spike, ain, timeoffset=float(t))
                    vlin.append((t,   'b', 'a input, 2 spikes only', t, t+pd))
                    t+=1.0
                    # 'temporal specificity':  two spikes of one sequence
                    ApplyStimSet(newb, inpb2spike, bin, timeoffset=float(t))
                    vlin.append((t,   'b', 'b input, 2 spikes only', t, t+pd))
                    t+=1.0
                    # this single spike should not evoke any outputs because it is not 'specific' enough
                    ApplyStimSet(newb, inpa1spike, ain, timeoffset=float(t))
                    vlin.append((t,   'b', 'a input, 1 spike only', t, t+pd))
            else:
                ApplyStimSet(newb, inpa1spike, ain, timeoffset=float(t))
                vlin.append((t,   'b', 'inpa1spike', t, t+pd))
        for t in range(32, 40, 4):
            if inpb:
                if dualtest==2:
                    #ApplyStimSet(newb, inpb2spike, bin, timeoffset=float(t))
                    ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
                    vlin.append((t,   'b', 'inpa only', t, t+pd))
                elif dualtest==1:
                    ApplyStimSet(newb, inpa2spike, ain, timeoffset=float(t))
                    ApplyStimSet(newb, inpb2spike, bin, timeoffset=float(t))
                    vlin.append((t,   'b', 'both inputs, 2 spikes only', t, t+pd))
                elif dualtest==3:
                    pass
            else:
                ApplyStimSet(newb, inpa2spike, ain, timeoffset=float(t))
                vlin.append((t,   'b', 'inpa2spike', t, t+pd))
    #}}}

    # see how to make things robust, prevent tetanus
    # what is memory capacity
    # allow flexible tests with variable width inputs, variable number of cells, variable number of syn delays
    # possibly later test sparseness of recurrent connections
    # Exp 1.5 {{{
    if True:
        """
            There seems to be about a 5ms delay between time spike is applied to input neuron, input neuron spikes, and
            target is forced to spike.  This even though the cs.strong delay is only 0.5 - 1.0 ms.  Probably due to channels ramping
            up.
            NOTE:  it seems important for the input patterns not to have repeats in cells too close together, presumably because that
            doesn't give cells time to recover (it seemed like when a cell failed to fire it had been used recently in the pattern)
            NOTE:  it would be good to make sure input patterns have different initial pairs of cells firing
        """
        endsim=30.0
        teststart=20.0  # when to start applying test patterns (partial inputs)
        trainings=1     # how many times to present each input pattern
        numspikespartial=4
        inputlength=9
        ncells=20
        numinputs=5        # this is really the number of distinct test input *patterns*
        tstep=.030          # how far apart spike intervals in input pattern will be
        phw=tstep/3
        #phpt=phw/2.0
        phpt=phw/3.0        # this should place the peak closer than half way to coincidence 
        #usechan, inputwidth, numsyns, recurmaxcond, recurrconnecttype = (True, 1, 3, '0.00400', 3)       # single spike test
        #usechan, inputwidth, numsyns, recurmaxcond, recurrconnecttype = (True, 2, 4, '0.00165', 3)       # pretty good 2-wide spike test
        #NOTE:  increasing numsyns while using recurrconnecttype==4 does not increase the inter-temporal connectivity, it just *spreads* it out!
        # increasing input width *would* increase inter-temporal connectivity . . . 
        #MAYBE it is easier to recall spatially rather than temporally (with 'half an idea' for an entire duration, rather than the first half of the whole
        # thing
        # works well.  one or so extra spikes.
        # numsyns:  number of back spikes that contribute forward (was 6, now 4)
        # nrecurr:  in recurrconnecttype==4, nrecurr is the number of connections each internal cell makes back to EVERY other internal cell.
        #       these connections are randomly selected from range of delays 1..numsyns.  thus nrecurr must be <=numsyns
        #       each cell connects to nrecurr/ncells targets.  this should probably scale up with ncells, be some reasonable fraction of it.
        #ncells=40; numinputs=4; usechan=True; inputwidth=2; inputlength=10; numsyns=4; recurmaxcond='0.00310'; recurrconnecttype=4; nrecurr=3; numspikespartial=3; phw=tstep/3.0       # missing many spikes

        # GOOD runs for research proposal:
        ##partialinputmethod='time'; ncells=40; numinputs=4; usechan=True; inputwidth=2; inputlength=10; numsyns=3; recurmaxcond='0.00270'; recurrconnecttype=4; nrecurr=3; numspikespartial=3; phw=tstep/3.0   # GREAT!  only a few extra spikes  could probably get rid of those with a bit of tweaking
        # issue with partial space method, is that you need x cells in past to trigger spike, but once the pattern gets recalled on two cells per time step, you will get
        # 2*x cells contributing to later spikes.  These paramaters work pretty well:
        ##partialinputmethod='space'; ncells=40; numinputs=4; usechan=True; inputwidth=2; inputlength=10; numsyns=5; recurmaxcond='0.00220'; recurrconnecttype=4; nrecurr=5; numspikespartial=1; phw=tstep/3.0

        # testing, with reduced number of cells to enhance visibility
        #partialinputmethod='space'; ncells=30; numinputs=4; usechan=True; inputwidth=2; inputlength=12; numsyns=5; recurmaxcond='0.00210'; recurrconnecttype=4; nrecurr=5; numspikespartialW=1; numspikespartialL=7; phw=tstep/3.0; endsim=16.0; teststart=8.0    # .00220, .00210 tetanic (with 20 cells), 
        partialinputmethod='time'; ncells=20; numinputs=4; usechan=True; inputwidth=2; inputlength=10; numsyns=5; recurmaxcond='0.00190'; recurrconnecttype=4; nrecurr=5; numspikespartial=3; phw=tstep/3.0; endsim=16.0; teststart=8.0

        # END research proposal runs

        # (40, 4, True, 2, 10, 4, '0.00310', 4, 3, 3, tstep/3.0)
        # works pretty well. quite a few missing spikes with 3 out of 6 recurrence ncells, numinputs, usechan, inputwidth, inputlength, numsyns, recurmaxcond, recurrconnecttype, nrecurr, numspikespartial, phw = (60, 16, True, 2, 10, 6, '0.00250', 4, 3, 5, tstep/3.0)
        #ncells, numinputs, usechan, inputwidth, inputlength, numsyns, recurmaxcond, recurrconnecttype, nrecurr, numspikespartial, phw = (60, 16, True, 3, 10, 6, '0.00350', 4, 1, 5, tstep/3.0)
        inpb=None; bspk=None
        douserep=True
        #csuse=0.5
        # adjust inptotargetdelay to get the red + marks to correspond to the forced spikes on the target cells
        # adjust recurdelay to get the delayed 'confluence' spikes to coincide with the forced spikes from input->target
        if usechan:
            inptotargetdelay=.005       # approximate delay for a cell to spike, *not counting* synaptic delay (channel charging etc.)
                # increasing inpttotargetdelay to .005 from .004, with recurdel at 0.0, has interesting effects.  better than increasing
                # recurdelay.  but .006 seems not as good as .005
            recurdelay=-.0015         # increasing this moves spikes to *left*!  making it negative will move to right.
            #recurmaxcond='0.00180'      # good value WITH channels
            #recurmaxcond='0.00250'      # too much
            #recurmaxcond='0.00210'      # a bit too little for numsyns==3
            #recurmaxcond='0.00205'      # 
            #recurmaxcond='0.00400'      #
            csuse=.485       # inp->target syn strength.  can test with recur disabled to make sure get 1 spike exactly
        else:
            inptotargetdelay=.004       # approximate delay for a cell to spike, *not counting* synaptic delay (channel charging etc.)
            recurdelay=.004
            recurmaxcond='0.00113'      # good value with NO channels
            csuse=.25       # inp->target syn strength.  a good value if channels are disabled; retest with recur disabled if channels are reenabled to make sure don't get multiple spikes on target
        #endsim=float(3 * numinputs)
        d=(0.0, endsim)
        brainname='RecurrentMemory'
        eps=.0001
        #phw=tstep/2
        recurofftest=False
        if recurofftest:        # disable recurrence as a test, to see if inputs cause multiple spikes
            csuse=.25           # .2 not enough; .25 causes one output spike; .5 too much, causes multiple target spikes
            douserep=False      # the synapses aren't present if we disable recurrence, which causes error
            recurrconnecttype=0
            print "NO RECURRENCE TEST!!!!!!!!!!"
        # increased celldelay by 2 ms because follow-on spikes seemed to be coming just a bit late.  very touchy.
        newb, cells, ain, bin, cs, ced, cid, sl=MakeTRBrain(brainname=brainname, ncells=ncells, numsyns=numsyns, tstep=tstep, d=d, douserep=douserep, docurrrep=docurrrep, edelay=eps, phw=phw, celldelay=inptotargetdelay+recurdelay, csuse=csuse, nochannels=False, pincmp=True, depr=True, phpt=phpt)

        #absuse='0.01    0.0'
        #absuse='0.008    0.0'       # this is for the recurrent syns
        #absuse='0.001    0.0'       # this is for the recurrent syns.  THIS IS ONLY THE INITAL VALUE; modified by Hebbian.  see recurmaxcond
        absuse='0.000    0.0'       # this is for the recurrent syns.  THIS IS ONLY THE INITAL VALUE; modified by Hebbian.  see recurmaxcond
        inputs={}
        inputspikes={}
        for i in range(0, numinputs):
            inputs[i], inputspikes[i]=MakeStimSet2(ncells, (0, (tstep*inputlength)-(tstep/10)), rseed=i*39, tstp=tstep, actcells=inputwidth)

        cs.parms["LEARN_LABEL"]=newb.sls["0Hebb"]       # no hebb on input->target cell syns
        #ph=0.2
        ph=1.20
        sl.parms["POS_HEB_PEAK_DELTA_USE"]='%f   0.0' % ph
        # scale up input cells so single input pulse will cause target spike
        # (the recurrent connections use the ced[] cells with synapses with lower conductance):
        cs.parms["MAX_CONDUCT"]='0.035'         # at .030, sometimes cells don't fire reliably
        # start all cells in low activity
        nh=0.0       # disable neghebb because of double-spike issue
        sl.parms["NEG_HEB_PEAK_DELTA_USE"]='%f   0.0' % nh
        for d in range(1, numsyns+1):
            #ced[d].parms["LEARN_LABEL"]=newb.sls["0Hebb"]
            ced[d].parms["MAX_CONDUCT"]=recurmaxcond
            ced[d].parms["ABSOLUTE_USE"]=absuse

        tstp=.5       # spacing between stim *application* starts.  should be > numinputs * tstep between inputs
        pd=tstp         # how wide a time chunk to show in graph
        #t=0.0
        #t=ts        # if we are fudging backward due to delay from input->target delay, we can't start at time 0
        tstrt=1.0    # when to apply first input pattern
        iinc=0
        #while t < 20.0:
        t=tstrt
        endt=tstrt+tstp*trainings*numinputs
        if endt > teststart:
            print "end time is too big: %f" % endt
        print "end time of training period is %d" % endt
        while t < endt:
        #while t < 3.0:
            #inn=stdrandom.randrange(0, numinputs)
            #inn=stdrandom.randrange(0, 3)
            inn=iinc%numinputs
            # if we do this,
            # stimuli are actually applied slightly before the time shown in the inputspike list.
            # that is because there is some delay (5 ms or so) before the pulse on the input cell is communicated
            # to the target cell.  the spikes shown on the spike plot as red + symbols should correspond to the
            # approximate time that the spike is actually *felt* on the target cell
            #print "stimlen %d" % len(inputs[inn])
            ApplyStimSet(newb, inputs[inn], ain, timeoffset=float(t)-inptotargetdelay)
            vlin.append((t,   'r', '%d' %inn, t, t+pd))
            t+=tstp; iinc+=1

        # setup partial inputs of length numspikepartial spikes
        partialinputs={}

        if partialinputmethod=='time':  # test input is first portion of all signals
            for iin in range(0, numinputs):
                thispartialinput={}
                partialinputs[iin]=thispartialinput
                for cn in range(0, ncells):
                    thispartialinput[cn]=[]
                inpfull=inputspikes[iin]
                for sn in range(0, (numspikespartial*inputwidth)):
                    celno, spktm=inpfull[sn]
                    thispartialinput[celno].append(spktm)
        elif partialinputmethod=='space':       # test input is fraction of entire input width for entire duration
            for iin in range(0, numinputs):
                thispartialinput={}
                partialinputs[iin]=thispartialinput
                for cn in range(0, ncells):
                    thispartialinput[cn]=[]
                inpfull=inputspikes[iin]
                #for sn in range(0, (inputlength*inputwidth), inputwidth):  # to do partial inputs for entire input duration
                for sn in range(0, (numspikespartialL*inputwidth), inputwidth):   # to do partial inputs for just part of input duration
                    # pick off the first numspikespartial spikes in each timestep (all spikes in each timestep are stored together)
                    for psn in range(0, numspikespartialW):
                        celno, spktm=inpfull[sn+psn]
                        thispartialinput[celno].append(spktm)
        else:
            print "partial input method", partialinputmethod, "unknown"
            sys.exit(0)

        for iin in range(0, numinputs, 1):
            t=teststart+(iin * tstp)
            #print "stimlen %d" % len(partialinputs[iin])
            ApplyStimSet(newb, partialinputs[iin], ain, timeoffset=float(t)-inptotargetdelay)
            vlin.append((t,   'b', '%d' %iin, t, t+pd))
    #}}}

    # this thing just goes tetanic.  what is the state of this test?
    # Exp 2 {{{
    if False:
        # protocol:
        # if we started with a and b *input syns* string enough for a single input to cause a spike
        # and had variable synaptic delays
        # a single input pattern (in fact, a single input spike) would certainly cause outputs
        # to prevent deluge, connect each cell to two other random cells with each of syn delay
        # of say 1, 2, 3 . . .
        # such an output pattern would probably die out pretty quickly if target cells required >1 input
        # to fire again.
        # if it takes a coincidence of two cells to fire, a single excitatory spike input on one target would not
        # result any follow on spikes
        # but if more than one excitatory spike input occurred, there would be good possibility of same cell
        # getting hit twice in t+1, t+2, t+3 as consequence of inputs (assuming synapse delay only up to 3)
        # a single pattern on input with width but no duration (presence or absence of single spike on each input,
        # all occuring at same time)
        # the output would probably not look much like input.
        #   would need to test this
        # the output could persist for a while or go tetanic
        # if gain was > 1.  If the input had duration too, the chance of things going tetanic seems rather high
        # as there are more overlapping responses from initial input.
        # what would Hebbian learning do?
        # for the a->t and b-> synapses, by assumption these synapses already cause spikes on single input,
        #     so strengthening of syns there probably wouldn't matter
        # for the recurrent connections:
        #     whereas previously, two inputs were required to get fire in next generation,
        #       a recurrent syn could become strong enough to fire on its own
        #       then perhaps only one of the inputs a or b could cause the new output series
        #       to fire
        # but what is role of inhibitory syns?  make patterns even more complex?  prevent runaway spiking?
        # first task:  test with single input spikes, not time series
        inpa, aspk=MakeStimSet2(ncells, (0, tstep*2), rseed=25656, tstp=tstep, actcells=2)
        inpb, aspk=MakeStimSet2(ncells, (0, tstep*2), rseed=25657, tstp=tstep, actcells=2)
        inpc, aspk=MakeStimSet2(ncells, (0, tstep*2), rseed=25658, tstp=tstep, actcells=2)
        inpd, aspk=MakeStimSet2(ncells, (0, tstep*2), rseed=25659, tstp=tstep, actcells=2)
        # scale up so single input will cause target spike
        # (the recurrent connections use the ced[] cells with lower conductance):
        cs.parms["MAX_CONDUCT"]='0.028'
        for d in range(1, maxrecurdelay+1):       # disable Hebbian
            #ced[d].parms["LEARN_LABEL"]=newb.sls["0Hebb"]
            ced[d].parms["MAX_CONDUCT"]='0.009'
        pd=1.0
        for t in range(0, 20, 4):
            ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
            ApplyStimSet(newb, inpb, bin, timeoffset=float(t))
            vlin.append((t,   'r', 'a + b', t, t+pd))
        for t in range(2, 20, 4):
            ApplyStimSet(newb, inpc, ain, timeoffset=float(t))
            ApplyStimSet(newb, inpd, bin, timeoffset=float(t))
            vlin.append((t,   'g', 'c + d', t, t+pd))
        for t in [20, 24]:
            ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
            vlin.append((t,   'b', 'a->a', t, t+pd))
            ApplyStimSet(newb, inpb, bin, timeoffset=float(t+2))
            vlin.append((t+2, 'c', 'b->b', t+2, t+2+pd))
        for t in [28, 32]:
            ApplyStimSet(newb, inpc, ain, timeoffset=float(t))
            vlin.append((t,   'b', 'c->a', t, t+pd))
            ApplyStimSet(newb, inpd, bin, timeoffset=float(t+2))
            vlin.append((t+2, 'c', 'd->b', t+2, t+2+pd))
        dorecurr=True
        recurrconnecttype=2
        nrecurr=5       # number of syns output per target cell *per delay step*
        nrecurrinhib=1  # number of inhib syns output per target cell *per delay step*
    #}}}

    # not sure what this is
    # Exp 3 {{{
    if False:       # two input test
        for t in range(0, 20, 4):
            #print "both %d a only %d b only %d" % (t, t+2, t+3)
            # apply both
            ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
            ApplyStimSet(newb, inpb, bin, timeoffset=float(t))
            vlin.append((t, 'r', '', 0, 0))
            # apply just input a and see if we get same response
            ##ApplyStimSet(newb, inpa, ain, timeoffset=float(t+2.0))
            # apply just input b
            ##ApplyStimSet(newb, inpb, bin, timeoffset=float(t+3.0))
    #}}}

    # not sure what this is
    # Exp 4 {{{
    if False:
        """
        This protocol convincingly demonstrates that the non-recurrent network can readily
        learn association of inputs from two sources.  a particular pattern will invoke
        nothing on one input alone, but when repeatedly applied to two inputs at the same time,
        Hebbian learning on the synapses will allow later input on only one of the inputs to
        trigger the same output pattern (which is the same as the input pattern, since there is
        no recurrence).  Note on USE plot:  during simultaneous application of both inputs,
        there is only a small deviation in potentiation between the a and b input synapses.
        This variation is accounted for (I believe) by the small permitted variation in synaptic
        delay and also possibly the small stdevs allowed in some channel parameters.
        """
        dorecurr=False
        for t in range(0, 4, 4):
            # control, make sure this results in no firing before hebbian happens
            ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
            vlin.append((t, 'g', '', 0, 0))
        #
        for t in range(4, 20, 4):
            ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
            #ApplyStimSet(newb, inpb, bin, timeoffset=float(t))
            print "NOTE!  applying inpa to bin also!"
            ApplyStimSet(newb, inpa, bin, timeoffset=float(t))
            vlin.append((t, 'r', '', 0, 0))
        #
        for t in range(20, 24, 4):
            ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
            vlin.append((t, 'g', '', 0, 0))
        #
        for t in range(24, 28, 4):
            ApplyStimSet(newb, inpa, bin, timeoffset=float(t))
            vlin.append((t, 'b', '', 0, 0))
        #
        for t in range(28, 32, 4):
            ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
            vlin.append((t, 'g', '', 0, 0))
        #
        for t in range(32, 36, 4):
            ApplyStimSet(newb, inpa, bin, timeoffset=float(t))
            vlin.append((t, 'b', '', 0, 0))
        #
        for t in range(36, 40, 4):
            ApplyStimSet(newb, inpa, ain, timeoffset=float(t))
            vlin.append((t, 'g', '', 0, 0))
    #}}}

    #tss=ni*2.0
    # see if a input alone will invoke same output after 'training':
    #ApplyStimSet(newb, inpa, ain, timeoffset=float(tss))

    # an inhib syn with a delay just a bit more than cs, to prevent double spikes on input->target conns
    # when followup PSCs from delays arrive
    # this doesn't work because (I think): the forced spike occurs *second*.  the triggered PSCs are set up to arrive
    # *before* the forced spike, and if and when these do cause a triggered spike, the triggered spike
    # occurs *before* the forced spike.  we can easily inhibit the forced spike, which isn't what we want, but
    # to inhibit the triggered spike we would need this to arrive quite a bit sooner, which would require a negative
    # delay . . . 
    ci=newb.Copy(newb.syntypes, "C.strongI1", "Ci")
    de, des=cs.parms["DELAY"].split(); de=float(de); des=float(des)
    ci.parms["DELAY"]="%f %f" % (0.0+40*eps, 0.0+45*eps)

    # Make connections {{{
    # synapse output of each cell onto each other cell (but not onto self!)
    for n in range(0, ncells):
        # input connections:
        newb.AddConnect(ain[n], cells[n], cs, "1.0", "10.0")
        newb.AddConnect(bin[n], cells[n], cs, "1.0", "10.0")
        #newb.AddConnect(ain[n], cells[n], ci, "1.0", "10.0")        # to prevent double spikes
        #newb.AddConnect(bin[n], cells[n], ci, "1.0", "10.0")        # to prevent double spikes

        if recurrconnecttype==4:
        # each cell connects to each other cell with only 'nrecurr' connections, with delays randomly selected from 1..numsyns
            for tc in range(0, ncells):
                if n!=tc:   # it appears NCS silently ignores connections back to self
                    cls=range(1, numsyns+1)
                    stdrandom.shuffle(cls)
                    for ii in range(0, nrecurr):
                        #dely=stdrandom.randrange(1, numsyns+1)
                        dely=cls[ii]
                        ss=ced[dely]
                        newb.AddConnect(cells[n], cells[tc], ss, "1.0", "10.0")

        # fully connected with excitatory, no inhib connections
        if recurrconnecttype==3:
            for si in range(1, numsyns+1):
                ss=ced[si]      # excitatory cell with delay si*tstep
                for tc in range(0, ncells):
                    if n!=tc:   # it appears NCS silently ignores connections back to self
                        # each cell connects back to each other cell with each delay factor in numsyns
                        newb.AddConnect(cells[n], cells[tc], ss, "1.0", "10.0")
        #
        if recurrconnecttype==2:
            # each cell connects to 'nrecurr' unique input cells recurrently,
            # with delay of each 1, 2, 3 .. according to 'maxrecurdelay'
            # may connect back to self
            for si in range(1, maxrecurdelay+1):       # we do nrecurrs at each delay
                cls=range(0, ncells)       # pick random targets (at most one connect per target)
                stdrandom.shuffle(cls)
                for ii in range(0, nrecurr):
                    #si=stdrandom.randrange(1, maxrecurdelay+1)        # pick random delay
                    ss=ced[si]      # excitatory cell with that delay
                    newb.AddConnect(cells[n], cells[cls[ii]], ss, "1.0", "10.0")
                cls=range(0, ncells)       # pick random targets (at most one connect per target)
                stdrandom.shuffle(cls)
                for ii in range(0, nrecurrinhib):
                    #si=stdrandom.randrange(1, maxrecurdelay+1)        # pick random delay
                    ss=cid[si]      # inhib cell with that delay
                    newb.AddConnect(cells[n], cells[cls[ii]], ss, "1.0", "10.0")
            continue
        #
        if recurrconnecttype==1:
            for t in range(0, ncells):
                # recurrent connections
                #if n!=t: newb.AddConnect(cells[n], cells[t], cs, "1.0", "10.0")
                # if you want variable connect delays:
                #if n!=t: newb.AddConnect(cells[n], cells[t], csv, "1.0", "10.0")
                # 20% inhib, 80% excit, delay in on of n steps:
                if n!=t:
                    si=stdrandom.randrange(1, maxrecurdelay+1)
                    # pick synapse 20% inhib, 80% excit, of variable delay (1 to maxrecurdelay steps)
                    if(stdrandom.random() < .20):
                        ss=cid[si]
                    else:
                        ss=ced[si]
                    newb.AddConnect(cells[n], cells[t], ss, "1.0", "10.0")
    #}}}

    if dorun:
        rrr=newb.Run(verbose=3, nprocs=1)
        if not rrr:
            print "failure, exiting testsuite"
            sys.exit(0)
    else:
        print "NOT RUNNING due to dorun=False parameter"

    #print "exiting"
    #sys.exit(0)

    (tm_year,tm_mon,tm_day,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst)=time.localtime()
    plotdate=':'.join(['%04d'%tm_year,'%02d'%tm_mon,'%02d'%tm_day,'%02d'%tm_hour,'%02d'%tm_min,'%02d'%tm_sec])
    plotdate+='-'

    # Plots and reports {{{
    print "LoadSpikeData for all cells, all reports"
    for n in range(0, ncells):
        print "cell", n
        data[n]=LoadSpikeData(brainname, 'rep%s'%n)
        inadata[n]=LoadSpikeData(brainname, 'inarep%s'%n)
        inbdata[n]=LoadSpikeData(brainname, 'inbrep%s'%n)
        #print "cell %d data:" %n
        #print data[n]
    #
    #subplot(2, 1, 1)
    #gridx=[float(x) for x in range(2, 40, 2)]
    #grid(True, xdata=gridx)    # figure grid() out
    #grid(True)
    #
    if False:
        print "generating plot1"
        nextfigure(figsize=(8.5,11))
        title("spikes on target cells, all time")
        for pn in range(0, ncells):
            dd=data[pn]
            if len(dd[0]):
                scatter(dd[0], len(dd[0])*[pn])
        for (x, c, ttl, vts, vte) in vlin:
            vlines([x], 0, ncells, c)
        xlim((0, endsim))
        ylim((-1, ncells-1+.2))
        savefig(plotdate+'recurr-temp-SPIKES.png')
    #
    if docurrrep:
        currreplen=0.5      # how much data to display on x axis
        FSV=10000.0
        print "generating plot2"
        nextfigure(figsize=(8.5,11))
        #for pn in range(0, ncells):
        showcells=ncells
        nsp=showcells
        # the x range to plot is determined by what is in the Report reqeust, above.  all time data requested there is
        # plotted here
        for pn in range(0, showcells):
            cellno=(ncells-1)-pn     # want highest cell at top, not bot
            subplot(nsp, 1, pn+1)
            if pn==0: title("Current into internal cells")
            # each plot will show all of the synapses onto the cell (one coming from the output of each other cell)
            # but only synapses of the reported name; so if there are multiple syns of different types this
            # won't show them all
            try:
                ReportPlot(brainname, ['crep%s'%cellno], plottype=None, plottitle="", xlab="", ylab="cur%d" %cellno, newfigure=False)
            except:
                print "no cell of that type"
            ylim((0.0, 1.0))
            xlim((docurrrep*FSV, (docurrrep+currreplen)*FSV))
        subplots_adjust(bottom=0.05, right=0.95, top=0.95, left=0.05)
        savefig(plotdate+'recurr-temp-CURRENT.png')
    #
    if True:
        savefn='recurr-temp-spikes-splitout.pdf'
        TestRecurrentMemoryPlot3(savefn, plotdate, vlin, ncells, data, inputspikes, inputs, partialinputs, numinputs, inputlength, tstep)
        savefn='recurr-temp-spikes-splitout-inputs.pdf'
        TestRecurrentMemoryPlot3(savefn, plotdate, vlin, ncells, data, inputspikes, inputs, partialinputs, numinputs, inputlength, tstep, plotoutput=False)
        savefn='recurr-temp-spikes-splitout-outputs.pdf'
        TestRecurrentMemoryPlot3(savefn, plotdate, vlin, ncells, data, inputspikes, inputs, partialinputs, numinputs, inputlength, tstep, plotinput=False)

    #
    if False:
        print "generating plot4"
        nextfigure(figsize=(8.5,11))
        title("spikes on a input cells")
        for pn in range(0, ncells):
            dd=inadata[pn]
            if len(dd[0]):
                scatter(dd[0], len(dd[0])*[pn])
        for (x, c, ttl, vts, vte) in vlin:
            vlines([x], 0, ncells, c)
        xlim((0, endsim))
        ylim((-.2, ncells-1+.2))
        savefig(plotdate+'recurr-temp-ainput.png')
    #
    if False:
        print "generating plot5"
        nextfigure(figsize=(8.5,11))
        title("spikes on b input cells")
        for pn in range(0, ncells):
            dd=inbdata[pn]
            if len(dd[0]):
                scatter(dd[0], len(dd[0])*[pn])
        for (x, c, ttl, vts, vte) in vlin:
            vlines([x], 0, ncells, c)
        xlim((0, endsim))
        ylim((-1, ncells-1+.2))
        savefig(plotdate+'recurr-temp-binput.png')
    #
    if douserep:
        print "generating plot6"
        nsp=ncells
        nextfigure(figsize=(8.5,11))
        de=1
        title("recurrent E%d synapses (target->target cells)" % de)
        for pn in range(0, ncells):
            cellno=(ncells-1)-pn     # want cell 9 at top, not bot
            subplot(nsp, 1, pn+1)
            # each plot will show all of the synapses onto the cell (one coming from the output of each other cell)
            # but only synapses of the reported name; so if there are multiple syns of different types this
            # won't show them all
            try:
                ReportPlot(brainname, ['userep%d-%s'%(de, cellno)], plottype=None, plottitle="", xlab="", ylab="USE%d" %cellno, newfigure=False)
            except:
                print "no synapses of that type"
            ylim((-.1, 1.1))
        # vlines somehow screws up the plots in interesting ways.  figure this out some time . . . 
        #for (x, c) in vlin:
        #    vlines([x], 0, ncells, c)
        savefig(plotdate+'recurr-temp-USE.png')
    #
    if False:
        print "generating plot7"
        nsp=ncells
        nextfigure(figsize=(8.5,11))
        title("recurrent E3 synapses")
        for pn in range(0, ncells):
            cellno=(ncells-1)-pn     # want cell 9 at top, not bot
            subplot(nsp, 1, pn+1)
            # each plot will show all of the synapses onto the cell (one coming from the output of each other cell)
            # but only synapses of the reported name; so if there are multiple syns of different types this
            # won't show them all
            try:
                ReportPlot(brainname, ['userep3-%s'%cellno], plottype=None, plottitle="", xlab="", ylab="USE%d" %cellno, newfigure=False)
            except:
                print "no synapses of that type"
        # vlines somehow screws up the plots in interesting ways.  figure this out some time . . . 
        #for (x, c) in vlin:
        #    vlines([x], 0, ncells, c)
        savefig(plotdate+'recurr-temp-USE-E3.png')
    #}}}

    # save a record so we can reproduce these results
    progname='testsuite.py'
    cmd='cp %s %s%s; bzip2 %s%s' % (progname, plotdate, progname, plotdate, progname)
    print cmd
    os.system(cmd)
    show()

#--------------------------------------------------

if __name__ == "__main__":
    testall=False       # turn this on to force all tests
    showplots=False

    if 0:
        # warning:  psyco won't work with saving matplotlib figures as postscript
        try:
            import psyco
            psyco.profile()
        except:
            print "psyco not installed.  It may speed things up.  See http://psyco.sf.net"

    if 0:
        # rc stopped working, check into this . . . FIXME
        #rc('font', family='sans-serif')
        #rc('xtick', labelsize=10)
        #rc('ytick', labelsize=10)
        if len(sys.argv) > 1:
            if sys.argv[1]=='run': dorun=True
        else: dorun=False
        TestRecurrentMemory(dorun=dorun, doplot=True)

    if 1 or testall:
        #TestHebbian(showplots=showplots)
        TestHebbianMinimal()
        sys.exit(0)

    if 0 or testall:
        TestFacil(showplots=showplots)

    if 0 or testall:
        TestPulseInput()

    if False:
        # dense big col for LJ cover:
        newb=BRAIN({"TYPE": "AREA-BRAIN", "FSV": "10000.00", "JOB": 'LJcover1',
            "SEED": "-100", "DURATION": '0.0001', "OUTPUT_CELLS": "YES",
            "OUTPUT_CONNECT_MAP": "YES", "DISTANCE": "YES"})

        # standard library doesn't contain a cell type called EM, so we'll make one based on ES:
        EM=newb.Copy(newb.celltypes, "ES", "EM")
        L1=newb.Copy(newb.celltypes, "ES", "L1")

        # default inhib and excite synapse types used for all connections
        snE="E"; stE=newb.syntypes[snE]
        snI="I"; stI=newb.syntypes[snI]

        cn="col"
        #bc=BCol2(newb, cn, emsize=70, otherlaysize=70, DoInhib=True, eremprob=.4, synE=snE, synI=snI, w=600, h=800)
        bc=BCol2(newb, cn, emsize=170, otherlaysize=170, DoInhib=True, eremprob=.4, synE=snE, synI=snI, w=1200, h=1200)
        #print newb
        newb.Run()  # need to run to get the plot data from NCS

    """
    General warning about random seeds:  make sure you're not doing something dumb, particularly
    if the data gathering and data analysis are done in separate loops.  The use of random numbers
    needs to be the same in all cases otherwise, e.g., the prfstimpat sequences might be different
    which would obviously screw up matching.  Might be better to explicity reseed before each important
    step . . . 
    """
    if 0 or testall:
        if 0:
            parms={}
            parms['ntapecells']=4
            parms['allmaxcond']=0.0154559943825
            parms['allF']=0.158029020429
            parms['allD']=0.274797491729
            parms['poshebbdeltause']=0.0351669794321
            parms['neghebbdeltause']=0.0222478597239
            #parms['usechans']=False
        elif 1:
            # these parms got a fitness of 1.0625 on randseed 332
            parms={'initUSE': (0.26000000000000001, 0.13), 'allF': 0.048355522528290742, 'allD': 0.20902835488319396, 'stiminterval': 1.0, 'keytoL1prob': 1.0, 'stimdur': 0.20000000000000001, 'thalsize': 10, 'EStothalprob': 0.5, 'ntapecells': 6, 'initRSE': (0.9, 0.9), 'poshebbdeltause': 0.26500923395156861, 'allmaxcond': 0.0089242937415838254, 'DoInhib': True, 'interspike': 60, 'neghebbdeltause': 0.054066728651523586, 'thaltoL1prob': 0.5, 'nstimpat': 4, 'otherlaysize': 10, 'trainseq': (2, 2, 2, 2, 2), 'eremprob': 1.0, 'datatoERprob': 1.0}
        else:
            parms=None

        if False:
            f=nextfigure()
            np=3; pn=1

            subplot(np, 1, pn); pn+=1
            ts=150000       # start at 20 sec
            dd=100000       # go for 10 more sec
            ReportPlot("E0332", "EMUSERep", newfigure=False, cols=[75, 80, 85], linelab=['synapse 75', 'synapse 80', 'synapse 85'], xlab="", xrange=(ts, ts+dd), legendloc='center right', ylab='USE')
            # dup of above style SpikePatternPlot("E0332", ["L1Rep"], newfigure=False, ylab='L1 cell number', xrange=(0, 4))
            locs, labels=xticks(); xticks(locs, [""]*len(locs))

            subplot(np, 1, pn); pn+=1
            # this must come from another model since EM doesn't have that many cells anymore . . . 
            SpikePatternPlot("E0332", ["EMRep"], newfigure=False, xlab='', ylab='EM cell number', xrange=(15, 25))
            locs, labels=xticks(); xticks(locs, [""]*len(locs))
            legend(('Each dot is a spike', ), loc='center right')
            #legend()

            # this looks OK, not great, but doesn't contribute much new info and squishes other plots in size:
            #subplot(np, 1, pn); pn+=1
            #ReportSpikePlot("E0332", ["EMRep"], newfigure=False, xrange=(ts, ts+dd))
 
            subplot(np, 1, pn); pn+=1
            ReportPlot('E0332', ['EMRep'], newfigure=False, cols=[5], linelab=['EM cell 5'], xrange=(ts, ts+dd), legendloc='center right')

            savefig("LJfig1.ps"); print "saved to .ps"
            #show()
            sys.exit(0) 

        allbd=0; allad=0; allbk=0; allak=0; anumposs=0
        #for randseed in [1212, 2323, 3434, 4545, 5656, 6767, 7878, 8989, 9898, 5050, 3935, 5259]:
        #for randseed in [9212, 2323, 5259]:
        #for randseed in [1212]:
        # 4, 4, 4, 4 for randseed in range(360, 380):
        #for randseed in range(62000, 62005):
        for randseed in range(332, 333):
        #for randseed in [1000, 1010]:
        #for randseed in [2323, 5259]:
            ro=True
            brainname="E0"+`randseed`
            if 0:
                E0(brainname=brainname, randseed=randseed, randomorder=ro, dorun=True)
            elif 0:
                (bd, ad, bk, ak, numposs)=E0(brainname=brainname, randseed=randseed, randomorder=ro, dorun=False, doprofilecheck=False, doplot=True)
                print bd, ad, bk, ak, numposs
                allbd+=bd; allad+=ad; allbk+=bk; allak+=ak; anumposs+=numposs
            elif 1: # run and check results in one step
                fr=True
                #randseed=-99
                (bd, ad, bk, ak, numposs)=E0(brainname=brainname, randseed=randseed, randomorder=ro, dorun=False, nprocs=1, fullreports=fr, doprofilecheck=True, doplot=True, dosaveplots="ps", parms=parms)
                print bd, ad, bk, ak, numposs
                allbd+=bd; allad+=ad; allbk+=bk; allak+=ak; anumposs+=numposs
            else:
                E0(brainname=brainname, randseed=randseed, randomorder=ro, dorun=False, doplot=True)
                show()

        print "allbd, allad, allbk, allak", allbd, allad, allbk, allak, anumposs
        # good fitness is defined as improvement 
        #anumposs=float(anumposs)
        #fitness=float(allad-allbd)/anumposs + float(allak-allbk)/anumposs
        # just define fitness as absolute fraction of post-training answer correct, normalized by number of runs.  so, 0-1.0
        # logically, there should be no way the fraction of pre-training correct could be above chance.  it it is,
        # we need to figure out why!
        fitness=float(allad + allak)/float(anumposs) 
        print "fitness: %.4f" % (fitness)
        # look at .ps files with display instead of onscreen plots.  faster, better, easier, permanent record
        if 0:
            show()
