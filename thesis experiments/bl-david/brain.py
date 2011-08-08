#!/usr/bin/env python
import os, sys, string, random, copy

"""
brain.py
    This module provides core classes for building brain models for NCS, and converting
    those models into NCS formatted input files.

    Written by:
        Rich Drewes

    With contributions from:
        Quan Zou
        Milind Zirpe
        Rene Doursat

    6.0:  20081120 RPD  Misc. clean up and new features, specifically:

    Moved some fields in BRAIN and other classes out of class definition into __init__.
    Fields in class definition are of course common to all instances and that's not
    really want we want for most of these things, except for storage of some default
    values for parms.

    Paramater values (parms) can now be tuples and the values in the tuple will be placed on
    the resulting paramter line in the NCS file.  Previously you had to use a string value
    for this effect, e.g.:
        cs.parms["ABSOLUTE_USE"]="0.5  0.0"
    but now this also works:
        cs.parms["ABSOLUTE_USE"]=(0.5, 0.0)

"""

__version__="6.0"       # RPD:  6.0 in progress 20081120 . . . 

#import psyco in calling program to improve performance if desired

"""
FIXME:  add automatic assignment of sequential TYPE names to columns
        if there is not TYPE when they are added to brain (like stims etc.)
        also maybe support unspecified target names in BRAIN.Copy().  harder,
        since we don't necessarily know if it's a COLUMN, STIM, . . .

FIXME:  instead of exiting in some areas, we should throw exceptions

FIXME:  maybe rethink the SelectLib stuff, so that chantypes etc. are not
        elements of the class itself but rather we just access text keys
        in a class element currentlib or something like that.  Then we
        could keep a list of keys that would be easy to extend.  Would
        have to modify everything that directly references the brain.chantypes,
        brain.lays etc. elements.

FIXME:  move the tuple polymorphism (from AddConnect) and string/var coercion
        to GuessInput/GuessOutput, change arg to be the string/tuple

FIXME:  update Report and Stim stuff to use tuple polymorphism and
        connection point guessing

FIXME:  change e.g. AddCellTypes() to take either a variable, or a
        string which is automatically indexed into brain.celltypes[]

FIXME:  check all Standard*Column etc. to make sure objects are added to
        brain in order.  This will require the column creation in the
        routine itself rather than by caller.  See Standard1CellColumn
        for example.

FIXME:  consolidate all GuessInput/GuessOutput

FIXME:  Diagnostics aren't so good when e.g. PrintParm fails in StringOrVar . . .
        it is hard to figure out the context of the failure.  It helps to
        set debug=True in PrintParm, but not as much as it might.  To see,
        do an AddConnect with prob=None.

FIXME:  I have modified column-column connects to accept minimal arguments and
        try to figure the rest out.  Should make similar changes to the layer-layer
        connects, and cellgroup to cellgroup connects

FIXME:  change all AddConnect routines to take (frm) (to) which can be tuples

RULE:   when adding connects, we use text names of what we are connecting.
            but a variable should also work, since we can do a StringOrVar on it
            to extract the TYPE which is the text name (CONFIRM)
            (however the synapse used in the AddConnect apparently must be a variable,
            not a string name)
        when an element to something (celltype to layer) we must use a variable
            that points to what we are connecting.

THINK:  allow objects to be specified by string name instead of variable if they
        are predefined in standard component library?
        causes reference problems during brain print . . . think about this

THINK:  the AddX() routines (AddConnect, AddCellType etc.) don't return a variable, the
        same way the class routines COLUMN(), LAYER() etc. do.  Should this be changed?
        This happens because the cells exist in a global cellsp{} dict.  Perhaps
        we should create a new cell instance for each?  But the cell is really a
        cell *type*, that shares parameters with other cells.

THINK:  CELL_TYPE in LAYER class is a hash indexed by the name of the celltype
            the value stored there is the tuple of the (variable of the CELL_TYPE
            you want for that cell group name, number of cells you want of that type)  
        COMPARTMENT in CELL class is a list.  each element in the list is a tuple
            of (variable pointing to what kind of compartment you want, string label
            you use to reference it basically _name postpended, and some other
            data items) 
            search for _name to find places where this applies

CHECK:  cols store a (list or hash) of layers
        layers store a (list or hash) of cell types
        cell types store a (list or hash) of compartments
            confirm irregularity of compartment storage per above THINK
        also note that the list of layers in col is not a tuple
        but list of cell types in layer is a tuple (with # cells of that type)
        and list of compartment types in cell is a tuple (with various compartment parms)
        some centralization of what is stored in each list/hash would be helpful
            for now, look at AddCellType or AddLayer or AddCompartment to find the
            tuple in question
        answer:
            layers in column stored as a list of layers (not tuples, since no layer parms)
            cell types in layer stored as hash of tuple

NOTE:   it would be nice to be able to pass in a variable or string TYPE indentifier
    in all cases (for example, connects).  However, when traversing things to add
    everything to the brain it is easiest if there are variables only.  If there is
    just a string, we have to also have a hash of those elements to index the string
    into . . . 

DOCUMENT:

NOTE: that compartments are a little weird in that there is a separate name supplied
    on the COMPARTMENT line in the CELL definition after the compartment type.  This
    allows multiple instances of a compartment type in a CELL, separately named.
    In contrast, you cannot, for example, have multiple instances of the same CELL_TYPE
    in a LAYER, nor multiple instances of the same LAYER type in a COLUMN.
    However with the convention I am using where the compartment name is automatically
    constructed by postpending -name to the compartment TYPE, brainlab does reimpose
    a restriction of one instance of each type per compartment.  This could change
    if desired by making the name use some -`i` index or something as the compartments
    are added to the cell, and/or adding a __NAME or __LABEL parm to the COMPARTMENT.

NOTE:  when we do AddConnects, we can specify EITHER the text name of
    what we are connecting to OR the variable for what we are connecting to.  It's just
    stored in a tuple, and when we make the connect we check to see if it is a string or
    var and act appropriately, indexing into the dict if it is a text name.

NEW:  "enumerated" columns.  Motivation:  the columns in NCS natively only allow USE
    strengths to be specified on a cell group to cell group basis.  brain3 allows
    creation of an enumerated column type that will map into a column with multiple cell
    groups, one cell group for each cell, and then column to column connections
    to such a virtual column

NOTE:  if you don't specify DISTANCE=YES in brain definition, recent versions of NCS
        seem to simply exit without processing but without an error message.

NOTE on NCS .in file structure:
    BRAIN has COLUMN_TYPE lines that reference the TYPE line in COLUMN blocks.
    Thus there is no real re-usability of COLUMNS; you cannot define a type of
    column with a certain structure and then say I want column A, B, and C to
    be of this type.  However, if a set of columns shares layer sub structure,
    you can point each of the COLUMNs you define to the same LAYER_TYPE structures.
    Since NCS's .in file has no concept of AREA built in, you can't do the same
    thing at that level:  you must define a new COLUMN_TYPE that references a
    unique COLUMN block for each column in the area. 

DOCUMENT:
    defining a separate argument list as a variable (a dictionary) vs. doing
    it inline in the function call using {"a":"b", ...} notation.

    added areas
    added Test1 and Test2 test brains for direct invocation
    changes from version 2 to 3:  won't crash if no column-column connects

    .in file has three different locations for col->col connects, lay->lay connects, within-layer connects
    BRAIN CONNECT (col->col)
    fill col (lay->lay, within a single col)
    fill lay (cell->cell, within a single lay)
    all connects specify celltype and compartment
    this is a general connect for all:

    Only highest level structures need to be added to brain
    layer instances don't need to be added to brain, only to col that owns them.
    However, the layer *type* must be in the brain. 
    if you don't have areas in the brain, you should add the columns
    and add the layers to the columns
    if you do have areas in the brain, add the columns to the area
    and add the areas to the brain
"""

####################################################################

def mysort(l):
    """
    mysort sorts in place *and* returns sorted list

    The builtin sort function does not return the sort list, it sorts in place only,
    so to iterate over a dictionary like this:
    for a in d.keys().sort():
    does not work because that returns None
    so this works:
    for a in mysort(d.keys()):
    NOTE:  2.4 has sorted()
    """
    l.sort()
    return l

def InitParms(parms, pt, defaults=None):
    """
    Classes use this to initialize their parameters.

    defaults is a dictionary of values to set in
    the parameter dictionary returned, unless overridden by
    a setting for the same key in the argument parms.
    """
    sparms={}
    if defaults is not None:
        for p in defaults.keys():
            sparms[p]=defaults[p]
    for p in parms.keys():
        if(p in pt):
            sparms[p]=parms[p]
        else:
            print "parameter", p, "is not supported"
            sys.exit(-1)
    return sparms

class StringOrVarError(Exception):
    """
    The exception that says that something went wrong in StringOrVar conversion.
    Not currently using this.
    """
    def __init__(self):
        print "StringOrVarError, exiting"
        sys.exit(0)
    def __repr__(self):
        print "StringOrVarError __repr__"

def StringOrVar(vv):
    """
    Returns a string for whatever vv is, returning the TYPE if a one of the BRAIN classes.

    If vv is a string, return that.  If it is an int or float, convert it to a string.
    Else assume it is a variable, and return that variable's TYPE parameter.

    Better to let exceptions happen rather than trap them.
    Trapping them makes it hard to figure out where error occured,
    unless you dump call trace.
    """
    if(type(vv)==type("")):
        return vv
    elif(type(vv)==type(1)):
        return '%d' % vv
    elif(type(vv)==type(1.0)):
        return '%0.5f' % vv
    else:
        try:
            vvparms=vv.parms
        except AttributeError:
            print "StringOrVar:  there is no parms dictionary in the item to be printed."
            print "This is vv:", vv
            print "This is type(vv):", type(vv)
            print "Try setting debug to True in PrintParms."
            sys.exit(0)
        if type(vvparms) is not type({}):
            print "StringOrVar:  parms is not a dictionary."
            print "This is vv:", vv
            print "This is type(vv):", type(vv)
            print "This is vv.parms:", vv.parm
            print "This is type(vv.parms):", type(vv.parms)
            print "Try setting debug to True in PrintParms."
            #raise StringOrVarError
            sys.exit(0)
        if "TYPE" not in vv.parms:
            print "StringOrVar:  no TYPE in parms."
            print "This is vv:", vv
            print "This is type(vv):", type(vv)
            print "Try setting debug to True in PrintParms."
            # another option would be to return a string like "STRINGORVARERROR" that would be
            # inserted into the output file; this might make it easier to track down problems
            #raise StringOrVarError
            sys.exit(0)
        r=vvparms["TYPE"]
        return r

def PrintParms(pt, parms, name, optarg=None):
    """
    Classes use this to print out their parameters.

    This is smart enough to print list items as multiple lines with the same parameter name.

    FIXME:  factor out the new split line while loop
    """
    def SplitLine(vv, s, ispace, pl):
        """
        Try to nicely split up long vv parms onto separate lines with proper leading space.
        Leading spaces for first line has already been taken care of by caller.

        s is the output string we are building and will append to.
        vv is a string, possibly with spaces, possibly quite long, that we may be able to split.
        ispace is a string that is the space to put between the values (after the parameter name).
        pl is a blank string long enough to contain any parameter name.
        SplitLine will put a newline at the end of the line we are building.
        """
        ln=0
        if len(vv)==0:
            # just in case there is no string there (like plain ASCII parm on report)
            s.append('\n')
            return
        while len(vv) > 0:
            # find a space to break on
            ii=vv[MAXPARM:].find(' ')
            if ii < 0:  # no spaces, can't split line, bail
                #print 'WHOLE PART:>%s<>%s<'%(vv, vv[:MAXPARM+ii])
                s.append(vv)
                vv=''
            else:
                #print 'FIRST PART:>%s<>%s<'%(vv, vv[:MAXPARM+ii])
                s.append(vv[:MAXPARM+ii])       # print first portion
                vv=vv[MAXPARM+ii+1:]
            s.append('\n')
            if len(vv) > 0: # if there is more to print, set up leading spaces
                s.append(ispace)
                s.append(pl)        # tab over for next portion of this long line
                if not vv.startswith('-'): s.append(' ')
        # END OF SplitLine!

    MAXPARM=50     # wrap parms if longer than this, breaking on spaces only.  this is parm len only, so add pl to get total line len
    debug=False
    pl="                             "
    s=[]
    if optarg:
        s.append(name)
        s.append(" ")
        s.append(optarg)
        s.append("\n")
    else:
        s.append(name)
        s.append("\n")
    if debug: print "\n\nPrintParms, pt before loop is:", pt
    for p in pt:        # parms printed in order they are in our permitted parms list, pt
        try:
            if debug: print "PrintParms looping on parm p=", p, "type ", type(p), "from pt=", pt
            if p in parms.keys():
                if p[0]=="_": continue      # leading underscore means internal parm, don't print
                # print pl-len(p) spaces
                v=parms[p]
                # Maybe it's a list; then print a line for each, e.g. a bunch of connects,
                # or a bunch of channels in a compartment, or a bunch of layers in a column
                # Could also be a hash now (I changed the contents of CELL_TYPE from being a list to a hash)
                # NEW:  a tuple indicates multiple numeric items for that line (often a value and a stddev, or a range)
                # FIXME:  reduce redundant code below
                # FIXME  this has become a bit sneaky with tuple/hash/list distinction
                if type(v)==type({}):   # if it's a hash, then contents of each hash element contains vars to print . . . 
                    for k in mysort(v.keys()):
                        # this may not handle general cases, but CELL_TYPE is (I think) the only hash for now
                        vv=v[k]
                        if(type(vv)==type(())):
                            if debug: print "the data itself is a tuple!", vv
                            vt=""
                            for vi in vv:
                                vt=vt+StringOrVar(vi)+" "
                            vv=vt
                        else:           # a string or variable single item
                            vv=StringOrVar(vv)
                        if(len(vv)):            # improve alignment of output by shifting initial negative numbers left one
                            min=vv[0]=="-"
                        else:
                            min=0
                        s.append("    ")
                        s.append(p)
                        s.append(" ")
                        s.append(pl[len(p)+min:])
                        SplitLine(vv, s, '    ', pl)
                elif type(v)==type(()):     # a tuple indicates multiple numeric values.  NEW
                    # this leaves a trailing space after last value, but no big deal
                    vt=""
                    for vv in v:        # for each number in tuple . . .
                        vt=vt+StringOrVar(vv)+" "
                    vv=vt
                    if(len(vv)):            # improve alignment of output by shifting initial negative numbers left one
                        min=vv[0]=="-"
                    else:
                        min=0
                    s.append("    ")
                    s.append(p)
                    s.append(" ")
                    s.append(pl[len(p)+min:])
                    SplitLine(vv, s, '    ', pl)
                elif type(v)==type([]):
                    for vv in v:
                        # item may be a single string, a single variable, or a tuple of strings and variables
                        # print them all out in order, printing strings as strings and any vars as the TYPE
                        # stored in that variable's parms
                        if(type(vv)==type(())):
                            if debug: print "the data itself is a tuple!", vv
                            # FIXME:  worth replacing with join()?
                            vt=""
                            for vi in vv:
                                vt=vt+StringOrVar(vi)+" "
                            vv=vt
                        else:           # a string or variable single item
                            vv=StringOrVar(vv)
                        if(len(vv)):            # improve alignment of output by shifting initial negative numbers left one
                            min=vv[0]=="-"
                        else:
                            min=0
                        s.append("    ")
                        s.append(p)
                        s.append(" ")
                        s.append(pl[len(p)+min:])
                        SplitLine(vv, s, '    ', pl)
                elif v==None:
                    print "PrintParms:  v is None.  That won't work."
                    print "p=", p
                    print "pt=", pt
                    #sys.exit(0)
                    raise       # should create my own exception derived from Exception . . .
                else:                   # just a regular item (a string or variable reference)
                    vv=StringOrVar(v)
                    if(len(vv)):
                        min=vv[0]=="-"
                    else:
                        min=0 
                    if debug: print p, vv
                    s.append("    ")
                    s.append(p)
                    s.append(" ")
                    s.append(pl[len(p)+min:])
                    SplitLine(vv, s, '    ', pl)
        except StringOrVarError:
            print "StringOrVar threw exception."
            print "Called from PrintParms while looping on:"
            print "p:", p
            print "type(p):", type(p)
            #print "parms the user passed parms=", parms
            print "parms permitted for this object pt=", pt
            print "Rerunning with debug=True in PrintParms might help too."
            sys.exit(0)

    s.append("END_")
    s.append(name)
    s.append("\n")
    return "".join(s)

####################################################################

class BRAIN:
    pt=["TYPE", "FSV", "JOB", "PORT", "SERVER", "SERVER_PORT", "SEED", "DURATION",
        "COLUMN_TYPE", "CONNECT", "STIMULUS_INJECT", "REPORT", "EVENT",
        "OUTPUT_CELLS", "OUTPUT_CONNECT_MAP", "LOAD", "SAVE", "DISTANCE", "_MAXCOND"]
    __version__="5.0"
    defaultparms={'TYPE': 'testbrain',
                  'FSV': '10000.00',
                  'JOB': 'testbrainjob',
                  'SEED': '-99',
                  'DURATION': '1.0',
                  'OUTPUT_CELLS': 'YES',
                  'OUTPUT_CONNECT_MAP': 'YES',
                  'DISTANCE': 'YES',
                  '_MAXCOND': '0.0024'}

    def __init__(self, parms={}, epsc=None, ipsc=None, simsecs=None, jobname=None, fsv=None):
        """
        Create a BRAIN object for modeling.

        Keyword args epsc and ipsc are the EPSC.txt and IPSC.txt
        waveform template filenames for excitatory and inhibitory post synaptic
        currents.  If they are not supplied, they will be guessed from
        the environment as $HOME/EPSC.txt and $HOME/IPSC.txt.

        parms is a dictionary for BRAIN level .in file parameters.
        Refer to NCS docs for available options.  If certain
        parameters are not supplied, defaults will be used as
        shown in BRAIN.defaultparms.
        """
        self.autocolnum=0        # sequence # for automatic naming of columns
        self.autostiminjnum=0
        self.autostimnum=0
        self.areas={}
        self.syns=None
        self.reportports=[]
        self.stimports=[]
        self.libs={}
        self.parms=InitParms(parms, self.pt, defaults=self.defaultparms)
        if self.parms["FSV"]!="10000.00":
            print "WARNING:  unusual FSV."
            #sys.exit(0)
        if simsecs is not None:
            self.parms["DURATION"]="%s" % simsecs
        if jobname is not None:
            self.parms["JOB"]=jobname
        if fsv is not None:
            self.parms["FSV"]="%s" % fsv
        if epsc is None or ipsc is None:
            # guess at the EPSC.txt and IPSC.txt waveform files
            homedir=os.environ['HOME']
            if epsc is None: epsc=os.path.join(homedir,"EPSC.txt")
            if ipsc is None: ipsc=os.path.join(homedir,"IPSC.txt")
            #print "Guessed IPSC and EPSC filenames as %s and %s." %(ipsc, epsc)
            #print "If that's wrong, supply them as epsc= and ipsc= in BRAIN()"
        self.StandardStuff(maxcond=float(self.parms["_MAXCOND"]), epsc=epsc, ipsc=ipsc)

    def version(self):
        """
        Returns BRAIN class version string.
        """
        return self.__version__

    def TraverseSynapse(self, synapse, synapses, syn_psg, syn_learning, syn_facil_depress, syn_augmentation):
        """
        Add all the referenced substructures from the synapse to the appropriate lists in the brain so that they can be conveniently printed.
        """
        if synapse not in synapses:
            synapses.append(synapse) 
        spsg=synapse.parms["SYN_PSG"]
        if spsg not in syn_psg:
            syn_psg.append(spsg)
        ll=synapse.parms["LEARN_LABEL"]
        if ll not in syn_learning:
            syn_learning.append(ll)
        sfd=synapse.parms["SFD_LABEL"]
        if sfd not in syn_facil_depress:
            syn_facil_depress.append(sfd)
        if synapse.parms.has_key("SYN_AUGMENTATION"):
            sa=synapse.parms["SYN_AUGMENTATION"]
            if sa not in syn_augmentation:
                syn_augmentation.append(sa)
        return (synapses, syn_psg, syn_learning, syn_facil_depress, syn_augmentation)

    def GetReportPorts(self):
        """
        Return a list of the port numbers this BRAIN is configured to use for port (network) based reporting.
        """
        ports=[]
        reps=self.parms["REPORT"]
        #print "reports:", reps
        for r in reps:
            if "PORT" in r.parms:       # might be a file based report
                p=r.parms["PORT"]
                ports.append(p)
        return ports

    def GetStimulusPorts(self):
        """
        Return a list of the port numbers this BRAIN is configured to use for port (network) based stimulus input.
        """
        ports=[]
        stimis=self.parms["STIMULUS_INJECT"]
        #print "reports:", reps
        for si in stimis:
            s=si.parms["STIM_TYPE"]
            p=s.parms["PORT"]
            ports.append(p)
        return ports

    def GetSynapses(self):
        """
        Return an ordered list of integer *strengths* of all synapses in the brain.

        If the synapse stored there did not have a strength associated with it
        (it was a base synapse, and does not end in __<int>, then that element
        will be set to None.  Otherwise, that element will be set to <int>.
        The order of this list will depend on the order in which the brain
        is constructed.  Therefore once you start caring about the order
        of synapses, you should not change how the brain is built,
        otherwise USE connections will be moved about.

        FIXME:  maxcond is a better indicator of synapse strength.
        The standard synapses should use that instead of USE.
        USE represents top of range in which short turm Facil
        and Depr adjust in; USE can be adjusted by Hebbian learning.
        """
        def GetSynapseStrength(synapse):
            """
            Return int strength of synapse, or None if it is not a __<int> type synapse.
            """
            vs=synapse.parms["TYPE"].split("__")
            if len(vs) == 2:
                val=int(vs[1])
                return val
            else:
                return None

        synstr=[]
        if "CONNECT" in self.parms:      # intercolumn connects
            cons=self.parms["CONNECT"]
            for i in range(0, len(cons)):
                (frmcol, frmlay, frmcell, frmcmp, tocol, tolay, tocell, tocmp, synapse, prob, speed)=cons[i]
                synstr.append(GetSynapseStrength(synapse))

        if("COLUMN_TYPE" in self.parms):
            for c in self.parms["COLUMN_TYPE"]:
                if "CONNECT" in c.parms:
                    cons=c.parms["CONNECT"]
                    for i in range(0, len(cons)):       # intracolumn (interlayer) connects
                        (frmlay, frmcell, frmcmp, tolay, tocell, tocmp, synapse, prob, speed)=cons[i]
                        #print "CONSYN: ", synapse
                        synstr.append(GetSynapseStrength(synapse))
                lays=c.parms["LAYER_TYPE"]
                for l in lays:
                    if "CONNECT" in l.parms:
                        cons=l.parms["CONNECT"]
                        for i in range(0, len(cons)):       # intralayer (celltype->celltype) connects
                            (frmcell, frmcmp, tocell, tocmp, synapse, prob, speed)=cons[i]
                            #print "LAYSYN: ", synapse
                            synstr.append(GetSynapseStrength(synapse))

        return synstr        

    def SetSynapses(self, synstr, syns):
        """
        Set synapses strengths in the brain to values in newstr[].

        synstr should be same len as the set of syns
        we find when we enumerate them here; if not, fail with error.

        FIXME:  maxcond is a better indicator of synapse strength.
        USE represents top of range in which short turm Facil
        and Depr adjust in; USE can be adjusted by Hebbian
        learning.
        """
        #print "SetSynapses:  supplied list is len", len(synstr)
        def ChangeSynapseStrength(syn, newstr, syns):
            """
            Set a synapse strength by changing the name of the synapse to <name>__<int>.

            FIXME:  maxcond is a better indicator of synapse strength.
            USE represents top of range in which short turm Facil
            and Depr adjust in; USE can be adjusted by Hebbian
            learning.

            Here we are changing synapse profiles, where the different
            profiles have different USE values, not maxconds.
            """
            if newstr==None:       # convert back to base synapse type
                syntype=syn.parms["TYPE"].split("__")[0]
            else:                       # change to requested strength
                syntype=syn.parms["TYPE"].split("__")[0]+"__"+`newstr`
            return syns[syntype]

        sn=0
        if "CONNECT" in self.parms:      # intercolumn connects
            cons=self.parms["CONNECT"]
            for i in range(0, len(cons)):
                (frmcol, frmlay, frmcell, frmcmp, tocol, tolay, tocell, tocmp, syn, prob, speed)=cons[i]
                newsyn=ChangeSynapseStrength(syn, synstr[sn], syns)
                cons[i]=(frmcol, frmlay, frmcell, frmcmp, tocol, tolay, tocell, tocmp, newsyn, prob, speed)
                sn=sn+1

        if("COLUMN_TYPE" in self.parms):
            for c in self.parms["COLUMN_TYPE"]:
                if "CONNECT" in c.parms:
                    cons=c.parms["CONNECT"]
                    for i in range(0, len(cons)):       # intracolumn (interlayer) connects
                        (frmlay, frmcell, frmcmp, tolay, tocell, tocmp, syn, prob, speed)=cons[i]
                        newsyn=ChangeSynapseStrength(syn, synstr[sn], syns)
                        cons[i]=(frmlay, frmcell, frmcmp, tolay, tocell, tocmp, newsyn, prob, speed)
                        sn=sn+1
                lays=c.parms["LAYER_TYPE"]
                for l in lays:
                    if "CONNECT" in l.parms:
                        cons=l.parms["CONNECT"]
                        for i in range(0, len(cons)):       # intralayer (celltype->celltype) connects
                            (frmcell, frmcmp, tocell, tocmp, syn, prob, speed)=cons[i]
                            #print "len str is ", len(synstr), sn, len(cons)
                            newsyn=ChangeSynapseStrength(syn, synstr[sn], syns)
                            cons[i]=(frmcell, frmcmp, tocell, tocmp, newsyn, prob, speed)
                            sn=sn+1

    def GetBrainJob(self):
        """
        Return the BRAIN's JOB parm value.
        """
        if "JOB" in self.parms:
            return self.parms["JOB"]
        else:
            print "GetBrainJob:  no JOB defined"
            sys.exit(0)

    def Run(self, verbose=False, nprocs=1, clearreports=True, parms=None, procnum=None, showprogress=False):
        """
        Simulate the BRAIN with NCS.

        parms allows some BRAIN parms to be overridden, if desired,
        for example, change the job name of an existing brain model after adjustment.

        Eventually change this from being a BRAIN.method to a brainlab function.
        """
        print "instead of BRAIN.Run(), you should now use the brainlab.Run(BRAIN) function"
        return -1

    def Plot3D(self):
        """
        Use netplot to plot a 3D representation of the BRAIN.

        Changed this from a BRAIN.method() to a brainlab function.
        """
        print "instead of BRAIN.Plot3D() method, you should now use the brainlab.Plot3D(BRAIN) function"
        return -1
        #brainlab.plot(self)

    def __repr__(self):
        """
        Convert a BRAIN to its string representation, an NCS .in file.
        """
        # go through the brain once, starting at highest level constructs (column for now, area
        # later, perhaps sheet?) and keep lists of all sub-structures of all types referenced:
        # chans, synapses, etc., for printing.
        # only the highest-level brain structures (columns for now) need to be added to the brain explicitly
        # (plus all stims and reports, of course).
        # the columns reference lower level brain structures, like layers, which reference cells . . . 
        #stims=[]   # now a dict
        synapses=[]
        channels=[]
        cmps=[]
        celltypes=[]
        layers=[]
        spikeshapes=[]
        syn_psg=[]
        syn_facil_depress=[]
        syn_learning=[]
        syn_augmentation=[]

        # there are synapses we must tabulate in intercolumn connects, intra column connects,
        # intra layer connects

        # this whole method of finding what is in the brain by traversing all structs
        # is pretty complex

        if("CONNECT" in self.parms):
            for con in self.parms["CONNECT"]:       # list of intercolumn connects
                (frmcol, frmlay, frmcell, frmcmp, tocol, tolay, tocell, tocmp, synapse, prob, speed)=con
                (synapses, syn_psg, syn_learning, syn_facil_depress, syn_augmentation)=\
                    self.TraverseSynapse(synapse, synapses, syn_psg, syn_learning, syn_facil_depress, syn_augmentation)

        # NOTE:  we don't need to look for cells in the connects, since
        # obviously nothing could connect to a cell that isn't also appearing in some column.
        # But for *synapses* and derivative structures, we *do* need to look at connects
        # (and at all three levels of connect, in fact) because some synapses may
        # only be present in some specific connects.  The TraverseSynapse() utility
        # routine makes that easy.

        if("COLUMN_TYPE" in self.parms): cos=self.parms["COLUMN_TYPE"]
        else: cos=[]

        #print "class BRAIN:  first column pass"; sys.stdout.flush()
        for c in cos:           # first pass through columns, to see what is referenced
            if("CONNECT" in c.parms):
                for con in c.parms["CONNECT"]:       # intracolumn (interlayer) connects
                    (frmlay, frmcell, frmcmp, tolay, tocell, tocmp, synapse, prob, speed)=con
                    (synapses, syn_psg, syn_learning, syn_facil_depress, syn_augmentation)=\
                        self.TraverseSynapse(synapse, synapses, syn_psg, syn_learning, syn_facil_depress, syn_augmentation)
            if 'LAYER_TYPE' not in c.parms: continue
            lays=c.parms["LAYER_TYPE"]
            #print "class BRAIN:  first column pass, layer loop"; sys.stdout.flush()
            for l in lays:
                if("CONNECT" in l.parms):
                    for con in l.parms["CONNECT"]:       # intralayer (celltype->celltype) connects
                        #print "CONNECT layer:", con
                        (frmcell, frmcmp, tocell, tocmp, synapse, prob, speed)=con
                        (synapses, syn_psg, syn_learning, syn_facil_depress, syn_augmentation)=\
                            self.TraverseSynapse(synapse, synapses, syn_psg, syn_learning, syn_facil_depress, syn_augmentation)
                if l not in layers:
                    layers.append(l)
                layct=l.parms["CELL_TYPE"]
                #print "class BRAIN:  first column pass, k in sort layct.keys()"; sys.stdout.flush()
                for k in mysort(layct.keys()):
                    (c, n)=layct[k]
                    if type(c) == type(""):
                        print "BRAIN print:  cell is type string.  Should be type CELL"; sys.stdout.flush()
                        sys.exit(0)
                    if c not in celltypes:
                        celltypes.append(c)
                    cellcmps=c.parms["COMPARTMENT"]
                    for (comptype, complabel, x, y, z) in cellcmps:
                        if comptype not in cmps:
                            cmps.append(comptype)
                        if 'CHANNEL' in comptype.parms:
                            cmpchans=comptype.parms["CHANNEL"]
                            #print "BRAIN repr:  cmpchans", cmpchans
                            for ch in cmpchans:
                                if ch not in channels:
                                    #print "BRAIN repr:  adding ch", ch
                                    channels.append(ch)
                        ss=comptype.parms["SPIKESHAPE"]
                        if ss not in spikeshapes:
                            spikeshapes.append(ss)
                # find synapses in connects at each level

        #print "class BRAIN:  after first column pass"; sys.stdout.flush()
        # get the stimulus referenced by each stim injection and add it to local list
        if("STIMULUS_INJECT" in self.parms):
            sts=self.parms["STIMULUS_INJECT"]
        else:
            sts=[]

        # sts is a list of variables of class STIMULUS_INJECTs
        #   the STIM_TYPE is a variable of class STIMULUS
        # stims is a list of variables of class STIMULUS
        # the sts list may contain multiple instances of the same STIMULUS; so we
        # do need to check for dups in the stims list after we build it
        stims={}        # faster for finding dups to use a hash than list append and sort
        stimsection="# SECTION stimulus\n"
        stiminjsection="# SECTION stiminject\n"
        #print "class BRAIN:  for st in sts, num sts:", len(sts), "num stims", len(stims); sys.stdout.flush()
        for st in sts:
            stiminjsection+=`st`+"\n"
            stimtype=st.parms["STIM_TYPE"]
            if stimtype not in stims:
                stims[stimtype]=stimtype
                stimsection+=`stimtype`+"\n"

        #print "class BRAIN:  before printparms"; sys.stdout.flush()
        s=[]
        # this PrintParms will print all the inter-column connects
        s.append(PrintParms(self.pt, self.parms, "BRAIN"))
        s.append("\n")

        #print "class BRAIN:  second column pass"; sys.stdout.flush()
        s.append("# SECTION fill columns\n")
        for c in cos:           # second pass through columns, to print COLUMN_SHELL dummies
            if "_WIDTH" in c.parms:
                wid=c.parms["_WIDTH"]
                hei=c.parms["_HEIGHT"]
                xloc=c.parms["_XLOC"]
                yloc=c.parms["_YLOC"]
            else:
                wid="300.0"
                hei="150.0"
                xloc="10.0"
                yloc="20.0"
            s.append(self.EmitColumnShell(c.parms["TYPE"], wid, hei, xloc, yloc))
            s.append("\n")
            s.append(`c`)
            s.append("\n")

        #print "class BRAIN:  layer pass"; sys.stdout.flush()
        s.append("# SECTION fill layers\n")
        for l in layers:
            # attempt to get the layer position from the name
            # this only works if layers are named ending in nLay-x
            # where n is the number of layers in the col, and x is the number of this layer (1, 2, ...)
            # currently this only works with single digit n and x
            lname=l.parms["TYPE"] 
            #print "lname is", lname
            if "_UPPER" in l.parms:
                upr=l.parms["_UPPER"]
                lwr=l.parms["_LOWER"]
            elif lname[-2]=="-" and (lname[-3]=="y" or lname[-3]=="Y") and (lname[-5]=="l" or lname[-5]=="L"):
                nlays=int(lname[-6])
                layn=int(lname[-1])
                ls=100/nlays
                upr=ls*layn; lwr=upr-ls
            else:
                upr=80; lwr=20
            s.append(self.EmitLayerShell(lname, `upr`, `lwr`))
            s.append("\n")
            #print "trying to print out the layer", l
            s.append(`l`)
            s.append("\n")

        #print "class BRAIN:  after layer pass"; sys.stdout.flush()
        s.append("# SECTION cells\n")
        for c in celltypes:
            s.append(`c`)
            s.append("\n")

        #print "class BRAIN:  stim"; sys.stdout.flush()
        s.append(stimsection)
        #print "class BRAIN:  stiminj"; sys.stdout.flush()
        s.append(stiminjsection)

        #print "class BRAIN:  report"; sys.stdout.flush()
        s.append("# SECTION report\n")
        if("REPORT" in self.parms):
            for a in self.parms["REPORT"]:
                s.append(`a`)
                s.append("\n")

        #print "class BRAIN: event"; sys.stdout.flush()
        s.append("# SECTION event\n")
        if("EVENT" in self.parms):
            for a in self.parms["EVENT"]:
                s.append(`a`)
                s.append("\n")

        #print "class BRAIN:  comp"; sys.stdout.flush()
        s.append("# SECTION compartments\n")
        for c in cmps:
            s.append(`c`)
            s.append("\n")

        #print "class BRAIN:  chan"; sys.stdout.flush()
        s.append("# SECTION channels\n")
        for c in channels:
            s.append(`c`)
            s.append("\n")

        #print "class BRAIN:  spikeshape"; sys.stdout.flush()
        s.append("# SECTION spikeshape\n")
        for c in spikeshapes:
            s.append(`c`)
            s.append("\n")

        #print "class BRAIN:  synpsg"; sys.stdout.flush()
        s.append("# SECTION syn_psg\n")
        for c in syn_psg:
            s.append(`c`)
            s.append("\n")

        #print "class BRAIN:  sfd"; sys.stdout.flush()
        s.append("# SECTION syn_facil_depress\n")
        for c in syn_facil_depress:
            s.append(`c`)
            s.append("\n")

        #print "class BRAIN:  syn_learn"; sys.stdout.flush()
        s.append("# SECTION syn_learning\n")
        for c in syn_learning:
            s.append(`c`)
            s.append("\n")

        #print "class BRAIN:  syn_augm"; sys.stdout.flush()
        s.append("# SECTION syn_augmentation\n")
        for c in syn_augmentation:
            s.append(`c`)
            s.append("\n")

        #print "class BRAIN:  synapse"; sys.stdout.flush()
        s.append("# SECTION synapse\n")
        for c in synapses:
            s.append(`c`)
            s.append("\n")

        #print "class BRAIN:  returning"; sys.stdout.flush()
        return "".join(s)

    def AddColumn(self, col):
        """
        Put COLUMN object col into the BRAIN

        Should this really be AddColumnType()?
        Maybe.  NCS calls them COLUMN_TYPES in the BRAIN section
        even though there really isn't any "type-of" abstraction;
        each COLUMN_TYPE must reference a COLUMN block below.
        First, they probably shouldn't be called COLUMN_TYPES in
        the BRAIN section; they should be called COLUMN.  And the
        COLUMN..END_COLUMN blocks should be called COLUMN_TYPE.
        Similarly, LAYER_TYPES are specified in COLUMN..END_COLUMN
        blocks, but they should be LAYER.  Hmm.

        The TYPE name of the column may not be defined when the
        COLUMN is initially created; in this case it will be generated
        automatically when the COLUMN is added to the BRAIN.
        """
        b=self
        col.brain=b
        if "TYPE" not in col.parms:
            # no name supplied, just assign some unique name.  would be better if it were
            # just unique per brain
            self.autocolnum+=1
            col.parms["TYPE"]="col"+`self.autocolnum`
        cn=col.parms["TYPE"]
        col.parms["COLUMN_SHELL"]=col.parms["TYPE"]+"_sh"      # temp hack
        b.cols[cn]=col
        self.parms.setdefault("COLUMN_TYPE", []).append(col)
        return col

    def AddArea(self, areaname, hx, hy, mx, my, w, h, xloc, yloc, colfunc, lays, cells, syns, comptypes):
        """
        Add an area of the indicated dimensions to the BRAIN.  (EXPERIMENTAL)

        This worked in earlier releases but hasn't been tested lately.

        Areas have no direct counterpart in the NCS .in file; we expand this request to
        a corresponding set of columns, and keep a record in the brain of the areas
        added.  Note that since we need to create custom columns, with our area-name
        prefix and using requested synapses, we pass a column creator function (colfunc) in to
        AddArea rather than passing in a column name.  If we passed in a column name
        we could perhaps clone that column, and modify the name, but that's ugly.
        (Actually, it might not be that bad to allow either one.)

        hx, hy:  hypercolumn x and y dimensions
        mx, my:  x andy dims in minicols within each hypercol
        """
        mcw=w/(hx*mx)  # mcw is minicol width
        hcw=w/(hx)     # hcw is hypercol width
        # center around xloc, yloc, so begin half width below each
        cxloc=xloc-(w/2.0)
        cyloc=yloc-(w/2.0)
        # loop over hypercols:
        allcols=[]
        #allcons=[]
        for x in range(1, hx+1):
            for y in range(1, hy+1):
                hcx=cxloc+hcw*(x-1)
                hcy=cyloc+hcw*(y-1)
                # loop over minicols
                for xx in range(1, mx+1):
                    for yy in range(1, my+1):
                        mcx=hcx+mcw*(xx-1)
                        mcy=hcy+mcw*(yy-1)
                        cn=areaname+"-"+`x`+"-"+`y`+"-"+`xx`+"-"+`yy`
                        sm=""
                        col=colfunc(cn, sm, (mcw/3), h, mcx, mcy, lays, cells, syns, comptypes) 
                        allcols.append(col)     # add to list to store with area
                        self.AddColumn(col)

        self.areas[areaname]=(hx, hy, mx, my, allcols)

    def ColumnConnect(self, c1, c2, lays, cells, syn, prob, speed): 
        """
        (DEPRECATED) Add a BRAIN level connect from cols c1 to c2.  Use AddConnect() instead.

        This is kept around since it was working with enumerated columns too.
        Move that feature from here to AddColumn() at some point.

        columns may either be enumerated or not
        (Enumerated cols have not been tested recently.)

        Four possibilities:
        src enum, dst enum
        src enum, dst not
        src not,  dst enum
        src not,  dst not         ( "normal" NCS)
        if we do things right, the number of connections for each type will end up
        the same on average for each approach
        so if src is not enum, and dest is enum, we'll get the size of the src cell group
        and for each cell in there, do a probability check for each cell in enumerated
        dest cell group.
        ISSUE:  a prob 1 connect from a cellgroup of, say, size 16 to a
        cell group of size 1 causes 16 connects.  setting prob to e.g.
        1/16 fixes that problem, but be aware that there won't necessarily
        even be one connection made and might be more than one!
        As long as one is made on average that should be OK.
        This only applies to connections made from one enumerated to
        non-enumerated area, not enum to enum.
        """
        c1enum=False
        c2enum=False
        if "_ENUM" in c1.parms:
            if c1.parms["_ENUM"]==True:
                c1enum=True
        if "_ENUM" in c2.parms:
            if c2.parms["_ENUM"]==True:
                c2enum=True
        #print "connecting", c1, "to", c2, c1enum, c2enum, "prob", prob
        if not c1enum and not c2enum:
            # let NCS do allocation from src cellgrp to dest according to probability
            (slay, scellgp, n1)=c1.GetColumnOutput(lays, cells)
            (tlay, tcellgp, n2)=c2.GetColumnInput(lays, cells)
            self.AddConnect(c1, slay, scellgp, "SOMA1_name", c2, tlay, tcellgp, "SOMA1_name", syn, prob, speed)
        elif c1enum and c2enum:
            (slay, scellgpprefix, scellgpsize)=c1.GetEnumColumnOutput(lays, cells)
            (tlay, tcellgpprefix, tcellgpsize)=c2.GetEnumColumnInput(lays, cells)
            #print "enumerated connection from", slay, scellgpprefix, scellgpsize, "to", tlay, tcellgpprefix, tcellgpsize
            # now check all point to point connections and if(prob) make the connection
            for i in range(0, scellgpsize):
                for j in range(0, tcellgpsize):
                    if random.random() < prob:
                        # create the cell group name from the prefix and the group number
                        scellgpname=scellgpprefix+"-"+`i`
                        scellgp=cells[scellgpname]
                        tcellgpname=tcellgpprefix+"-"+`j`
                        tcellgp=cells[tcellgpname]
                        # we've already checked prob ourself, now we force connect with prob=1.0
                        self.AddConnect(c1, slay, scellgp, "SOMA1_name", c2, tlay, tcellgp, "SOMA1_name", syn, 1.0, speed)
        elif not c1enum and c2enum:
            (slay, scellgp, n1)=c1.GetColumnOutput(lays, cells)
            (tlay, tcellgpprefix, tcellgpsize)=c2.GetEnumColumnInput(lays, cells)
            # all connects will be from a multi-cell cellgroup, but we have an enumerated
            # dest group, so we check for n1 connections (n1 is size of src cell group)
            for i in range(0, n1):
                for j in range(0, tcellgpsize):
                    if random.random() < prob:
                        # create the cell group name from the prefix and the group number
                        tcellgpname=tcellgpprefix+"-"+`j`
                        tcellgp=cells[tcellgpname]
                        # we've already checked prob ourself, now we force connect with prob=1.0
                        self.AddConnect(c1, slay, scellgp, "SOMA1_name", c2, tlay, tcellgp, "SOMA1_name", syn, 1.0/float(n1), speed)
        else: # c1enum and not c2enum
            (slay, scellgpprefix, scellgpsize)=c1.GetEnumColumnOutput(lays, cells)
            (tlay, tcellgp, n2)=c2.GetColumnInput(lays, cells)
            # all connections will be (randomly) to same destination multi-cell cell group
            for i in range(0, scellgpsize):
                for j in range(0, n2):
                    if random.random() < prob:
                        # create the cell group name from the prefix and the group number
                        scellgpname=scellgpprefix+"-"+`i`
                        scellgp=cells[scellgpname]
                        # we've already checked prob ourself, now we force connect with prob=1.0
                        self.AddConnect(c1, slay, scellgp, "SOMA1_name", c2, tlay, tcellgp, "SOMA1_name", syn, 1.0/float(n2), speed)

    def AddConnect(self, frm, to, synapse=None, prob=.1, speed=10.0):
        """
        Add a BRAIN-level connect from col frm to col to.

        Uses new style arguments, addressing with GuessConnect().

        NOTE that frmcol, frmlay, etc. can be text names OR variables that point to objects!
        we try to be smart and accept the minimum amount of information
        the minimum required is frmcol and tocol, and from that we may be
        able to figure everything else out (if, for example, there is only one layer
        in the column or if one layer is designated as the _INPUT or _OUTPUT layer)
        """
        if frm is None or to is None:
            print "BRAIN.AddConnect:  you must specify at least frmcol and tocol"
            sys.exit(0) 

        (frmcol, frmlay, frmcell, frmcmp)=self.GuessConnect(frm, inorout='out')
        (tocol, tolay, tocell, tocmp)=self.GuessConnect(to, inorout='in')

        if synapse is None:
            # FIXME:  check for some synapse that is actually present!
            synapse=self.syntypes["C.strong"]
        if prob is None:
            rob="%.4f"%1.0
        if speed is None:
            speed="%.4f"%10.0
        con=(frmcol, frmlay, frmcell, frmcmp, tocol, tolay, tocell, tocmp, synapse, prob, speed)
        self.parms.setdefault("CONNECT", []).append(con)

    def ConnectAreas(self, a1, a2, connecttype, syn, prob, speed, lays, cells):
        """
        (EXPERIMENTAL) Connect two areas together. (Needs to be retested.)

        connect patterns:
        'all'
        'corresponding':  source and dest areas must have same dims.  x,y in src -> x,y in dest
        'random':
        'neighbors-same-minicol':
        'neighbors-other-minicols':

        Pass in two probabilities?
        1:  prob. that we will make a column to column connect here
        this determines how many USE values we keep
        2:  prob. passed to NCS .in file to be used for cell group to cell group connections
        the actual USE value (initial strength of connection) is
        determined by the synapse value passed in

        All routines should work whether src, dst, or both are enumerated or 'normal' NCS cols
        """
        (hx1, hy1, mx1, my1, allcols1)=self.areas[a1]
        (hx2, hy2, mx2, my2, allcols2)=self.areas[a2]

        #print "to connect with ",connecttype+":"
        #print a1, hx1, hy1, mx1, my1
        #print a2, hx2, hy2, mx2, my2
        if connecttype=="all":
            c1i=0
            for sx in range(1, hx1+1):
                for sy in range(1, hy1+1):
                    for smx in range(1, mx1+1):
                        for smy in range(1, my1+1):
                            c1=allcols1[c1i]
                            c2i=0
                            for tx in range(1, hx2+1):
                                for ty in range(1, hy2+1):
                                    for tmx in range(1, mx2+1):
                                        for tmy in range(1, my2+1):
                                            #print c2i, tx, ty, tmx, tmy
                                            c2=allcols2[c2i]
                                            self.ColumnConnect(c1, c2, lays, cells, syn, prob, speed)
                                            c2i=c2i+1
                            c1i=c1i+1 

        elif connecttype=="corresponding":
            if hx1 != hx2 or hy1 != hy2 or mx1 != mx2 or my1 != my2:
                print "dimensions of areas must equal exactly for connect type", connecttype, a1, a2
                sys.exit(0)     # or just return failure?
            c1i=0
            for sx in range(1, hx1+1):
                for sy in range(1, hy1+1):
                    for smx in range(1, mx1+1):
                        for smy in range(1, my1+1):
                            c1=allcols1[c1i]
                            c2=allcols2[c1i]
                            (slay, scellgp, nn)=c1.GetColumnOutput(lays, cells)
                            (tlay, tcellgp, nn)=c2.GetColumnInput(lays, cells)
                            self.AddConnect(c1, slay, scellgp, "SOMA1_name", c2, tlay, tcellgp, "SOMA1_name", syn, prob, speed)
                            c1i=c1i+1 
        else:
            print "unsupported connect type", connecttype
            sys.exit(0)

        self.parms["CONNECT"].append(con)

    def GuessOutput(self, frmcol, frmlay, frmcell, frmcmp):
        """
        Pick a sensible output layer, cell, cmp.

        If items are designated _OUTPUT, use that, of if there is only one candidate pick that

        This general routine might be called for a layer-layer connect
        in a column so col might be None.  That's OK, we just leave
        it as None.

        Conversion from string names to vars is assumed to have already
        taken place, e.g. in GuessConnect.
        """
        if frmlay is None:
            if frmcol is not None and type(frmcol) is not type(""):
                cp=frmcol.parms
                if '__OUTPUT_LAYER' in cp:
                    ln=cp['_OUTPUT_LAYER']
                    frmlay=self.lays[ln]
                else:
                    #print "GuessOutput:  type(frmcol):", type(frmcol), frmcol
                    lays=frmcol.parms['LAYER_TYPE']
                    if len(lays) > 1:
                        print "GuessOutput:  no frmlay was specified, there is no designated _OUTPUT_LAYER in that column, and there is more than one LAYER_TYPE to pick from.  Can't guess."
                        sys.exit(0)
                    frmlay=lays[0]              # NOT a tuple!
            else:
                frmlay=None
        if frmcell is None:
            if frmlay is not None and type(frmlay) is not type(""):
                lp=frmlay.parms
                if '__OUTPUT_CELLGROUP' in lp:
                    cn=lp['_OUTPUT_CELLGROUP']
                    frmcell=self.celltypes[cn]
                else:
                    cells=frmlay.parms['CELL_TYPE']
                    if len(cells) > 1:
                        print "GuessOutput:  no frmcell was specified, there is no designated _OUTPUT_CELLGROUP in the layer, and there is more than one CELL_TYPE cell group to pick from.  Can't guess."
                        sys.exit(0)
                    k=cells.keys()[0]          # hash, NOT a list!
                    (frmcell, n)=cells[k]      # a tuple!
            else:
                frmcell=None
        if frmcmp is None:
            if frmcell is not None and type(frmcell) is not type(""):
                cp=frmcell.parms
                if '_OUTPUT_COMPARTMENT' in cp:
                    cn=cp['_OUTPUT_COMPARTMENT']
                    frmcmp=self.comptypes[cn]
                else:
                    cmps=frmcell.parms['COMPARTMENT']
                    if len(cmps) > 1:
                        print "GuessOutput:  no frmcmp was specified, there is no designated _OUTPUT_COMPARTMENT in the cell, and there is more than one COMPARTMENT to pick from.  Can't guess."
                        sys.exit(0)
                    (frmcmp, cmplabel, x, y, z)=cmps[0]     # list, NOT a hash!  tuple!
                # convert compartment vars to strings (see comment at top of file)
                frmcmp=frmcmp.parms["TYPE"]+"_name"
            else:
                frmcmp=None
        return (frmcol, frmlay, frmcell, frmcmp)

    def GuessInput(self, tocol, tolay, tocell, tocmp):
        """
        Pick a sensible input layer, cell, cmp

        If items are designated _INPUT, use that, or if there is only one candidate pick that.

        This general routine might be called for a layer-layer connect
        in a column so col might be None.  That's OK, we just leave
        it as None.

        Conversion from string names to vars is assumed to have already
        taken place, e.g. in GuessConnect.
        """
        if tolay is None:
            if tocol is not None and type(tocol) is not type(""):
                cp=tocol.parms
                if '_INPUT_LAYER' in cp:
                    ln=cp['_INPUT_LAYER']
                    tolay=self.lays[ln]
                else:
                    lays=tocol.parms['LAYER_TYPE']
                    if len(lays) > 1:
                        print "GuessInput:  no tolay was specified, there is no designated _INPUT_LAYER in that column, and there is more than one LAYER_TYPE to pick from.  Can't guess."
                        sys.exit(0)
                    tolay=lays[0]       # NOT a tuple
            else:
                tolay=None
        if tocell is None:
            if tolay is not None and type(tolay) is not type(""):
                lp=tolay.parms
                if '_INPUT_CELLGROUP' in lp:
                    cn=lp['_INPUT_CELLGROUP']       # a string
                    tocell=self.celltypes[cn]
                else:
                    cells=tolay.parms['CELL_TYPE']
                    if len(cells) > 1:
                        print "GuessInput:  no tocell was specified, there is no designated _INPUT_CELLGROUP in the layer, and there is more than one CELL_TYPE cell group to pick from.  Can't guess."
                        sys.exit(0)
                    k=cells.keys()[0]
                    (tocell, n)=cells[k]        # hash, tuple!
            else:
                tocell=None
        if tocmp is None:
            if tocell is not None and type(tocell) is not type(""):
                cp=tocell.parms
                if '_INPUT_COMPARTMENT' in cp:
                    cn=cp['_INPUT_COMPARTMENT']
                    tocmp=self.comptypes[cn]
                else:
                    cmps=tocell.parms['COMPARTMENT']    # a string
                    if len(cmps) > 1:
                        print "GuessInput:  no tocmp was specified, there is no designated _INPUT_COMPARTMENT in the cell, and there is more than one COMPARTMENT to pick from.  Can't guess."
                        sys.exit(0)
                    (tocmp, cmplabel, x, y, z)=cmps[0]     # list, NOT a hash!  tuple!
                # convert compartment vars to strings (see comment at top of file)
                tocmp=tocmp.parms["TYPE"]+"_name"
            else:
                tocmp=None
        return (tocol, tolay, tocell, tocmp)

    def AddStimInject(self, s):
        """
        Puts a STIMULUS_INJECT param in the BRAIN for given stimulus.

        s should be the *variable* that contains the actual stimulus of the requested type
        """
        # set up default TYPE names if they are not defined
        if 'TYPE' not in s.parms:
            s.parms['TYPE']="autostiminj%d"%self.autostiminjnum
            self.autostiminjnum+=1
        # try to set the referenced STIM's TYPE if it isn't set, too:
        if 'STIM_TYPE' in s.parms:
            stim=s.parms['STIM_TYPE']
            #print 'STIM_TYPE is in stiminject parms, set to type', type(stim)
            if type(stim)!=type(""):        # then assume it is a STIMULUS instance
                # why can't we type(BRAIN.STIMULUS) is 'classobj' not 'instance'.  hmm. 
                #print 'it is a STIMULUS type instance', type(BRAIN.STIMULUS)
                if 'TYPE' not in stim.parms:
                    stim.parms['TYPE']="autostim%d"%self.autostimnum
                    self.autostimnum+=1
            # stim could be a string, probably . . . 
        self.parms.setdefault("STIMULUS_INJECT", []).append(s)

    def AddSpikeStim(self, addr, spikelist, stimname=None, cmp=None):
        """
        Adds a CURRENT pulse STIMULUS block to force a spike at each time in spikelist (given in secs).
        """
        #(col, lay, cell, cmp)=self.GuessConnect(addr, inorout='in')
        #if col is None or lay is None or cell is None or cmp is None:
        #    print "AddSpikeStim:  can't guess target for stimulus, supply more information"
        #    sys.exit(0)
        if stimname is None:
            stimname="autostim%d"%self.autostiminjnum
            self.autostiminjnum+=1
        #self.AddSpikeTrainPulseStim(stimname, addr, spikelist, StringOrVar(cmp))
        self.AddSpikeTrainPulseStim(stimname, addr, spikelist, cmp=cmp)

    #def AddSpikeTrainPulseStim(self, stimname, area, layer, cellgrp, spikelist, cmp=None):
    def AddSpikeTrainPulseStim(self, stimname, addr, spikelist, cmp=None):
        """
        Create stimulus into addr at the times (in sec) given in spikelist.

        NOTE:  This is an older interface.  Recommend use of AddSpikeStim() instead,
        since that takes the new uniform addressing approach.

        addr is the usual tuple addressing where the stim should be applied.
        If portions of the addr are not supplied, they will be guessed using GuessConnect()

        A separate STIMULUS mode PULSE block will be defined for each spike in spikelist.

        This will take up more space in the .in file than using a FileStim (see AddSpikeTrainFileStim)
        but does not require a separate file to contain the stim, and allows 

        Assumes compartment to apply stim is named "SOMA1_name" if it cannot be guessed.
        """
        (area, layer, cellgrp, cmp)=map(StringOrVar, self.GuessConnect(addr, inorout='in'))
        if cmp is None:
            cmp='SOMA1_name'
        sn=0
        for s in spikelist:
            stim_args={}
            stim_args["TYPE"]=stimname+"-"+`sn`
            stim_args["MODE"]="CURRENT"
            stim_args["PATTERN"]="PULSE"
            stim_args["TIMING"]="EXACT"
            stim_args["SAMESEED"]="NO"
            ampstart=10.0; ampend=10.0; width=0.001
            stim_args["AMP_START"]=ampstart
            stim_args["AMP_END"]=ampend
            stim_args["WIDTH"]=width
            starttime=s; endtime=s+width; freqstart=1.0
            stim_args["TIME_START"]=starttime
            stim_args["TIME_END"]=endtime
            stim_args["FREQ_START"]=freqstart
            stim=self.STIMULUS(stim_args)

            stimi_args={}
            stimi_args["TYPE"]=stimname+"-inj"+"-"+`sn`
            stimi_args["STIM_TYPE"]=stim
            #print area, layer, cellgrp, cmp
            stimi_args["INJECT"]=area+" "+layer+" "+cellgrp+" "+cmp+" 1.0"
            #print "did AddSpikeTrainPulseStim to ", stimi_args["INJECT"]; sys.exit(0)
            stimi=self.STIMULUS_INJECT(stimi_args)

            self.AddStimInject(stimi)
            sn+=1

    def AddSpikeTrainFileStim(self, stimname, area, layer, cellgrp, spikelist):
        """
        Create a stimulus file that applies a current spike at the times in spikelist and arrange for that file to be applied.

        The file will contain a probability 1.0, at
        the indicated time, for the application of a CURRENT spike
        sufficient to cause any reasonable cell to fire.  Because
        of the NCS FIREWIND (firewindos) limitation, we force
        the TIME_INCREMENT to be the smallest usable value,
        .0025 seconds, which limits the resolution of the spike
        applications. 

        Another way of doing this would be to create a separate PULSE
        stim for each pulse in the list.  The .in file could end up
        with thousands of PULSE STIMULUS blocks.  Probably impractical
        but the timing would be more precise.  AddSpikeTrainPulseStim
        will do things this way.

        FIXME:  change to use new GuessInput tuple addressing.

        FIXME:  currently CELLS_PER_FREQ hardcoded to 1 . . . 

        NOTE:  a TIME_INCREMENT of less than .0025 (the FIREWIND
        firewindow value) does not work.  It is as if the stimulus
        is not applied
        """
        if not spikelist: return
        stim_args={}
        stim_args["TYPE"]=stimname
        stim_args["MODE"]="CURRENT"
        #stim_args["MODE"]="VOLTAGE"
        stim_args["PATTERN"]="FILE_BASED"
        stim_args["FILENAME"]=spikelist     # when brain is printed, this will be converted to a data file
        tfi=0.0025
        cellsperfreq=1
        stim_args["TIME_INCREMENT"]="%.4f 1.0" % tfi
        stim_args["CELLS_PER_FREQ"]=`cellsperfreq`
        stim_args["TIMING"]="EXACT"
        stim_args["FREQ_COLS"]=1
        stim_args["SAMESEED"]="NO"
        ampstart=10.0
        ampend=10.0
        width=.001
        stim_args["AMP_START"]=`ampstart`
        stim_args["AMP_END"]=`ampend`
        stim_args["WIDTH"]=`width`
        dynrangelo=0
        #dynrangehi=80
        dynrangehi=1000         # this param shouldn't really matter
        stim_args["DYN_RANGE"]=`dynrangelo`+" "+`dynrangehi`
        # maybe not great to set this up here
        #(starttime, endtime)=dur
        freqstart=9999
        starttime=0.0
        # NOTE:  without the +width on the following line, the spike doesn't get applied for
        # its full width and therefore might not trigger a spike
        endtime=spikelist[-1]+tfi+width       # make sure last spike is used
        stim_args["FREQ_START"]=freqstart
        stim_args["TIME_START"]=starttime
        stim_args["TIME_END"]=endtime
        stim=self.STIMULUS(stim_args)

        stimi_args={}
        stimi_args["TYPE"]=stimname+"-inj"
        stimi_args["STIM_TYPE"]=stim
        stimi_args["INJECT"]=area+" "+layer+" "+cellgrp+" "+"SOMA1_name 1.0"
        stimi=self.STIMULUS_INJECT(stimi_args)

        self.AddStimInject(stimi)

    def AddSimpleStim(self, stimname, col, stimtype,
                        freqcols=None, cellsperfreq=None, timefreqinc=None, vert=None,
                        ampstart=None, ampend=None, width=None, freqstart=None, phase=None,
                        dur=(0.0, 1.0), dynrange=(0, 200), port=None, ip=None, filename=None,
                        rate=None, tau=None, corr=None, var=None, seed=None, pattern='NOISE',
                        prob=1.0):
        """
        Add a stim to the BRAIN.

        Changed to use new tuple addressing.
        """
        stim_args={}
        stim_args["TYPE"]=stimname
        if stimtype[0]=="v" or stimtype[0]=="V":
            stim_args["MODE"]="VOLTAGE"
        elif stimtype[0]=="c" or stimtype[0]=="C":
            stim_args["MODE"]="CURRENT"
        else:
            print "ERROR:  unknown stimtype in AddSimpleStim:", stimtype
            sys.exit(0) 
        if port!=None:
            stim_args["PATTERN"]="INPUT"
            stim_args["PORT"]=`port`
            stim_args["FILENAME"]=ip
            stim_args["FREQ_COLS"]=freqcols
            stim_args["CELLS_PER_FREQ"]=cellsperfreq
            stim_args["TIME_INCREMENT"]=timefreqinc+" "+"1.000000"
        elif pattern=="SINE":
            stim_args["PATTERN"]="SINE"
            stim_args["VERT_TRANS"]=`vert`
        elif pattern=="NOISE":
            stim_args["PATTERN"]="NOISE"
            stim_args["RATE"]=`rate`
            stim_args["TAU_NOISE"]=`tau`
            stim_args["CORREL"]=`corr`
            stim_args["SEED"]=`seed`
        elif pattern=="ONGOING":
            stim_args["PATTERN"]="ONGOING"
            stim_args["RATE"]=`rate`
            stim_args["TAU_NOISE"]=`tau`
            stim_args["CORREL"]=`corr`
            stim_args["VAR"]=`var`
            stim_args["SEED"]=`seed`
        elif pattern=="PULSE":
            stim_args["PATTERN"]="PULSE"
        elif pattern=='LINEAR':
            stim_args["PATTERN"]="LINEAR"
        else:
            print "ERROR:  pattern", pattern,"stims currently unsupported in AddSimpleStim"
            sys.exit(0) 
        (dynrangelo, dynrangehi)=dynrange
        if freqstart is not None:
            stim_args["FREQ_START"]=`freqstart`
        if dynrangelo and dynrangehi:
            stim_args["DYN_RANGE"]=`dynrangelo`+" "+`dynrangehi`
        stim_args["TIMING"]="EXACT"
        stim_args["SAMESEED"]="NO"
        if ampstart is not None:
            stim_args["AMP_START"]=`ampstart`
        if ampend is not None:
            stim_args["AMP_END"]=`ampend`
        if width is not None:
            stim_args["WIDTH"]=`width`
        (starttime, endtime)=dur
        stim_args["TIME_START"]=`starttime`
        stim_args["TIME_END"]=`endtime`
        stim=self.STIMULUS(stim_args)

        (col, layer, cellgrp, cmp)=map(StringOrVar, self.GuessConnect(col, inorout='in'))
        stimi_args={}
        stimi_args["TYPE"]=stimname+"-inj"
        stimi_args["STIM_TYPE"]=stim
        stimi_args["INJECT"]=col+" "+layer+" "+cellgrp+" "+cmp+" "+("%1.6f" % prob)
        stimi=self.STIMULUS_INJECT(stimi_args)

        self.AddStimInject(stimi)

    def AddFileBasedDirectStim(self, stimname, col, stimtype,
                        freqrows=None, cellsperfreq=None, timing='EXACT',  sameseed='NO', dur=(0.0, 1.0),
                        filename=None, pattern='FILE_BASED_DIRECT', prob=1.0):
        """
        Add a file based direct stim to the BRAIN.
        Changed to use new tuple addressing.
        """
        stim_args={}
        stim_args["TYPE"]=stimname
        if stimtype[0]=="v" or stimtype[0]=="V":
            stim_args["MODE"]="VOLTAGE"
        elif stimtype[0]=="c" or stimtype[0]=="C":
            stim_args["MODE"]="CURRENT"
        else:
            print "ERROR:  unknown stimtype in AddFileBasedDirectStim:", stimtype
            sys.exit(0) 
        stim_args["PATTERN"]=pattern
        stim_args["FILENAME"]=filename
        stim_args["FREQ_COLS"]=freqrows
        stim_args["CELLS_PER_FREQ"]=cellsperfreq
        stim_args["SAMESEED"]=sameseed
        stim_args["TIMING"]=timing
        (starttime, endtime)=dur
        stim_args["TIME_START"]=`starttime`
        stim_args["TIME_END"]="%.7s"%`endtime`

        stim=self.STIMULUS(stim_args)
        (col, layer, cellgrp, cmp)=map(StringOrVar, self.GuessConnect(col, inorout='in'))
        stimi_args={}
        stimi_args["TYPE"]=stimname+"-inj"
        stimi_args["STIM_TYPE"]=stim
        stimi_args["INJECT"]=col+" "+layer+" "+cellgrp+" "+cmp+" "+("%1.6f" % prob)
        stimi=self.STIMULUS_INJECT(stimi_args)

        self.AddStimInject(stimi)

    def AddFileBasedStim(self, stimname, col, stimtype,
                        freqrows=None, cellsperfreq=None, timefreqinc=None, timing='EXACT', sameseed='NO',
                        ampstart=None, ampend=None, width=None, freqstart=None, dur=(0.0, 1.0), dynrange=(0, 200),
                        filename=None, pattern='FILE_BASED', prob=1.0,port=0):
        """
        Add a file based stim to the BRAIN.
        Changed to use new tuple addressing.
        """
        stim_args={}
        stim_args["TYPE"]=stimname
        if stimtype[0]=="v" or stimtype[0]=="V":
            stim_args["MODE"]="VOLTAGE"
        elif stimtype[0]=="c" or stimtype[0]=="C":
            stim_args["MODE"]="CURRENT"
        else:
            print "ERROR:  unknown stimtype in AddFileBasedStim:", stimtype
            sys.exit(0) 
        stim_args["PATTERN"]=pattern
        stim_args["FILENAME"]=filename
        stim_args["PORT"]=port
        stim_args["TIME_INCREMENT"]=timefreqinc
        stim_args["FREQ_COLS"]=freqrows
        stim_args["CELLS_PER_FREQ"]=cellsperfreq
        (dynrangelo, dynrangehi)=dynrange
        if dynrangelo is not None and dynrangehi is not None:
            stim_args["DYN_RANGE"]=`dynrangelo`+" "+`dynrangehi`
        stim_args["TIMING"]=timing
        stim_args["SAMESEED"]=sameseed
        if ampstart is not None:
            stim_args["AMP_START"]=`ampstart`
        if ampend is not None:
            stim_args["AMP_END"]=`ampend`
        if width is not None:
            stim_args["WIDTH"]=`width`
        (starttime, endtime)=dur
        stim_args["TIME_START"]=`starttime`
        stim_args["TIME_END"]="%.7s"%`endtime`

        if freqstart is not None:
            stim_args["FREQ_START"]=`freqstart`

        stim=self.STIMULUS(stim_args)
        (col, layer, cellgrp, cmp)=map(StringOrVar, self.GuessConnect(col, inorout='in'))
        stimi_args={}
        stimi_args["TYPE"]=stimname+"-inj"
        stimi_args["STIM_TYPE"]=stim
        stimi_args["INJECT"]=col+" "+layer+" "+cellgrp+" "+cmp+" "+("%1.6f" % prob)
        stimi=self.STIMULUS_INJECT(stimi_args)

        self.AddStimInject(stimi)

    def AddReport(self, r):
        """
        Put a REPORT in the BRAIN section of the .in file for report r.
        """
        self.parms.setdefault("REPORT", []).append(r)

    def AddEvent(self, e):
        """
            Put a EVENT in the BRAIN section of the .in file for event e.
        """
        self.parms.setdefault("EVENT", []).append(e)

    def GuessConnect(self, addr, inorout="out"):
        """
        Return explicit address of the possibly only partially specified brain address in 'to'.

        The addr can be a simple string or variable, in which case it is taken to refer to a
        column by name or by variable.  Otherwise it is a tuple of (col, lay),
        (col, lay, cellgroup), or (col, lay, cellgroup, compartment).
        If partially specified, we guess the likely connection point (or only connection point) and
        fail if we can't guess.

        The addr might be specified using string names of connection
        points or variables or a mixture.

        Returns all items as vars (CONFIRM) except for compname
        which is a string.

        If inorout is 'out', try to pick likely output candidates
        from partially specified addresses.  Otherwise, try to pick likely input candidates

        Maybe rework this to use named parms, then callers wouldn't spend so much
        time remapping args. 
        """
        # extract info from (possible) tuple, or string
        if type(addr)==type(()) or type(addr)==type([]):
            if len(addr)==2:
                (col, lay)=addr
                cell=None
                cmp=None
            elif len(addr)==3:
                (col, lay, cell)=addr
                cmp=None
            elif len(addr)==4:
                (col, lay, cell, cmp)=addr
        else:   # just a column, guess the rest
            col=addr
            lay=None
            cell=None
            cmp=None 

        # convert any items that are string names to variables, via hashes in brain
        if type(col)==type(""):
            col=self.cols[col]    
        if type(lay)==type(""):
            lay=self.lays[lay]    
        if type(cell)==type(""):
            cell=self.celltypes[cell]
        if type(cmp)==type(""):
            cmp=self.comptypes[cmp]

        if inorout=='out':
            return self.GuessOutput(col, lay, cell, cmp)
        return self.GuessInput(col, lay, cell, cmp)

    def AddSeedLessSimpleReport(self, repname, addr, reptype='v', satype='', freq=1, port=None, ip="134.197.40.155", prob=1.0, dur=(0.0, 1.0), synname=None, format='ASCII'):
        """
            Compatibility function.  Simple calls AddSimpleReport() with same params plus seed=None
        """
        return AddSimpleReport(self, repname, addr, reptype, freq, port, ip, prob, dur, synname, format, seed=None)

    def AddSimpleReport(self, repname, addr, reptype='v', freq=1, port=None, ip="134.197.40.155", prob=1.0, dur=(0.0, 1.0), synname=None, format='ASCII', seed="SELECT_FRONT"):
        """
        This is an easier interface to use than AddReport.

        It doesn't require any knowledge of NCS .in file syntax and keywords.
        Arguments can be either variables that contain the object you are
        reporting on, or string names of those items.  (CHECK THIS)

        Uses the unified column addressing scheme (GuessConnect).

        reptype is report type, 'v' for voltage, 'c' for current, 'a' for
        SYNAPSE_USE, 'r' for SYNAPSE_RSE (add more later).

        filename for report will be brainname-repname.txt
        (NCS itself prepends brainname to reports.)
        """
        (col, lay, cellgrp, compname)=self.GuessConnect(addr)

        rep_args={}
        rep_args["TYPE"]=repname
        if seed is not None:
            rep_args["SEED"]=seed
        rep_args["CELLS"]="%s %s %s %s" %(StringOrVar(col), StringOrVar(lay), StringOrVar(cellgrp), StringOrVar(compname))
        rep_args["PROB"]="%.3f" % prob
        #rt=reptype[0]
        rt=reptype
        if rt=='v' or rt=="V":
            rep_args["REPORT_ON"]="VOLTAGE"
        elif rt=='fc':
            rep_args["REPORT_ON"]="FIRE_COUNT"
        elif rt=='c' or rt=='C':
            # NCS was changed some time back and there is no "CURRENT" report, now there is
            # a group of CURRENT reports NET_CURRENT, SYN_CURRENT, LEAK_CURRENT and more
            rep_args["REPORT_ON"]="NET_CURRENT"
            #rep_args["REPORT_ON"]="CURRENT"
        elif rt=='s' or rt=='S':
            rep_args["REPORT_ON"]="SYN_CURRENT"
        elif rt=='a' or rt=='A':
            # docs say an absolute USE report doesn't need a REPORT_ON parm
            if synname is None:
                print "AddSimpleReport:  absolute USE report requires synapse name (synname= parameter)"
                # shouldn't GuessConnect pick a synapse too?  think about that
                sys.exit(0)
            rep_args["REPORT_ON"]="SYNAPSE_USE"     # possibly unnecessary, but does not cause syntax error
            rep_args["SYNAPSE"]=synname
        elif rt=='r' or rt=='R' or rt=='u' or rt=='U':
            if synname is None:
                print "AddSimpleReport:  RSE report requires synapse name (synname= parameter)"
                # shouldn't GuessConnect pick a synapse too?  think about that
                sys.exit(0)
            # an RSE report doesn't need a REPORT_ON parm
            #rep_args["REPORT_ON"]="SYNAPSE_RSE"     # gives syntax error; docs say not required but *can't* be provided
            rep_args["SYNAPSE_RSE"]=synname
        elif rt=='f':
            if synname is None:
                print "AddSimpleReport:  SYNAPSE_UF report requires synapse name (synname= parameter)"
                sys.exit(0)
            rep_args["SYNAPSE_UF"]=synname
        elif rt=='sc':
            rep_args["REPORT_ON"]="STIM_CURRENT"
        elif rt=='sa':
            rep_args["SYN_AUGMENTATION"]=satype
            rep_args["OPTION"]="AVERAGE_SYN"
        else:
            print "AddSimpleReport:  report type",rt,"unknown.  Exiting."
            sys.exit(0)
        if port!=None:
            rep_args["FILENAME"]=ip
            rep_args["PORT"]=`port`
        else:
            filename=repname+".txt" 
            rep_args["FILENAME"]=filename
        rep_args["FREQUENCY"]=freq
        if format=='ASCII':
            rep_args["ASCII"]=""
        elif format=='EXP':
            rep_args["ASCII"]="EXP"
        (starttime, endtime)=dur
        rep_args["TIME_START"]="%.5f" % float(starttime)
        rep_args["TIME_END"]="%.5f" % float(endtime)
        rep=self.REPORT(rep_args)

        self.AddReport(rep)
        return rep

    def AddSimpleEvent(self, eventname, addr, starttime, synname=None, usefile=None):
        """
        This is an easier interface to use than AddEvent.

        It doesn't require any knowledge of NCS .in file syntax and keywords.
        Arguments can be either variables that contain the object you are
        reporting on, or string names of those items.  (CHECK THIS)

        Uses the unified column addressing scheme (GuessConnect).

        filename for report will be brainname-repname.txt
        (NCS itself prepends brainname to reports.)
        """
        (col, lay, cellgrp, compname)=self.GuessConnect(addr)

        event_args={}
        event_args["TYPE"]=eventname
        event_args["CELLS"]="%s %s %s %s" %(StringOrVar(col), StringOrVar(lay), StringOrVar(cellgrp), StringOrVar(compname))
        if synname!=None:
            event_args["SYNAPSE"]=synname
        if usefile!=None and starttime>=0:
            event_args["USE_OVERRIDE"]="%s             %.5f" %((usefile), float(starttime))
        event=self.EVENT(event_args)

        self.AddEvent(event)
        return event

    def Copy(self, container, fromtype, newtype):
        """
        Return an independently modifiable copy of supplied element named 'fromtype' into name 'newtype' in container.

        This makes it easy to create a base type of something (like a cell)
        and then make variants of that base type.
        Usually after making a copy, the caller will then add the element
        to the appropriate containter for that object type, e.g.:
        cn=newb.Copy(comptypes["SOMA1"]) 
        comptypes[compname]=cn

        We don't actually want to do a deepcopy since that can create multiple
        variable instances of referenced objects with the same underlying TYPE names
        and cause both instances to be emitted during brain print, leading to duplicate
        symbol errors.  Not really necessary, anyway.  We DO also need to make a copy of the
        parms dict though, but not the individual elements in the parms array.  If we
        don't copy the parms array then it will be shared, which is obviously bad.
        """
        #n=copy.deepcopy(container[fromtype])
        if type(fromtype)==type(""):
            n=copy.copy(container[fromtype])
            n.parms=copy.copy(container[fromtype].parms)
        else:       # it had better be a variable in the container, or at least the same type!
            n=copy.copy(fromtype)
            n.parms=copy.copy(fromtype.parms)
        n.parms["TYPE"]=newtype
        #print "n.parms is:", n.parms
        #print "n.parms TYPE is:", n.parms["TYPE"]
        container[newtype]=n
        return n

    def SelectLib(self, libname):
        """
        Allow user to set the current component library from the set of defined libs.
        """
        lib=self.libs[libname]
        self.chantypes=lib['chantypes']
        self.spks=lib['spks']
        self.comptypes=lib['comptypes']
        self.celltypes=lib['celltypes']
        self.spsgs=lib['spsgs']
        self.sfds=lib['sfds']
        self.sls=lib['sls']
        self.sas=lib['sas']
        self.syntypes=lib['syntypes']
        self.lays=lib['lays']
        self.cols=lib['cols']

    def StandardStuff(self, maxcond=0.0024, epsc=None, ipsc=None):
        """
        Return a set of standard channel types, spikes, compartment types, ...

        Rename this.
        """
        ln='standard'
        lib={}
        lib['chantypes']=self.StandardChannels()
        lib['spks']=self.StandardSpikes()
        lib['comptypes']=self.StandardCompartments(lib['spks'], lib['chantypes'])
        lib['celltypes']=self.StandardCells(lib['comptypes'])
        lib['spsgs']=self.StandardPSGs(epsc, ipsc)
        lib['sfds']=self.StandardSFDs()                 # syn facil and depression profiles
        lib['sls']=self.StandardSLs()                   # syn learning profiles
        lib['sas']=self.StandardSAs()                   # syn augmentation profiles
        lib['syntypes']=self.StandardSynapses(lib['spsgs'], lib['sls'], lib['sfds'], lib['sas'], maxcond=maxcond)
        # this is a bit tricky.  normally layers must be added to a column before connects are made
        # in this case, we don't have any columns since they don't really have a type-of abstraction
        # we'll hack it by sending in brain as an argument!
        lib['lays']=self.StandardLayers(lib['syntypes'], lib['celltypes'])     # change to laytypes
        lib['cols']={}

        self.libs[ln]=lib
        self.SelectLib('standard')
        return (self.chantypes, self.spks, self.comptypes, self.celltypes, self.spsgs, self.sfds, self.sls, self.sas, self.syntypes, self.lays)

    class SPIKESHAPE:
        pt=["TYPE", "VOLTAGES"]
        parms={}

        def __init__(self, parms):
            self.parms=InitParms(parms, self.pt)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "SPIKESHAPE")

    class SYN_PSG:
        pt=["TYPE", "PSG_FILE"]
        parms={}

        def __init__(self, parms):
            self.parms=InitParms(parms, self.pt)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "SYN_PSG")

    class SYN_FACIL_DEPRESS:
        pt=["TYPE", "SFD", "FACIL_TAU", "DEPR_TAU"]
        parms={}

        def __init__(self, parms):
            self.parms=InitParms(parms, self.pt)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "SYN_FACIL_DEPRESS")

    class SYN_LEARNING:
        pt=["TYPE", "LEARNING", "LEARNING_SHAPE", "NEG_HEB_WINDOW", "NEG_HEB_PEAK_DELTA_USE", "NEG_HEB_PEAK_TIME",
             "POS_HEB_WINDOW", "POS_HEB_PEAK_DELTA_USE", "POS_HEB_PEAK_TIME"]
        parms={}

        def __init__(self, parms):
            self.parms=InitParms(parms, self.pt)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "SYN_LEARNING")

    class SYN_AUGMENTATION:
        pt=["TYPE", "AUGMENTATION_DELAY", "AUGMENTATION_INIT", "AUGMENTATION_TAU", "MAX_AUGMENTATION",
             "CA_INTERNAL", "CA_SPIKE_INCREMENT", "CA_TAU", "ALPHA"]
        parms={}

        def __init__(self, parms):
            self.parms=InitParms(parms, self.pt)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "SYN_AUGMENTATION")

    class SYNAPSE:
        pt=["TYPE", "SYN_PSG", "SYN_REVERSAL", "LEARN_LABEL", "ABSOLUTE_USE",
            "PREV_SPIKE_RANGE", "SFD_LABEL", "SYN_AUGMENTATION", "RSE_INIT", "MAX_CONDUCT", "DELAY", "HEBB_START", "HEBB_END"]
        parms={}

        def __init__(self, parms):
            self.parms=InitParms(parms, self.pt)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "SYNAPSE")

    class STIMULUS_INJECT:
        pt=["TYPE", "STIM_TYPE", "INJECT"]
        parms={}

        def __init__(self, parms={}):
            self.parms=InitParms(parms, self.pt)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "STIMULUS_INJECT")

    class STIMULUS:
        pt=["TYPE", "MODE", "PATTERN", "PORT", "FILENAME", "FREQ_COLS", "CELLS_PER_FREQ",
            "TIME_INCREMENT", "DYN_RANGE", "TIMING", "SAMESEED", "AMP_START", "AMP_END",
            "WIDTH", "FREQ_START", "TIME_START", "TIME_END", "VERT_TRANS", "PHASE", "RATE",
            "TAU_NOISE", "VAR", "CORREL", "SEED"]
        parms={}

        def __init__(self, parms={}):
            self.parms=InitParms(parms, self.pt)

        def __repr__(self):
            # before calling generic PrintParms, check for special FILENAMEs that contain
            # a list of spikes to be written to a file and used to trigger spike stimuli 
            if "FILENAME" in self.parms:
                if type(self.parms["FILENAME"])==type([]):
                    tfi=float(self.parms["TIME_INCREMENT"].split()[0])
                    s=self.parms["FILENAME"]
                    fn=self.parms["TYPE"]+".stm"
                    self.parms["FILENAME"]=fn
                    # TIME_INCREMENT specifies how much time each sample corresponds to
                    #print "printing out stimulus, and found a list.  creating file FINISHME"
                    # compute time start and time end based on last element in list and BRAIN's FSV?
                    # create stim file.  look at TIME_INC to see how to create file?
                    # FIXME:  currently ignoring TIME_START and TIME_END . . .
                    # FIXME:  currently ignoring DYN_RANGE--do we need this?  we'll see . . . 
                    if int(self.parms["FREQ_COLS"])!= 1:
                        print "In class STIMULUS __repr__:  FREQ_COLS currently must be 1 for spike train stim files"
                        sys.exit(0)
                    f=open(fn, "w")
                    i=0; el=len(s)
                    t=0.0
                    endstim=float(self.parms["TIME_END"])
                    #if el> 0: endstim=s[-1]
                    #else: endstim=0.0
                    #print "endstim is", endstim
                    #endstim+=tfi       # to make sure last stim shows up; FIXME
                    while (t < endstim) and (i < el):
                        if t >= s[i]:
                            print >>f, "1.0"        # spike prob is 1.0
                            i+=1
                        else:
                            print >>f, "0.0"        # no spike
                        t+=tfi
                    f.close()
            return PrintParms(self.pt, self.parms, "STIMULUS")

    class REPORT:
        pt=["TYPE", "SEED", "CELLS", "PROB", "REPORT_ON", "SYNAPSE", "SYNAPSE_RSE", "SYN_AUGMENTATION", "OPTION",
            "FILENAME", "PORT", "FREQUENCY", "ASCII", "TIME_START", "TIME_END"]

        def __init__(self, parms={}):
            self.parms=InitParms(parms, self.pt)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "REPORT")

    class EVENT:
        pt=["TYPE", "CELLS", "SYNAPSE", "USE_OVERRIDE"]

        def __init__(self, parms={}):
            self.parms=InitParms(parms, self.pt)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "EVENT")

    class COLUMN:
        pt=["TYPE", "COLUMN_SHELL", "LAYER_TYPE", "CONNECT", "_WIDTH", "_HEIGHT", "_XLOC", "_YLOC", "_INPUT_LAYER", "_OUTPUT_LAYER", "_ENUM"]

        def __init__(self, parms={}):
            self.parms=InitParms(parms, self.pt)

        def AddLayerType(self, layer):
            """
                Really should be AddLayer not AddLayerType; however keeping consistent with NCS for now.
            """
            b=self.brain            # get brain from column
            layer.brain=b
            ln=layer.parms["TYPE"]
            b.lays[ln]=layer
            if type(layer)==type(""):
                print "WARNING:  COLUMN.AddLayerType was passed a string, not a LAYER"
            self.parms.setdefault("LAYER_TYPE", []).append(layer)

        def AddConnect(self, frm, to, syn="INVALIDSYNAPSE", prob=.1, speed=10.0):
            """ New version that supports tuple polymorphism
                FIXME:  add syn, prob, speed defaults

                GuessOutput requires brain, since brain contains celltypes etc.
                which are referenced.  But a Column might not even be part of
                a brain at this point . . .
            """
            if self.brain is None:
                print "COLUMN.AddConnect():  you must make the COLUMN part of a BRAIN before adding connections to it"
                sys.exit(0)
            # put a "None" column at the beginning so we can use general address
            # guessing routines
            if type(frm)!=type(()) and type(frm)!=type([]):
                frm=[frm]
            if type(to)!=type(()) and type(to)!=type([]):
                to=[to]
            ffrm=[None]; ffrm.extend(frm)
            tto=[None]; tto.extend(to)
            (frmcol, frmlay, frmcell, frmcmp)=self.brain.GuessConnect(ffrm, inorout='out')
            (tocol, tolay, tocell, tocmp)=self.brain.GuessConnect(tto, inorout='in')

            con=(frmlay, frmcell, frmcmp, tolay, tocell, tocmp, syn, prob, speed)
            self.parms.setdefault("CONNECT", []).append(con)

        def GetColumnOutput(self, lays, cells):
            """ Return the self-identified output layer and output cellgroup for the
                column for *inter column connects*.  Later, will have to have
                ability to get the intra column connects of various types
            """
            slayname=self.parms["_OUTPUT_LAYER"]
            slay=lays[slayname]
            scellgpname=slay.parms["_OUTPUT_CELLGROUP"]
            scellgp=cells[scellgpname]
            ch=slay.parms["CELL_TYPE"]
            (c, n)=ch[scellgpname]
            n=int(n)
            return (slay, scellgp, n)

        def GetEnumColumnOutput(self, lays, cells):
            """ Return the self-identified output layer and output cellgroup for the
                column for *inter column connects*.  Later, will have to have
                ability to get the intra column connects of various types
                returns string *name* of cell group, not cell variable itself
            """
            slayname=self.parms["_OUTPUT_LAYER"]
            slay=lays[slayname]
            scellgpprefix=slay.parms["_OUTPUT_CELLGROUP"]
            h=slay.parms["_CELLGROUP_SIZE"]
            scellgpsize=h[scellgpprefix]
            return (slay, scellgpprefix, scellgpsize)

        def GetColumnInput(self, lays, cells):
            """ Return the self-identified input layer and input cellgroup for the
                column for *inter column connects*.  Later, will have to have
                ability to get the intra column connects of various types
            """
            tlayname=self.parms["_INPUT_LAYER"]
            tlay=lays[tlayname]
            tcellgpname=tlay.parms["_INPUT_CELLGROUP"]
            tcellgp=cells[tcellgpname]
            ch=tlay.parms["CELL_TYPE"]
            (c, n)=ch[tcellgpname]
            n=int(n)
            return (tlay, tcellgp, n)

        def GetEnumColumnInput(self, lays, cells):
            """ Return the self-identified input layer and input cellgroup for the
                column for *inter column connects*.  Later, will have to have
                ability to get the intra column connects of various types
                returns string *name* of cell group, not cell variable itself
            """
            tlayname=self.parms["_INPUT_LAYER"]
            tlay=lays[tlayname]
            tcellgpprefix=tlay.parms["_INPUT_CELLGROUP"]
            h=tlay.parms["_CELLGROUP_SIZE"]
            tcellgpsize=h[tcellgpprefix]
            return (tlay, tcellgpprefix, tcellgpsize)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "COLUMN")

    class LAYER:
        pt=["TYPE", "LAYER_SHELL", "CELL_TYPE", "CONNECT", "_INPUT_CELLGROUP", "_OUTPUT_CELLGROUP", "_UPPER", "_LOWER", "_CELLGROUP_SIZE"]
        """ _CELLGROUP_SIZE is a hash, keyed by the cellgroup prefix, for enumerated
            cell groups where you actually have multiple cell groups of size 1 e.g. exc-1, exc-2
        """

        def __init__(self, parms={}):
            #if "TYPE" not in parms:
            #    # no name supplied, just assign some unique name
            self.parms=InitParms(parms, self.pt)
            self.parms["LAYER_SHELL"]=self.parms["TYPE"]+"_sh"      # temp hack

        def AddCellType(self, celltype, n):
            """
                celltype can be string name of cell type or var that points to cell type
            """
            n=int(n)        # could be passed in as string or int
            ct=(celltype, n)
            if type(celltype)==type(""):
                print "LAYER.AddCellType():  celltype can't be string, must be CELL"
                sys.exit(0)
                #ctname=celltype
            else:
                ctname=celltype.parms["TYPE"]
            self.parms.setdefault("CELL_TYPE", {})[ctname]=ct

        def AddConnect(self, frm, to, synapse, prob=.1, speed=10.0):
            """
            frm and to can be just a cell name string or variable, or
            a tuple that contains (cell, cmp).  If a cmp is not specified
            it is guessed, or set to "SOMA1_name".

            FIXME:  what about mixing vars and strings in tuple?
            The string for cmp would have to be the cmp *label*,
            that is, with _name on the end.  Test.
            Change to use GuessConnect?  Problems with that.  Col may not be set, as in StandardLayers.
            """
            if self.brain is None:
                print "LAYER.AddConnect():  you must make the LAYER part of a COLUMN before adding connections to it"
                sys.exit(0)
            prob=float(prob); speed=float(speed)
            # all this work to use generic GuessConnect()
            if type(synapse)==type(""):
                print "LAYER AddConnect:  synapse can't be a string"
                sys.exit(0)
            if type(frm)==type(()):
                (frmcell, frmcmp) = frm
            else:
                frmcell=frm
                frmcmp=None
                #frmcmp="SOMA1_name"
            if type(to)==type(()):
                (tocell, tocmp) = to
            else:
                tocell=to
                tocmp=None
                #tocmp="SOMA1_name"
            frm=(None, None, frmcell, frmcmp)
            to=(None, None, tocell, tocmp)
            (frmcol, frmlay, frmcell, frmcmp)=self.brain.GuessConnect(frm, inorout='out')
            (tocol, tolay, tocell, tocmp)=self.brain.GuessConnect(to, inorout='in')
            con=(frmcell, frmcmp, tocell, tocmp, synapse, prob, speed) 
            self.parms.setdefault("CONNECT", []).append(con)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "LAYER")

    class CELL:
        pt=["TYPE", "COMPARTMENT", "CONNECT"]

        def __init__(self, parms):
            self.parms=InitParms(parms, self.pt)

        def AddCompartment(self, cmptype, x, y, z=0.0):
            """
                cmptype is a reference to a defined compartment, gives characteristics of that cmp
                cmplabel is what connects are *made to*.  NOTE:  this is now constructed automatically
                from the cmptype by postpending "-name" to the cmptype.  This restricts us to only
                one instance of a compartment type per cell but is more consistent with NCS requirements
                elsewhere.
                cmptype is a *variable*; cmplabel is a *string* since there is no underlying
                object being referenced
                NOTE:  z was added later
            """
            cmplabel=StringOrVar(cmptype)+"_name"
            if type(cmptype)==type(""):
                print "WARNING:  CELL.AddCompartment() was pass a string not a COMPARTMENT"
            cmp=(cmptype, cmplabel, x, y, z)  
            self.parms.setdefault("COMPARTMENT", []).append(cmp)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "CELL")

        def AddConnect(self, frmcmp, tocmp, speed, gfor, grev):
            """
                NOTE that frmcol, frmlay, etc. can be text names OR variables that point to objects!
            """
            if type(speed) is not type(1):
                print "class CELL:  AddConnect:  speed should be an integer"
                sys.exit(0)
            frmcmpname=StringOrVar(frmcmp)+"_name"
            tocmpname=StringOrVar(tocmp)+"_name"
            con=(frmcmpname, tocmpname, speed, gfor, grev)
            self.parms.setdefault("CONNECT", []).append(con)

    class COMPARTMENT:
        """
        DOCUMENT:  in a CELL, there are COMPARTMENT lines (one now, maybe multiple later), like this:
        COMPARTMENT SOMA1 SOMA1_name 0.0 0.0
        the SOMA1 is a COMPARTMENT *TYPE* reference; the SOMA1_name is what connections reference

        DOCUMENT:  multiple CHANNEL items can be present.  pass them as a list
        and each one will be printed separately
        """
        pt=["TYPE", "SPIKESHAPE", "SPIKE_HALFWIDTH", "TAU_MEMBRANE",
            "R_MEMBRANE", "THRESHOLD", "LEAK_REVERSAL", "LEAK_CONDUCTANCE",
            "VMREST", "CA_INTERNAL", "CA_EXTERNAL", "CA_SPIKE_INCREMENT",
            "CA_TAU", "CHANNEL"]

        def __init__(self, parms):
            self.parms=InitParms(parms, self.pt)

        def AddChannel(self, chan):
            self.parms.setdefault("CHANNEL", []).append(chan)

        def DelChannel(self, chan):
            """
            Convenience function.  Can be done directly by manipulation of cmp.parms[] items.
            chan is chan to delete; it can be a CHANNEL variable or a string channel name
            """
            if "CHANNEL" in self.parms:
                chans=self.parms["CHANNEL"]
                #print chans
                for c in chans:
                    if type(chan)==type(""):
                        if c.parms["TYPE"]==chan:
                            chans.remove(c)
                            break
                    elif type(c)==type(chan):
                        if c==chan:
                            chans.remove(c)
                            break;
                    else:
                        print "DelChannel type error"
                        sys.exit(0)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "COMPARTMENT")

    class CHANNEL:
        """
        DOCUMENT:  channels are unusual in that the first line has the family on
        it, e.g.:
        CHANNEL Kahp
        this is an inconsistency within the definition, should have a "FAMILY" flag
        """
        pt=["TYPE", "REVERSAL_POTENTIAL", "M_INITIAL", "M_POWER", "CA_SCALE_FACTOR",
             "CA_EXP_FACTOR", "CA_HALF_MIN", "CA_TAU_SCALE_FACTOR",
             "E_HALF_MIN_M", "SLOPE_FACTOR_M",
             "SLOPE_FACTOR_M_STDEV", "TAU_SCALE_FACTOR_M",
             "V_TAU_VOLTAGE_M", "V_TAU_VOLTAGE_M_STDEV", "V_TAU_VALUE_M",
             "V_TAU_VALUE_M_STDEV", "H_INITIAL", "H_POWER", "E_HALF_MIN_H",
             "SLOPE_FACTOR_H", "SLOPE_FACTOR_H_STDEV", "V_TAU_VOLTAGE_H",
             "V_TAU_VOLTAGE_H_STDEV", "V_TAU_VALUE_H", "V_TAU_VALUE_H_STDEV",
             "UNITARY_G", "STRENGTH"]

        def __init__(self, parms, family):
            self.family=family      # FIXME:  make this part of pt instead of separate var?
            self.parms=InitParms(parms, self.pt)

        def __repr__(self):
            return PrintParms(self.pt, self.parms, "CHANNEL", optarg=self.family)

    def StandardChannels(self):
        """
            Return a standard set of ion channels with common parameters.
        """
        chans={}
        chan_args={}
        chan_args["TYPE"]="ahp-2"
        chan_args["REVERSAL_POTENTIAL"]="-80.000000 0.000000"
        chan_args["M_INITIAL"]="0.300000 0.000000"
        chan_args["M_POWER"]="2.000000 0.000000"
        chan_args["CA_SCALE_FACTOR"]="0.000125 0.000000"
        chan_args["CA_EXP_FACTOR"]="2.000000 0.000000"
        chan_args["CA_HALF_MIN"]="2.500000 0.000000"
        chan_args["CA_TAU_SCALE_FACTOR"]="0.003000 0.000100"
        chan_args["UNITARY_G"]="0.054000 0.000000"
        chan_args["STRENGTH"]="0.200000 0.020000"
        chans["ahp-2"]=self.CHANNEL(chan_args, family="Kahp")

        chan_args={}
        chan_args["TYPE"]="m-1"
        chan_args["REVERSAL_POTENTIAL"]="-80.000000 0.000000"
        chan_args["M_INITIAL"]="0.300000 0.010000"
        chan_args["M_POWER"]="1.000000 0.000000"
        chan_args["E_HALF_MIN_M"]="-44.000000 0.200000"
        chan_args["SLOPE_FACTOR_M"]="40.000000 20.000000 8.800000"
        #chan_args["SLOPE_FACTOR_M_STDEV"]="0.000000"
        chan_args["TAU_SCALE_FACTOR_M"]="0.303000 0.000000"
        chan_args["UNITARY_G"]="0.084000 0.000000"
        chan_args["STRENGTH"]="0.060000 0.002000"
        chans["m-1"]=self.CHANNEL(chan_args, family="Km")

        chan_args={}
        chan_args["TYPE"]="a-1"
        chan_args["REVERSAL_POTENTIAL"]="-80.000000 0.000000"
        chan_args["M_INITIAL"]="0.300000 0.010000"
        chan_args["M_POWER"]="1.000000 0.000000"
        chan_args["E_HALF_MIN_M"]="-21.300000 0.200000"
        chan_args["SLOPE_FACTOR_M"]="35.000000"  # FIXME--3 vals needed?
        chan_args["SLOPE_FACTOR_M_STDEV"]="0.500000"
        #chan_args["TAU_SCALE_FACTOR_M"]="0.303000 0.000000"    # FIXME--need this?
        chan_args["V_TAU_VOLTAGE_M"]="100.000000"
        chan_args["V_TAU_VOLTAGE_M_STDEV"]="0.000000"
        chan_args["V_TAU_VALUE_M"]="0.000200 9999.000000"
        chan_args["V_TAU_VALUE_M_STDEV"]="0.000000"
        chan_args["H_INITIAL"]="0.600000 0.005000"
        chan_args["H_POWER"]="1.000000 0.000000"
        chan_args["E_HALF_MIN_H"]="-58.000000 0.210000"
        chan_args["SLOPE_FACTOR_H"]="8.200000"
        chan_args["SLOPE_FACTOR_H_STDEV"]="0.500000"
        chan_args["V_TAU_VOLTAGE_H"]="-21.000000 -1.000000 10.000000 21.000000"
        chan_args["V_TAU_VOLTAGE_H_STDEV"]="0.000000"
        chan_args["V_TAU_VALUE_H"]="0.005000 0.001000 0.015000 0.020000 0.250000"
        chan_args["V_TAU_VALUE_H_STDEV"]="0.000000"
        chan_args["UNITARY_G"]="0.120000 0.000000"
        chan_args["STRENGTH"]="0.100000 0.002000"
        chans["a-1"]=self.CHANNEL(chan_args, family="Ka")

        return chans

    def StandardSpikes(self):
        """ Return a standard set of spike voltage values (appropriate for FSV=10000).
        """
        spks={}

        spk_args={}
        spk_args["TYPE"]="AP_Hoffman"
        spk_args["VOLTAGES"]="-38.000000 -35.000000 -30.000000 -20.000000 -7.000000 15.000000 30.000000 20.000000 7.000000 -8.000000 -16.000000 -22.000000 -28.000000 -33.000000 -37.000000 -40.000000 -43.000000 -45.000000 -47.000000 -49.000000 -50.000000"
        spks["AP_Hoffman"]=self.SPIKESHAPE(spk_args)

        return spks

    def StandardCompartments(self, spks, chans):
        comptypes={}

        comptype_args={}
        comptype_args["TYPE"]="SOMA1"
        comptype_args["SPIKESHAPE"]=spks["AP_Hoffman"]
        comptype_args["SPIKE_HALFWIDTH"]="10.000000 0.000000"
        comptype_args["TAU_MEMBRANE"]="0.015000 0.000500"
        comptype_args["R_MEMBRANE"]="200.000000 3.000000"
        comptype_args["THRESHOLD"]="-40.000000 1.000000"
        comptype_args["LEAK_REVERSAL"]="0.000000 0.000000"
        comptype_args["LEAK_CONDUCTANCE"]="0.000000 0.000000"
        comptype_args["VMREST"]="-60.000000 1.000000"
        comptype_args["CA_INTERNAL"]="100.000000 0.000000"
        comptype_args["CA_EXTERNAL"]="0.000000 0.000000"
        comptype_args["CA_SPIKE_INCREMENT"]="300.000000 20.000000"
        comptype_args["CA_TAU"]="0.070000 0.001000"
        comptypes["SOMA1"]=self.COMPARTMENT(comptype_args)
        comptypes["SOMA1"].AddChannel(chans["ahp-2"])
        comptypes["SOMA1"].AddChannel(chans["m-1"])
        comptypes["SOMA1"].AddChannel(chans["a-1"])

        return comptypes

    def StandardCell(self, name, cells, comptypes):
        """
        Add to cells hash a standard cell named 'name' containing one standard SOMA1 compartment.
        If cell name already exists, won't add again and won't give error, just returns.
        """
        if name in cells: return cells[name]
        cell_args={}
        cell_args["TYPE"]=name
        cells[name]=self.CELL(cell_args)
        cells[name].AddCompartment(comptypes["SOMA1"], 0.0, 0.0, 0.0)
        return cells[name]

    def StandardCells(self, comptypes):
        # NOTE:  all these cells are identical; probably not right 
        cells={}

        cell_args={}

        cell_args["TYPE"]="E"
        cells["E"]=self.CELL(cell_args)
        cells["E"].AddCompartment(comptypes["SOMA1"], 0.0, 0.0, 0.0)

        cell_args["TYPE"]="ER"
        cells["ER"]=self.CELL(cell_args)
        cells["ER"].AddCompartment(comptypes["SOMA1"], 0.0, 0.0, 0.0)

        cell_args["TYPE"]="ES"
        cells["ES"]=self.CELL(cell_args)
        cells["ES"].AddCompartment(comptypes["SOMA1"], 0.0, 0.0, 0.0)

        cell_args["TYPE"]="I1"
        cells["I1"]=self.CELL(cell_args)
        cells["I1"].AddCompartment(comptypes["SOMA1"], 0.0, 0.0, 0.0)

        cell_args["TYPE"]="I"
        cells["I"]=self.CELL(cell_args)
        cells["I"].AddCompartment(comptypes["SOMA1"], 0.0, 0.0, 0.0)

        return cells

    def StandardPSGs(self, epsc, ipsc):
        spsgs={}

        if epsc==None or ipsc==None:
            print "StandardPSGs:  you must define the PSG waveform filenames"
            sys.exit(0)
        spsg_args={}
        spsg_args["TYPE"]="PSGexcit"
        spsg_args["PSG_FILE"]=epsc
        spsgs["PSGexcit"]=self.SYN_PSG(spsg_args)
        spsg_args["TYPE"]="PSGinhib"
        spsg_args["PSG_FILE"]=ipsc
        spsgs["PSGinhib"]=self.SYN_PSG(spsg_args)

        return spsgs

    def StandardSFDs(self):
        sfds={}

        for (t, s, f, d) in [("F0", "NONE", "0.000 0.000", "0.000 0.000"),
                             ("F1", "BOTH", "0.376 0.253", "0.045 0.021"),
                             ("F2", "BOTH", "0.021 0.009", "0.706 0.405"),
                             ("F3", "BOTH", "0.062 0.031", "0.144 0.080")]:
            sfd_args={}
            sfd_args["TYPE"]=t
            sfd_args["SFD"]=s
            sfd_args["FACIL_TAU"]=f
            sfd_args["DEPR_TAU"]=d
            sfds[t]=self.SYN_FACIL_DEPRESS(sfd_args)

        return sfds

    def StandardSLs(self):
        sls={}

        sl_args={}
        sl_args["TYPE"]= "0Hebb"
        sl_args["LEARNING"]= "NONE"
        sl_args["LEARNING_SHAPE"]= "TRIANGLE"
        sl_args["NEG_HEB_WINDOW"]= (0.04, 0.0)
        sl_args["NEG_HEB_PEAK_DELTA_USE"]= (0.010000, 0.000000)
        sl_args["NEG_HEB_PEAK_TIME"]= (0.010000, 0.0000)
        sl_args["POS_HEB_WINDOW"]= (0.040000, 0.000000)
        sl_args["POS_HEB_PEAK_DELTA_USE"]= (0.005000, 0.000000)
        sl_args["POS_HEB_PEAK_TIME"]= (0.010000, 0.000000)
        sls["0Hebb"]=self.SYN_LEARNING(sl_args)

        sl_args["TYPE"]= "+Hebb"
        sl_args["LEARNING"]= "+HEBBIAN"
        sls["+Hebb"]=self.SYN_LEARNING(sl_args)

        sl_args["TYPE"]= "-Hebb"
        sl_args["LEARNING"]= "-HEBBIAN"
        sls["-Hebb"]=self.SYN_LEARNING(sl_args)

        sl_args["TYPE"]= "BHebb"
        sl_args["LEARNING"]= "BOTH"
        sls["BHebb"]=self.SYN_LEARNING(sl_args)
        return sls

    def StandardSAs(self):
        sas={}

        for (t, at, ma) in [("SA.E1", "4.2  0.2", "1.5  0.1"),
                            ("SA.E2", "3.01 0.2", "1.1  0.1")]:
            sa_args={}
            sa_args["TYPE"]=t
            sa_args["AUGMENTATION_DELAY"]="0.2  0"
            sa_args["AUGMENTATION_INIT"]="1  0"
            sa_args["AUGMENTATION_TAU"]=at
            sa_args["MAX_AUGMENTATION"]=ma
            sa_args["CA_INTERNAL"]="0  0"
            sa_args["CA_SPIKE_INCREMENT"]="10  0.03"
            sa_args["CA_TAU"]="0.07  0.001"
            sa_args["ALPHA"]="0.0007  0.0001"
            sas[t]=self.SYN_AUGMENTATION(sa_args)

        return sas

    def StandardSynapses(self, spsgs, sls, sfds, sas, maxcond=.0024, syncols=[""], synlays=[""]):
        """
        Creates multiple instances of base synapse type with different USE levels for different strengths of connection.

        References to same synapse type of a particular USE will create *instances*
        of that type of synapse in the runtime, of course, which can
        then vary based on dynamics

        syncols and synlays are used to create multiple types of synapses
        with different prefixes (per column or layers).  Pass them in as
        [""] if that is not desired.

        NOTE:  maxcond does not apply to syncols and synlays versions, only
        base set.  Actually, it applies to all now.

        FIXME:  it makes more sense to have different inital MAXCOND values rather
        than ABSOLUTE_USE values if you are trying to vary the initial strength of synapses . . . 
        """
        syns={}

        # create a set of 11 simple excit and inhib synapses with varying USE vals, plus the base type
        syn_args={}
        syn_args["LEARN_LABEL"]=sls["+Hebb"]
        # ABSOLUTE_USE is the range in which short-term facilitation operates; only Hebbian learning
        # adjusts the ABSOLUTE_USE range.
        syn_args["ABSOLUTE_USE"]="0.25 0.13"
        syn_args["PREV_SPIKE_RANGE"]="0.0 0.04"
        syn_args["SFD_LABEL"]=sfds["F2"]
        syn_args["HEBB_START"]="0"
        syn_args["HEBB_END"]="20"
        # if we started RSE_INIT at 0, that would be as if the cell were "buzzed" and totally
        # depressed at the outset.  by starting at 1.0 it will get its full ABSOLUTE_USE
        # value right at the start.  by starting it at .9 we simulate some past activity
        # but not enough to depress it very much
        syn_args["RSE_INIT"]="1.0 0.2"
        syn_args["MAX_CONDUCT"]="%.4f"%maxcond
        syn_args["DELAY"]="0.003 0.0033"
        sn="E"
        syn_args["TYPE"]=sn
        syn_args["ABSOLUTE_USE"]="0.50 0.10"
        syn_args["SYN_REVERSAL"]="0.0 2.0"
        syn_args["SYN_PSG"]=spsgs["PSGexcit"]
        syns[sn]=self.SYNAPSE(syn_args)
        sn="I"
        syn_args["TYPE"]=sn
        syn_args["ABSOLUTE_USE"]="0.50 0.10"
        syn_args["SYN_REVERSAL"]="-90.0 2.0"
        syn_args["SYN_PSG"]=spsgs["PSGinhib"]
        syns[sn]=self.SYNAPSE(syn_args)
        for u in range(0, 10+1):
            USE="%.2f" % (float(u)/10.0)
            syn_args["ABSOLUTE_USE"]=USE+" 0.10"
            sn="E__"+`u`
            syn_args["TYPE"]=sn
            syn_args["SYN_REVERSAL"]="0.0 2.0"
            syn_args["SYN_PSG"]=spsgs["PSGexcit"]
            syns[sn]=self.SYNAPSE(syn_args)
            sn="I__"+`u`
            syn_args["TYPE"]=sn
            syn_args["SYN_REVERSAL"]="-90.0 2.0"
            syn_args["SYN_PSG"]=spsgs["PSGinhib"]
            syns[sn]=self.SYNAPSE(syn_args)

        # now create the custom layer-specific synapses
        for c in syncols:
            for l in synlays:

                sm=""       # synapse name modifier containing col and lay names, if requested
                if(c):
                    sm=   c+"-"
                    if(l):
                        sm=sm+l+"-"

                syn_args={}

                sn=sm+"L-L";
                syn_args["TYPE"]=sn
                syn_args["SYN_PSG"]=spsgs["PSGexcit"]
                syn_args["SYN_REVERSAL"]="0.0 2.0"
                syn_args["LEARN_LABEL"]=sls["+Hebb"]
                # see above for comment on ABSOLUTE_USE
                syn_args["ABSOLUTE_USE"]="0.25 0.13"
                syn_args["PREV_SPIKE_RANGE"]="0.0 0.04"
                syn_args["SFD_LABEL"]=sfds["F2"]
                # see above for comment on RSE_INIT
                syn_args["RSE_INIT"]="1.0 0.2"
                syn_args["MAX_CONDUCT"]="%.4f"%maxcond
                syn_args["DELAY"]="0.003 0.0033"
                syns[sn]=self.SYNAPSE(syn_args)

                sn=sm+"L4-Lx"
                syn_args["TYPE"]=sn
                syn_args["MAX_CONDUCT"]="%.4f"%maxcond
                syns[sn]=self.SYNAPSE(syn_args)

                sn=sm+"L4-I"
                syn_args["TYPE"]=sn
                syn_args["LEARN_LABEL"]=sls["0Hebb"]
                syn_args["MAX_CONDUCT"]="%.4f"%maxcond
                syns[sn]=self.SYNAPSE(syn_args)

                sn=sm+"E-E"
                syn_args["TYPE"]=sn
                syn_args["MAX_CONDUCT"]="%.4f"%maxcond
                syns[sn]=self.SYNAPSE(syn_args)

                syn_args["SYN_PSG"]=spsgs["PSGinhib"]
                syn_args["SYN_REVERSAL"]="-90.0 2.0"
                syn_args["MAX_CONDUCT"]="%.4f"%maxcond
                syn_args["DELAY"]="0.0015 0.0018"
                for f in ["F1", "F2", "F3"]:
                    sn=sm+"I-E."+f
                    syn_args["TYPE"]=sn
                    syn_args["SFD_LABEL"]=sfds[f]
                    syns[sn]=self.SYNAPSE(syn_args)

                syn_args["LEARN_LABEL"]=sls["0Hebb"]
                syn_args["MAX_CONDUCT"]="%.4f"%maxcond
                for f in ["F1", "F2", "F3"]:
                    sn=sm+"I-I."+f
                    syn_args["TYPE"]=sn
                    syn_args["SFD_LABEL"]=sfds[f]
                    syns[sn]=self.SYNAPSE(syn_args)

                sn=sm+"E-I"
                syn_args["TYPE"]=sn
                syn_args["SYN_PSG"]=spsgs["PSGexcit"]
                syn_args["SYN_REVERSAL"]="0.0 2.0"
                syn_args["LEARN_LABEL"]=sls["0Hebb"]
                syn_args["SFD_LABEL"]=sfds["F2"]
                syn_args["MAX_CONDUCT"]="%.4f"%maxcond
                syns[sn]=self.SYNAPSE(syn_args)

                sn=sm+"C.strong"
                syn_args["TYPE"]=sn
                syn_args["MAX_CONDUCT"]="%.4f"%maxcond
                syn_args["DELAY"]="0.003 0.0033"
                syns[sn]=self.SYNAPSE(syn_args)

                sn=sm+"C.mod"
                syn_args["TYPE"]=sn
                syn_args["MAX_CONDUCT"]="%.4f"%maxcond
                syns[sn]=self.SYNAPSE(syn_args)

        return syns

    def StandardLayers(self, syns, cells, syncols=[""]):
        lays={}
        lay_args={}

        # a super simple single-cell layer, no connections:
        ln="1CELL"
        lay_args["TYPE"]=ln
        lay_args["_INPUT_CELLGROUP"]="ER"
        lay_args["_OUTPUT_CELLGROUP"]="ER"
        lays[ln]=self.LAYER(lay_args)

        # see comment in StandardStuff for why we set this here:
        lays[ln].brain=self

        lays[ln].AddCellType(cells["ER"], "1")

        # more layer types, with multiple cell groups, for multilayer columns:

        # if we want each column to have its own set up synapses in it internally,
        # then each column has to reference a uniquely named set of layers (and
        # each layer will have its connects made up of synapses with unique names)
        for c in syncols:
            sm=""
            if(c): sm=c+"-"
            ln=sm+"L2"
            if(c): sym=ln+"-"
            else: sym=""
            lay_args={}
            lay_args["TYPE"]=ln
            lays[ln]=self.LAYER(lay_args)
            # see comment in StandardStuff for why we set this here:
            lays[ln].brain=self
            # FIXME:  define input and output layers for this column
            lays[ln].AddCellType(cells["ER"], "10")
            lays[ln].AddCellType(cells["ES"], "10")
            lays[ln].AddCellType(cells["I1"], "6")
            lays[ln].AddConnect(cells["ER"], cells["ER"], syns[sym+"E-E"], "0.8", "1.0")
            lays[ln].AddConnect(cells["ES"], cells["ES"], syns[sym+"E-E"], "0.8", "1.0")
            lays[ln].AddConnect(cells["I1"], cells["ER"], syns[sym+"I-E.F1"], "0.1072", "1.0")
            lays[ln].AddConnect(cells["I1"], cells["ES"], syns[sym+"I-E.F1"], "0.1072", "1.0")
            lays[ln].AddConnect(cells["I1"], cells["ER"], syns[sym+"I-E.F2"], "0.572", "1.0")
            lays[ln].AddConnect(cells["I1"], cells["ES"], syns[sym+"I-E.F2"], "0.572", "1.0")
            lays[ln].AddConnect(cells["I1"], cells["ER"], syns[sym+"I-E.F3"], "0.1208", "1.0")
            lays[ln].AddConnect(cells["I1"], cells["ES"], syns[sym+"I-E.F3"], "0.1208", "1.0")
            lays[ln].AddConnect(cells["ER"], cells["I1"], syns[sym+"E-I"], "0.8", "1.0")
            lays[ln].AddConnect(cells["ES"], cells["I1"], syns[sym+"E-I"], "0.8", "1.0")
            lays[ln].AddConnect(cells["ER"], cells["ES"], syns[sym+"E-E"], "0.8", "1.0")
            lays[ln].AddConnect(cells["ES"], cells["ER"], syns[sym+"E-E"], "0.8", "1.0")
            lays[ln].AddConnect(cells["I1"], cells["I1"], syns[sym+"I-E.F1"], "0.1072", "1.0")
            lays[ln].AddConnect(cells["I1"], cells["I1"], syns[sym+"I-E.F2"], "0.1072", "1.0")
            lays[ln].AddConnect(cells["I1"], cells["I1"], syns[sym+"I-E.F3"], "0.572", "1.0")

            # handy abbreviations:
            ER=cells["ER"]
            I1=cells["I1"]

            # NOTE:  all the rest of the layers have the same structure.  That may not be what you want
            for l in ["L3", "L4", "L5", "L6"]:
                ln=sm+l
                if(c): sym=ln+"-"
                else: sym=""

                lay_args={}
                lay_args["TYPE"]=ln
                lays[ln]=self.LAYER(lay_args)
                # see comment in StandardStuff for why we set this here:
                lays[ln].brain=self
                lays[ln].AddCellType(ER, "20")
                lays[ln].AddCellType(I1, "6")
                lays[ln].AddConnect(ER,  ER,  syns[sym+"E-E"], "0.8", "1.0")
                lays[ln].AddConnect(I1,  ER,  syns[sym+"I-E.F1"], "0.1072", "1.0")
                lays[ln].AddConnect(I1,  ER,  syns[sym+"I-E.F2"], "0.572", "1.0")
                lays[ln].AddConnect(I1,  ER,  syns[sym+"I-E.F3"], "0.1208", "1.0")
                lays[ln].AddConnect(ER,  I1,  syns[sym+"E-I"], "0.8", "1.0")
                lays[ln].AddConnect(I1,  I1,  syns[sym+"I-E.F1"], "0.1072", "1.0")
                lays[ln].AddConnect(I1,  I1,  syns[sym+"I-E.F2"], "0.1072", "1.0")
                lays[ln].AddConnect(I1,  I1,  syns[sym+"I-E.F3"], "0.572", "1.0")

        return lays

    def Standard1CellColumn(self, colname=None, loc=(0,0,0,0)):
        """
        """
        (w,h,xloc,yloc)=loc
        #sm=synapseprefix
        lays=self.lays
        cells=self.celltypes
        if colname is None:
            colname="autocol%d"%self.autocolnum
            self.autocolnum+=1
        cn=colname
        #if synpref is None:
        #    synpref=colname+"-syn"

        col_args={}
        col_args["TYPE"]=cn
        col_args["_WIDTH"]="%.4f"%w
        col_args["_HEIGHT"]="%.4f"%h
        col_args["_XLOC"]="%.4f"%xloc
        col_args["_YLOC"]="%.4f"%yloc
        col_args["_OUTPUT_LAYER"]=colname+"_"+"1CELL"
        col_args["_INPUT_LAYER"]=colname+"_"+"1CELL"
        col=self.COLUMN(col_args)
        self.AddColumn(col)

        # a simple 1 excitable cell single layer, no interconnections:
        lay_args={}
        ln=colname+"_"+"1CELL"
        lay_args["TYPE"]=ln
        lay_args["_INPUT_CELLGROUP"]="ER"
        lay_args["_OUTPUT_CELLGROUP"]="ER"
        lays[ln]=self.LAYER(lay_args)
        lays[ln].AddCellType(cells["ER"], "1")
        L1=lays[ln]
        col.AddLayerType(L1)

        return col

    def SingleCellColumn(self, colname, synapseprefix, w, h, xloc, yloc, lays, cells, syns):
        cn=colname
        sm=synapseprefix

        col_args={}
        col_args["TYPE"]=cn
        col_args["_WIDTH"]="%.4f"%w
        col_args["_HEIGHT"]="%.4f"%h
        col_args["_XLOC"]="%.4f"%xloc
        col_args["_YLOC"]="%.4f"%yloc
        col_args["_OUTPUT_LAYER"]="1CELL"
        col_args["_INPUT_LAYER"]="1CELL"
        col=self.COLUMN(col_args)
        col.AddLayerType(lays["1CELL"])
        return col

    def Standard1LayerColumn(self, colname, synapseprefix, w, h, xloc, yloc, lays, cells, syns, comptypes):
        cn=colname
        sm=synapseprefix

        # a simple 16 excitable cell single layer, no interconnections:
        lay_args={}
        ln=colname+"_"+"1LAY"
        lay_args["TYPE"]=ln
        lay_args["_INPUT_CELLGROUP"]="ER"
        lay_args["_OUTPUT_CELLGROUP"]="ER"
        lays[ln]=self.LAYER(lay_args)
        lays[ln].AddCellType(cells["ER"], "16")
        #lays[ln].AddCellType(cells["ER"], "1")
        L1=lays[ln]

        col_args={}
        col_args["TYPE"]=cn
        col_args["_WIDTH"]="%.4f"%w
        col_args["_HEIGHT"]="%.4f"%h
        col_args["_XLOC"]="%.4f"%xloc
        col_args["_YLOC"]="%.4f"%yloc
        col_args["_OUTPUT_LAYER"]=colname+"_"+"1LAY"
        col_args["_INPUT_LAYER"]=colname+"_"+"1LAY"
        col=self.COLUMN(col_args)
        col.AddLayerType(L1)
        return col

    def StandardEnumeratedColumn(self, colname, synapseprefix, w, h, xloc, yloc, lays, cells, syns, comptypes):
        """
            make an Enumerated column with three layers of standard sizes of exc and inh cells
        """
        makelays=[(9, 5, "std", "output"), (15, 7, "mut", "input"), (8, 4, "std", None)]
        #makelays=[(3, 1, "std", "output"), (3, 1, "mut", "input"), (3, 1, "std", None)]
        laycons=[(1, "exc", 3), (2, "exc", 1)]
        return self.EnumeratedColumn(colname, synapseprefix, w, h, xloc, yloc, lays, cells, syns, comptypes, makelays, laycons)

    def EnumeratedColumn(self, colname, synapseprefix, w, h, xloc, yloc, lays, cells, syns, comptypes, makelays, laycons):
        """
        (EXPERIMENTAL) Create an enumerated column.

        makelays is a list of (e, i) excitatory, inhibitory cell pairs
        these will be added to lays layer list
        new:  also inter and intralayer connection patterns, input and output layers
        by default no connections are made between cell groups in a layer
        nor between cell groups in different layers
        """
        cn=colname
        sm=synapseprefix

        col_args={}
        col_args["TYPE"]=cn
        col_args["_WIDTH"]="%.4f"%w
        col_args["_HEIGHT"]="%.4f"%h
        col_args["_XLOC"]="%.4f"%xloc
        col_args["_YLOC"]="%.4f"%yloc
        col_args["_ENUM"]=True
        # bad:  makes assumption about layer organization
        lnum=1
        for (e, i, p, t) in makelays:
            ln=colname+"_"+`lnum`
            # must be exactly one input and output layer!
            if t=="input":
                col_args["_INPUT_LAYER"]=ln
            elif t=="output":
                col_args["_OUTPUT_LAYER"]=ln
            lnum=lnum+1 

        exctype="E"
        inhtype="I"

        # now that input and output layers are defined we can create column
        col=self.COLUMN(col_args)

        lnum=1
        for (e, i, p, t) in makelays:
            lay_args={}
            ln=colname+"_"+`lnum`
            lay_args["TYPE"]=ln
            # FIXME:  should somehow derive this:
            lay_args["_INPUT_CELLGROUP"]=exctype
            lay_args["_OUTPUT_CELLGROUP"]=exctype
            h={}
            h[exctype]=e
            h[inhtype]=i
            lay_args["_CELLGROUP_SIZE"]=h
            lays[ln]=self.LAYER(lay_args)
            # we must give each cell its own named cellgroup (-1, -2, etc.)
            # normally, a cellgroup will refer to some number of cells of a given common type,
            # and the name of the cell group in the layer is just the name of that underlying cell;
            # however, since we have to be able to uniquely reference each cellgroup, each cellgroup
            # in the enumerated col must have a unique name (laynum-cellname-cellnum)
            # and, we have to create a cell with such a name too!
            # note however that different layers can share these underlying cell *types* (e.g. 3-ER-9)
            # actually, don't need layer number prepended to cell name since lay name is part of address
            # any time the cell is referenced
            for ee in range(0, e):      # we are enumerating cells!
                cellname=exctype+"-"+`ee`
                c=StandardCell(cellname, cells, comptypes)
                lays[ln].AddCellType(c, 1)
            for ii in range(0, i):
                cellname=inhtype+"-"+`ii`
                c=StandardCell(cellname, cells, comptypes)
                lays[ln].AddCellType(c, 1)
            # FIXME:  the prob of connection is hard coded; since this is a "standard" column
            # that may not be so bad, but some flexibility would be better
            prob=0.1
            speed=1.0
            # FIXME:  make the below enumerations more elegant
            # enumerate the intra layer connections in this layer according to requested connection pattern:
            # make enumerated E->I exc connections
            if p=="std" or p=="mut":
                for ee in range(0, e):
                    for ii in range(0, i):
                        if random.random() < prob:
                            scellgpname=exctype+"-"+`ee`
                            scellgp=cells[scellgpname]
                            tcellgpname=inhtype+"-"+`ii`
                            tcellgp=cells[tcellgpname]
                            lays[ln].AddConnect(scellgp, "SOMA1_name", tcellgp, "SOMA1_name", syns["E"], 1.0, speed)
            # make enumerated E->E exc connections
            if p=="std":        # not done for "mut" connection pattern
                for ee in range(0, e):
                    for eee in range(0, e):
                        if random.random() < prob:
                            scellgpname=exctype+"-"+`ee`
                            scellgp=cells[scellgpname]
                            tcellgpname=exctype+"-"+`eee`
                            tcellgp=cells[tcellgpname]
                            lays[ln].AddConnect(scellgp, "SOMA1_name", tcellgp, "SOMA1_name", syns["E"], 1.0, speed)
            # make enumerated I->E inh connections
            if p=="std" or p=="mut":
                for ii in range(0, i):
                    for ee in range(0, e):
                        if random.random() < prob:
                            scellgpname=inhtype+"-"+`ii`
                            scellgp=cells[scellgpname]
                            tcellgpname=exctype+"-"+`ee`
                            tcellgp=cells[tcellgpname]
                            lays[ln].AddConnect(scellgp, "SOMA1_name", tcellgp, "SOMA1_name", syns["I"], 1.0, speed)
            col.AddLayerType(lays[ln])
            lnum=lnum+1 

        # enumerate the requested inter layer connections in this column:
        prob=0.1
        speed=1.0
        for (s, c, t) in laycons:
            slname=colname+"_"+`int(s)`
            sl=lays[slname]
            tlname=colname+"_"+`int(t)`
            tl=lays[tlname]
            # we will always connect to the INPUT_CELLGROUP of the requested layer, but
            # the connections will come from the inhib cells of the source group if the
            # conns are inhibitory or exc cells of the source group if the conns are exc
            tcgpprefix=tl.parms["_INPUT_CELLGROUP"]
            if c=="exc":
                scgpprefix=exctype
                s=syns["E"]
            else:
                scgpprefix=inhtype
                s=syns["I"]
            eh=sl.parms["_CELLGROUP_SIZE"]
            ssize=eh[scgpprefix]
            eh=tl.parms["_CELLGROUP_SIZE"]
            tsize=eh[tcgpprefix]
            for ss in range(0, ssize):
                for tt in range(0, tsize):
                    if random.random() < prob:
                        scellgpname=scgpprefix+"-"+`ss`
                        scellgp=cells[scellgpname]
                        tcellgpname=tcgpprefix+"-"+`tt`
                        tcellgp=cells[tcellgpname]
                        col.AddConnect(sl, scellgp, "SOMA1_name", tl, tcellgp, "SOMA1_name", s, 1.0, speed)

        return col

    def Standard3LayerColumn(self, colname, synapseprefix, w, h, xloc, yloc, lays, cells, syns, comptypes):
        """
        NOTE that for this column we add the layers to lays here rather than in
        the StandardLayer routine above.  This seems like a good idea.
        A custom set of layers is created and added to lays for each column created.
        This is so that the layer connections can have CONNECTS with different synaptic
        USE strengths.  (FIXME:  make this an option that can be turned on or off.)
        NOTE that the referenced synapses do not have custom names; that's OK, it just
        means that the synapses must have the same properties for all such layers, but
        we can still use CONNECTS with different strengths of that class of synapse.
        """
        cn=colname
        sm=synapseprefix

        E=cells["ER"]
        I=cells["I1"]

        lay_args={}
        ln=colname+"_"+"3LAY-1"
        lay_args["TYPE"]=ln
        lay_args["_INPUT_CELLGROUP"]="ER"
        lay_args["_OUTPUT_CELLGROUP"]="ER"
        lays[ln]=self.LAYER(lay_args)
        lays[ln].AddCellType(cells["ER"], "9")      # FIXME:  confirm these cell types ER/I1
        lays[ln].AddCellType(cells["I1"], "5")
        lays[ln].AddConnect(E, "SOMA1_name", I, "SOMA1_name", syns["E"], "0.1", "1.0")
        lays[ln].AddConnect(E, "SOMA1_name", E, "SOMA1_name", syns["E"], "0.1", "1.0")
        lays[ln].AddConnect(I, "SOMA1_name", E, "SOMA1_name", syns["I"], "0.1", "1.0")
        L1=lays[ln]
        
        lay_args={}
        ln=colname+"_"+"3LAY-2"
        lay_args["TYPE"]=ln
        lay_args["_INPUT_CELLGROUP"]="ER"
        lay_args["_OUTPUT_CELLGROUP"]="ER"
        lays[ln]=self.LAYER(lay_args)
        lays[ln].AddCellType(cells["ER"], "15")      # FIXME:  confirm these cell types ER/I1
        lays[ln].AddCellType(cells["I1"], "7")
        lays[ln].AddConnect(E, "SOMA1_name", I, "SOMA1_name", syns["E"], "0.1", "1.0")
        lays[ln].AddConnect(I, "SOMA1_name", E, "SOMA1_name", syns["I"], "0.1", "1.0")
        L2=lays[ln]

        lay_args={}
        ln=colname+"_"+"3LAY-3"
        lay_args["TYPE"]=ln
        lay_args["_INPUT_CELLGROUP"]="ER"
        lay_args["_OUTPUT_CELLGROUP"]="ER"
        lays[ln]=self.LAYER(lay_args)
        lays[ln].AddCellType(cells["ER"], "8")      # FIXME:  confirm these cell types ER/I1
        lays[ln].AddCellType(cells["I1"], "4")
        lays[ln].AddConnect(E, "SOMA1_name", I, "SOMA1_name", syns["E"], "0.1", "1.0")
        lays[ln].AddConnect(E, "SOMA1_name", E, "SOMA1_name", syns["E"], "0.1", "1.0")
        lays[ln].AddConnect(I, "SOMA1_name", E, "SOMA1_name", syns["I"], "0.1", "1.0")
        L3=lays[ln]

        col_args={}
        col_args["TYPE"]=cn
        col_args["_WIDTH"]="%.4f"%w
        col_args["_HEIGHT"]="%.4f"%h
        col_args["_XLOC"]="%.4f"%xloc
        col_args["_YLOC"]="%.4f"%yloc
        col_args["_INPUT_LAYER"]=colname+"_"+"3LAY-2"
        col_args["_OUTPUT_LAYER"]=colname+"_"+"3LAY-1"
        col=self.COLUMN(col_args)
        col.AddLayerType(L1)
        col.AddLayerType(L2)
        col.AddLayerType(L3)
        col.AddConnect(L1, E, "SOMA1_name", L3, E, "SOMA1_name", syns["E"], "0.1", "1.0")
        col.AddConnect(L2, E, "SOMA1_name", L1, E, "SOMA1_name", syns["E"], "0.1", "1.0")
        return col

    def Standard6LayerColumn(self, colname, synapseprefix, w, h, xloc, yloc, lays, cells, syns, comptypes):
        cn=colname
        sm=synapseprefix
        L2=lays[sm+"L2"]
        L3=lays[sm+"L3"]
        L4=lays[sm+"L4"]
        L5=lays[sm+"L5"]
        L6=lays[sm+"L6"]

        # handy abbreviations:
        ER=cells["ER"]
        ES=cells["ES"]
        I1=cells["I1"]

        col_args={}
        col_args["TYPE"]=cn
        col_args["_WIDTH"]="%.4f"%w
        col_args["_HEIGHT"]="%.4f"%h
        col_args["_XLOC"]="%.4f"%xloc
        col_args["_YLOC"]="%.4f"%yloc
        col=self.COLUMN(col_args)
        col.AddLayerType(L2)
        col.AddLayerType(L3)
        col.AddLayerType(L4)
        col.AddLayerType(L5)
        col.AddLayerType(L6)
        col.AddConnect(L2, ES, "SOMA1_name", L3, ER, "SOMA1_name", syns[sm+"L-L"], "0.8", "1.0")
        col.AddConnect(L3, ER, "SOMA1_name", L2, ER, "SOMA1_name", syns[sm+"L-L"], "0.8", "1.0")
        col.AddConnect(L3, ER, "SOMA1_name", L5, ER, "SOMA1_name", syns[sm+"L-L"], "0.8", "1.0")
        col.AddConnect(L3, ER, "SOMA1_name", L6, ER, "SOMA1_name", syns[sm+"L-L"], "0.8", "1.0")
        col.AddConnect(L4, ER, "SOMA1_name", L2, ER, "SOMA1_name", syns[sm+"L4-Lx"], "0.8", "1.0")
        col.AddConnect(L4, ER, "SOMA1_name", L2, I1, "SOMA1_name", syns[sm+"L4-I"], "0.8", "1.0")
        col.AddConnect(L4, ER, "SOMA1_name", L3, ER, "SOMA1_name", syns[sm+"L4-Lx"], "0.8", "1.0")
        col.AddConnect(L4, ER, "SOMA1_name", L3, I1, "SOMA1_name", syns[sm+"L4-I"], "0.8", "1.0")
        col.AddConnect(L4, ER, "SOMA1_name", L5, ER, "SOMA1_name", syns[sm+"L4-Lx"], "0.8", "1.0")
        col.AddConnect(L4, ER, "SOMA1_name", L5, I1, "SOMA1_name", syns[sm+"L4-I"], "0.8", "1.0")
        col.AddConnect(L4, ER, "SOMA1_name", L6, ER, "SOMA1_name", syns[sm+"L4-Lx"], "0.8", "1.0")
        col.AddConnect(L4, ER, "SOMA1_name", L6, I1, "SOMA1_name", syns[sm+"L4-I"], "0.8", "1.0")
        col.AddConnect(L5, ER, "SOMA1_name", L2, ER, "SOMA1_name", syns[sm+"L-L"], "0.8", "1.0")
        col.AddConnect(L6, ER, "SOMA1_name", L2, ER, "SOMA1_name", syns[sm+"L-L"], "0.8", "1.0")
        return col

    class EnumeratedArea:
        """
        Not implemented in this release.
        """
        pass

    def EmitColumnShell(self, cn, w, h, x, y):
        """
        NCS requires a COLUMN_SHELL for each col.  This emits it for column named cn.

        Basically it just holds spatial location for the column.  However, since there
        is no type-of abstraction for a column, this information might as well be in
        the column itself.  Or change NCS to have a type-of abstraction for the column. 
        """
        s=[]
        s.append("COLUMN_SHELL\n")
        s.append("    TYPE     "); s.append(cn); s.append("_sh\n")
        s.append("    WIDTH    %.4f\n" % float(w))
        s.append("    HEIGHT   %.4f\n" % float(h))
        s.append("    LOCATION %.4f %.4f\n" % (float(x), float(y)))
        s.append("END_COLUMN_SHELL\n")
        return "".join(s)

    def EmitLayerShell(self, cn, u, l):
        # temp hack, shells not really used for now
        s=[]
        s.append("LAYER_SHELL\n")
        s.append("    TYPE     ")
        s.append(cn)
        s.append("_sh\n")
        s.append("    UPPER    %d\n" % int(u))
        s.append("    LOWER    %d\n" % int(l))
        s.append("END_LAYER_SHELL\n")
        return "".join(s)

####################################################################

def AreaTest():
    """ Test new area abstractions.
    """
    newb=BRAIN({"TYPE": "AREA-BRAIN", "FSV": "10000.00", "JOB": "areabrain",
                "SEED": "999999", "DURATION": "2.00", "OUTPUT_CELLS": "YES",
                "OUTPUT_CONNECT_MAP": "YES"})
    # no stims
    # no stiminjects
    # no reports
    chans=StandardChannels()
    spks=StandardSpikes()               # action potential template
    comptypes=StandardCompartments(spks, chans)
    cells=StandardCells(comptypes)
    spsgs=StandardPSGs(None, None)
    sfds=StandardSFDs()                 # syn facil and depression profiles
    sls=StandardSLs()                   # syn learning profiles
    sas=StandardSAs()                   # syn augmentation profiles
    syns=StandardSynapses(spsgs, sls, sfds, sas)
    lays=StandardLayers(syns, cells)
    #for cn in ["AS", "VS", "AC", "BP", "FP", "BM", "FM"]:
    #    sm=""
    #    col=Standard6LayerColumn(cn, sm, lays, cells, syns)
    #    newb.AddColumn(col)

    areas={}

    w=200.0
    h=100.0
    x=0.0
    y=0.0
    for areaname in ["M", "V"]:
        #print "on area", areaname
        areas[areaname]=newb.AddArea(areaname, 5, 5, 1, 1, w, h, x, y, SingleCellColumn, lays, cells, syns, comptypes)
        y=y+w+50.0      # 50.0 to give a little separation between areas

    #use1=
    newb.ConnectAreas("M", "V", "all", syns["E"], "1.0", "10.0", lays, cells)
    #use2=
    newb.ConnectAreas("M", "V", "corresponding", syns["E"], "1.0", "10.0", lays, cells)

    #print "1st connect resulted in", len(use1), "use vals" # 625
    #print "2nd connect resulted in", len(use2), "use vals" # 25
    #cons=newb.parms["CONNECT"]

    #print "there are", len(cons), "inter-column connections"
    #for i in range(0, len(cons)):
    #    (frmcol, frmlay, frmcell, frmcmp, tocol, tolay, tocell, tocmp, synapse, prob, speed)=cons[i]
    #    print i,"connected with", synapse

    #print newb
    newb.syns=syns
    return newb

def Test1():
    """ This is designed to generate identical .in file as the original full_ivo.py model.
        Test2() may contain some simplifications that result in a functionally identical .in
        file that looks a little different; e.g., all synapses are defined per-layer for
        consistency even when they don't have to be.
    """

    per_layer_synapses=True

    newb=BRAIN({"TYPE": "IVO-BRAIN", "FSV": "10000.000000", "JOB": "full_ivo12032003-1",
                "PORT": "1541", "SERVER": "134.197.40.155", "SEED": "999999", 
                "DURATION": "2.000000"})

    #####
    stims={}

    stim_args={}
    stim_args["TYPE"]="stimulus1"
    stim_args["MODE"]="CURRENT"
    stim_args["PATTERN"]="INPUT"
    stim_args["PORT"]="1501"
    stim_args["FILENAME"]="134.197.40.155"
    stim_args["FREQ_COLS"]="1"
    stim_args["CELLS_PER_FREQ"]="20"
    stim_args["TIME_INCREMENT"]="0.002500 1.000000"
    stim_args["TIMING"]="EXACT"
    stim_args["SAMESEED"]="NO"
    stim_args["AMP_START"]="10.0"
    stim_args["AMP_END"]="10.0"
    stim_args["WIDTH"]="0.01"
    stim_args["FREQ_START"]="9999.000000"
    stim_args["TIME_START"]="0.0"
    stim_args["TIME_END"]="5.0"
    stims["stimulus1"]=STIMULUS(stim_args)

    stim_args["TYPE"]="stimulus2"
    stim_args["PORT"]="1521"
    stim_args["TIME_INCREMENT"]="0.040000 1.000000"
    stims["stimulus2"]=STIMULUS(stim_args)
    # (stimulus items are reference by stiminjects and don't need to be
    # added to brain explicitly)

    #####
    stimis={}

    stimi_args={}
    stimi_args["TYPE"]="stiminject1"
    stimi_args["STIM_TYPE"]=stims["stimulus1"]
    stimi_args["INJECT"]="AS L4 ER SOMA1_name 1.0"
    stimis["stiminject1"]=STIMULUS_INJECT(stimi_args)

    stimi_args["TYPE"]="stiminject2"
    stimi_args["STIM_TYPE"]=stims["stimulus2"]
    stimi_args["INJECT"]="VS L4 ER SOMA1_name 1.0"
    stimis["stiminject2"]=STIMULUS_INJECT(stimi_args)

    # put these in the brain:
    for s in stimis.keys():
        newb.AddStimInject(stimis[s])

    #####
    reps={}

    rep_args={}
    rep_args["TYPE"]="MyReport1"
    rep_args["CELLS"]="FM L5 ER SOMA1_name"
    rep_args["PROB"]="1.0"
    rep_args["REPORT_ON"]="VOLTAGE"
    rep_args["FILENAME"]="134.197.40.155"
    rep_args["PORT"]="1511"
    rep_args["FREQUENCY"]="1"
    rep_args["ASCII"]=""
    rep_args["TIME_START"]="0.0"
    rep_args["TIME_END"]="2.0"
    reps["MyReport1"]=REPORT(rep_args)

    rep_args["TYPE"]="MyReport2"
    rep_args["FILENAME"]="volt_a.txt"
    del rep_args["PORT"]
    reps["MyReport2"]=REPORT(rep_args)

    rep_args["TYPE"]="MyReport3"
    rep_args["CELLS"]="BM L5 ER SOMA1_name"
    rep_args["FILENAME"]="134.197.40.155"
    rep_args["PORT"]="1531"
    reps["MyReport3"]=REPORT(rep_args)

    rep_args["TYPE"]="MyReport4"
    rep_args["FILENAME"]="volt_b.txt"
    del rep_args["PORT"]
    reps["MyReport4"]=REPORT(rep_args)

    rep_args["TYPE"]="VS_L4_ER"
    rep_args["CELLS"]="VS L4 ER SOMA1_name"
    rep_args["FILENAME"]="volt.vs.l4.er.txt"
    reps["VS_L4_ER"]=REPORT(rep_args)

    rep_args["TYPE"]="AS_L4_ER"
    rep_args["CELLS"]="AS L4 ER SOMA1_name"
    rep_args["FILENAME"]="volt.as.l4.er.txt"
    reps["AS_L4_ER"]=REPORT(rep_args)

    # put these in the brain:
    for k in reps.keys():
        newb.AddReport(reps[k])

    #####
    chans=StandardChannels()
    spks=StandardSpikes()               # action potential template
    comptypes=StandardCompartments(spks, chans)
    cells=StandardCells(comptypes)
    spsgs=StandardPSGs(epsc="/home/cwilson/EPSC.txt", ipsc="/home/cwilson/IPSC.txt")
    sfds=StandardSFDs()                 # syn facil and depression profiles
    sls=StandardSLs()                   # syn learning profiles
    sas=StandardSAs()                   # syn augmentation profiles

    if(per_layer_synapses):
        """ Each layer in FM, BM, FP, BP has unique synapse named, e.g.:  FM-L2-E-E
            by putting "" in the col list, we will also create a base set of synapses with no
            col or layer name prepended for use by cols that don't have per-layer syns.
            For per_layer_synapse, we actually want to create a set with COL-LAY-SYN (for
            LAYER CONNECTs), COL_SYN (for COLUMN CONNECT), and plain SYN for BRAIN CONNECTS
            since at each of these levels may have synaptic connections with different type
            properties. 
            See also comment at top of this script.
            VS does not get per-layer synapses (that's just the way Christine's IVO's designed)
        """
        syncols=["FM", "BM", "FP", "BP", ""]
        synlays=["L2", "L3", "L4", "L5", "L6", ""]
    else:
        syncols=[""]
        synlays=[""]

    syns=StandardSynapses(spsgs, sls, sfds, sas)
    lays=StandardLayers(syns, cells)

    ##### columns
    cols={}

    # NOTE:  all these columns have the same structure; confirm with Christine that this is right
    for cn in ["AS", "VS", "AC", "BP", "FP", "BM", "FM"]:
        sm=""
        if(per_layer_synapses):
            if cn=="BP" or cn=="FP" or cn=="BM" or cn=="FM":     # only these cols have custom synapses
                sm=cn+"-"
        cols[cn]=Standard6LayerColumn(cn, sm, 1.0, 2.0, 3.0, 4.0, lays, cells, syns, comptypes)
        newb.AddColumn(cols[cn])

    #### connects between different columns

    # FM, FP, BM, BP have custom layer names

    # figure out a cleaner way to do this
    # should be able to readily reference the col to get the layer name stored there
    if per_layer_synapses:
        FPL2=lays["FP-L2"]
        FPL3=lays["FP-L3"]
        FPL4=lays["FP-L4"]
        FPL5=lays["FP-L5"]
        FPL6=lays["FP-L6"]
        FML2=lays["FM-L2"]
        FML4=lays["FM-L4"]
        FML6=lays["FM-L6"]
        BPL2=lays["BP-L2"]
        BPL3=lays["BP-L3"]
        BPL4=lays["BP-L4"]
        BPL5=lays["BP-L5"]
        BPL6=lays["BP-L6"]
        BML2=lays["BM-L2"]
        BML4=lays["BM-L4"]
        BML5=lays["BM-L5"]
        BML6=lays["BM-L6"]
        VSL3=lays["L3"]     # VS does not have per-layer synapses
    else:
        FPL2=lays["L2"]
        FPL3=lays["L3"]
        FPL4=lays["L4"]
        FPL5=lays["L5"]
        FPL6=lays["L6"]
        FML2=lays["L2"]
        FML4=lays["L4"]
        FML6=lays["L6"]
        BPL2=lays["L2"]
        BPL3=lays["L3"]
        BPL4=lays["L4"]
        BPL5=lays["L5"]
        BPL6=lays["L6"]
        BML2=lays["L2"]
        BML4=lays["L4"]
        BML5=lays["L5"]
        BML6=lays["L6"]
        VSL3=lays["L3"]

    # handy abbreviations:
    AS=cols["AS"]
    VS=cols["VS"]
    AC=cols["AC"]
    BP=cols["BP"]
    FP=cols["FP"]
    BM=cols["BM"]
    FM=cols["FM"]
    ER=cells["ER"]
    ES=cells["ES"]
    I1=cells["I1"]

    newb.AddConnect(VS, lays["L2"], ES, "SOMA1_name", FP, FPL4, ER, "SOMA1_name", syns["C.strong"], "1.0", "10.0")
    newb.AddConnect(VS, lays["L2"], ES, "SOMA1_name", BP, BPL4, ER, "SOMA1_name", syns["C.strong"], "1.0", "10.0")

    newb.AddConnect(AS, lays["L2"], ES, "SOMA1_name", AC, lays["L2"], ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")

    newb.AddConnect(AC, lays["L3"], ER, "SOMA1_name", FP, FPL3, ER, "SOMA1_name", syns["C.strong"], "1.0", "10.0")
    newb.AddConnect(AC, lays["L3"], ER, "SOMA1_name", BP, BPL3, ER, "SOMA1_name", syns["C.strong"], "1.0", "10.0")

    newb.AddConnect(FP, FPL2, ES, "SOMA1_name", FM, FML4, ER, "SOMA1_name", syns["C.strong"], "1.0", "10.0")
    newb.AddConnect(FP, FPL2, ES, "SOMA1_name", BP, BPL4, ER, "SOMA1_name", syns["C.strong"], "1.0", "10.0")
    newb.AddConnect(FP, FPL5, ER, "SOMA1_name", FM, FML4, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(FP, FPL5, ER, "SOMA1_name", BP, BPL2, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(FP, FPL5, ER, "SOMA1_name", BM, BML2, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(FP, FPL6, ER, "SOMA1_name", VS, VSL3, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")

    newb.AddConnect(FM, FML2, ES, "SOMA1_name", FP, FPL2, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(FM, FML2, ES, "SOMA1_name", BM, BML2, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(FM, FML2, ES, "SOMA1_name", BM, BML4, ER, "SOMA1_name", syns["C.strong"], "1.0", "10.0")
    newb.AddConnect(FM, FML2, ER, "SOMA1_name", BM, BML4, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(FM, FML6, ER, "SOMA1_name", FP, FPL3, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")

    newb.AddConnect(BP, BPL2, ES, "SOMA1_name", BM, BML4, ER, "SOMA1_name", syns["C.strong"], "1.0", "10.0")
    newb.AddConnect(BP, BPL2, ES, "SOMA1_name", FP, FPL4, ER, "SOMA1_name", syns["C.strong"], "1.0", "10.0")
    newb.AddConnect(BP, BPL5, ER, "SOMA1_name", BM, BML4, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(BP, BPL5, ER, "SOMA1_name", FP, FPL2, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(BP, BPL5, ER, "SOMA1_name", FM, FML2, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(BP, BPL6, ER, "SOMA1_name", VS, VSL3, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")

    newb.AddConnect(BM, BML2, ES, "SOMA1_name", BP, BPL2, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(BM, BML2, ES, "SOMA1_name", FM, FML2, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(BM, BML2, ES, "SOMA1_name", FM, FML4, ER, "SOMA1_name", syns["C.strong"], "1.0", "10.0")
    newb.AddConnect(BM, BML5, ER, "SOMA1_name", FM, FML4, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")
    newb.AddConnect(BM, BML6, ER, "SOMA1_name", BP, BPL3, ER, "SOMA1_name", syns["C.mod"], "1.0", "10.0")

    ####

    # output the brain
    #print newb

    #allsyns=newb.GetSynapses()
    #print "there are", len(allsyns), "synapses"
    newb.syns=syns
    return newb

def EnumeratedTest():
    """
        Test brain with column having enumerated cells (each cell is its own cellgroup)
        FIXME:  remove explicit StandardStuff
    """
    newb=BRAIN({"TYPE": "AREA-BRAIN", "FSV": "10000.00", "JOB": "areabrain",
                "SEED": "999999", "DURATION": "2.00", "OUTPUT_CELLS": "YES",
                "OUTPUT_CONNECT_MAP": "YES"})
    # no stims
    # no stiminjects
    # no reports
    chans=StandardChannels()
    spks=StandardSpikes()               # action potential template
    comptypes=StandardCompartments(spks, chans)
    cells=StandardCells(comptypes)
    spsgs=StandardPSGs(None, None)
    sfds=StandardSFDs()                 # syn facil and depression profiles
    sls=StandardSLs()                   # syn learning profiles
    sas=StandardSAs()                   # syn augmentation profiles
    syns=StandardSynapses(spsgs, sls, sfds, sas)
    lays=StandardLayers(syns, cells)

    #col=EnumeratedColumn("colname", "synpref", 10, 10, 10, 10, lays, cells, syns, comptypes, [(10,5), (5,6), (16, 5)])
    #newb.AddColumn(col)

    newb.AddArea("A", 2, 2, 2, 2, 10, 10, 10, 10, StandardEnumeratedColumn, lays, cells, syns, comptypes)
    newb.AddArea("B", 2, 2, 2, 2, 10, 10, 10, 10, StandardEnumeratedColumn, lays, cells, syns, comptypes)
    newb.AddArea("C", 2, 2, 2, 2, 10, 10, 10, 10, Standard3LayerColumn, lays, cells, syns, comptypes)

    conpat="all"
    syn="E"
    prob=0.1
    # test enumerated to enumerated connections:
    #newb.ConnectAreas("A", "B", conpat, syns[syn], prob, "10.0", lays, cells)
    # test non enumerated to enumerated:
    syn="E"
    newb.ConnectAreas("C", "B", conpat, syns[syn], prob, "10.0", lays, cells)

    newb.syns=syns
    return newb

if __name__ == "__main__":
    """
    For testing, if invoked directly rather than being included
    in other code.  These tests may be obsolete.  Fix them.
    """
    #newb=Test1()
    #newb=AreaTest()
    newb=EnumeratedTest()
    print newb
    sys.exit(0)

    # this won't work with Test1 because we don't have USE variants for each synapse type
    allsyns=newb.GetSynapses()
    print "there are", len(allsyns), "synapses"
    #print allsyns

    for i in range(0, len(allsyns)):
        allsyns[i]=random.randrange(0, 10+1)
    newb.SetSynapses(allsyns, newb.syns)

    print "after changes 1:"
    #print allsyns
    print newb

    for i in range(0, len(allsyns)):
        allsyns[i]=random.randrange(0, 10+1)
    newb.SetSynapses(allsyns, newb.syns)

    print "after changes 2:"
    print newb
