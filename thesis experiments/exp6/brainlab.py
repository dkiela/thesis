#!/usr/bin/env python
import os, time, sys
from brain import *

"""
brainlab.py

    This module provides support routines for job execution, plotting and figure generation,
    for NCS+brainlab jobs.

    1.03:  20091012 PRD
        Changed " Total run time" search string to recognize job completion (NCS apparently removed leading space)

    1.02:  20081128 RPD
        Small doc and other fixes.

    1.01:  changed from old mpich invocation to new
            added -nolocal option to mpirun invocation so jobs don't run on headnode too
        should at some point include ethernet and myrinet invocation options to this script
"""

__version__="1.03"

from socket import gethostname
from os.path import join

hn=gethostname()

# My 3D pyopengl plotting library. 
try:
    from netplot import *
except:
    print hn+": brainlab:  netplot is not available, don't try 3D plots"

# matplotlib is a matlab-like plot library that supports numpy.
# maybe better to use the interface designed for python rather than the
# matlab compatibility layer (pylab)
try:
    from pylab import *
except:
    print hn+": brainlab:  matplotlib (pylab) not available, plotting functions disabled"

try:
    import numpy
except:
    print hn+": brainlab:  numpy not available"
import cPickle

# pyx is a 2D postscript drawing package that is handy for making column
# diagrams for documentation
try:
    import pyx
except:
    print hn+": brainlab:  pyx not available; 2D documentation drawing support disabled"

fignum=1

# import psyco in the calling program if desired

"""
    FIXME:  now that e.g. LoadSpikeData can operate on a variable for the report
        instead of a text name, it would be good if the report functions didn't
        demand a text report name but left it optional and assigned one automatically
        if it wasn't supplied

    FIXME:  make sure all plotting routines do a fetch if needed.
            make sure all plotting routines don't do a show()
            make sure all plotting routines can take a save as arg (ps or png)
            make sure all plotting routines can plot into a subfig (will allocate using nextfigure())
                or will accept usefig= argument so caller can arrange things as desired 

    maybe change BRAIN.Run() from a method to a simple function Run(brain)

    FIXME:  create subdir in remote-invoke for each job?
        that would be cleaner

    DOCUMENT:  only selectively copying reports back.  if a spikelist is
    requested, or a spikeplot, we don't need all the data so there is
    no point in copying everything back.

    FIXME:  haven't tested .stm file copy over to remote etc. under new naming scheme

    Report ideas:
        would like user to be able to just say "voltage report on these cells for this time"
        rather than having to request an NCS report and then plot something based on that
        report, however, it is also very valuable to be able to store the raw data for the
        report so that the report can be regenerated.

        * Start of a run should only delete the .txt report files that will be regenerated,
            not ALL .txt files!
        * call to report should look for the file locally, and if present, use that
            if not, the report file should be copied over (but from what dir?) or
            the data should be copied from remote to local, or a processed version
            of the data should be retrieved
            answer:  look at brain name.  This should be unique for each run.
        * support multiple reports for a given cell range or just have one report
            that must contain all data of interest, broken out by user?

    We no longer automatically prepend $HOME to the remdir from the brainlabrc.
    It can be included in the remdir in the brainlabrc if desired.
    If you want to execute from local directory, set remdir='./' in brainlabrc.
    Remember to specify trailing / on remdir in brainlabrc.

    Stim and report and .in files will be prepended with brainname,
    which should be unique for each job (or else they may be overwritten)

    when you run a job with a particular brainname you blow away all files beginning with
    that string in the $HOME/remdir!
    create subdir for each job named as brain name?  or preface all files with brainname? 
        latter, for now

    FIXME:  the account on the remote system is assumed to be the same username
    on the local system.  make this more general.  Save info into a config file.
    Detect if config file is not present, and ask the user to config.
"""

# These can be overridden in a .brainlabrc file:
remoteexec=False
remotemachine="localhost"
remdir="remote-invoke/"
#ncscmd="ncs4p"
ncscmd='/home/virtus/Desktop/brainlab/ncs5p'     # make sure the mpich invocation agrees with binary (ethernet or myrinet) on next line
#ncscmd="ncs5mStim_2005_06_23"
#mcmd='/opt/mpich/gnu/bin/mpirun'
mcmd='/usr/bin/mpirun'
nolocal=False

verbose=True
# look for ./.brainlabrc, or (later) $HOME/.brainlabrc
# if that fails, look for brainlabrc with no leading .
try:
    # set our global namespace to be execfile's local namespace
    # so variables set there are changed in this module too!
    execfile('.brainlabrc', globals(), globals())
    #print "found .brainlabrc"
    #print "remoteexec is", remoteexec
except:
    #print "did not find ./.brainlabrc"
    try:
        execfile('brainlabrc', globals(), globals())
    except:
        print "WARNING:  did not find .brainlabrc or brainlabrc on host "+hn

# what char is placed by NCS between brain name and report name?
# this was "." in earlier versions, then became "-":
TXTSEP="-"

def Plot3D(b):
    return plot(b)

def Run(b, verbose=False, nprocs=1, clearreports=True, parms=None, procnum=None, showprogress=False):
    """
    Simulate the BRAIN with NCS.

    parms allows some BRAIN parms to be overridden, if desired,
    for example, change the job name of an existing brain model after adjustment.

    This was changed from being a BRAIN.method to a brainlab function taking a BRAIN as a parameter.
    """
    if parms is not None:
        newparms=InitParms(parms, b.pt)
        for k in newparms:
            #print "overriding parm", k
            b.parms[k]=newparms[k]
    return run(b, verbose=verbose, nprocs=nprocs, clearreports=clearreports, procnum=procnum, showprogress=showprogress)

def run(b, verbose=False, nprocs=1, clearreports=True, procnum=None, showprogress=False):
    """ Run a brain, possibly locally or on remote compute machine or cluster.

        Currently, this should not be invoked directly.  It is invoked
        from a brainlab's Run() function (formerly it was invoked as a BRAIN.Run() method,
        which is now deprecated).

        FIXME:  all .stm files in current dir are copied over.  This
        is rather crude but easy to do and allows use of wildcard in
        scp.  Could obviously extract the filenames from the brain.

        If procnum is not None, we assume this to be a single processor
        job we are to execute on machine procnum.  nprocs is ignored
        in this case.

        This is called from brain.Run() method . . . is this a good
        way of doing it?  Maybe do away with method and just make it a function.

        Note:  changed nlog.txt to use brainname rather than procnum,
        since may have multiple jobs on a procnum.  Obviously, make
        sure brainnames are unique.
    """
    brainname=b.GetBrainJob()
    #if remdir[0]!='/':
    #    tmpdir=join("\$HOME", remdir)
    #else:
    #    tmpdir=remdir
    tmpdir=remdir

    # this is a bit risky . . . 
    # remove local files to make sure we have a clean working dir
    #if verbose: print "remote dir will be",tmpdir
    if 0:
        if verbose: print "run:  NOT removing local temp files"
        print "FIXME:  should remove files that should be regenerated"
    elif 0:
        if verbose: print "run:  removing all local temp files"
        os.system("rm -f *.dat *.txt *.stm *.in")
    else:
        if verbose: print "run:  removing local temp files for brainname", brainname
        cmd="rm -f "
        cmd+=brainname+".* "
        if verbose and clearreports: print "run:  also removing local reports"
        if clearreports:
            cmd+=brainname+"-* "
        os.system(cmd)

    if verbose: print "run:  writing .in file"
    f=open(brainname+".in", "w")
    f.write(`b`)
    f.close()

    if remoteexec:
        if verbose: print "run:  clearing remote job files"
        if verbose and clearreports: print "run:  also clearing remote reports"
        # with a subdir for each job:
        #ncmd="\'rm -rf "+tmpdir+brainname+" >/dev/null 2>&1\'"
        # or with all files in remote-invoke:  (all files associated with this job begin brainname-* or brainname.*)
        # this could conceivably cause problems if people pick odd names with - in them
        ncmd="\"rm -f "
        ncmd+=tmpdir+brainname+".* "
        if clearreports:
            ncmd+=tmpdir+brainname+"-* "
        ncmd+=">/dev/null 2>&1\""
        rcmd="ssh "+remotemachine+" "+ncmd
        os.system(rcmd)
        if verbose: print rcmd

    if remoteexec:
        if verbose: print "run:  sending .in and all .stm files to cortex"
        rcmd="scp -C "+brainname+".in "+brainname+"*.stm "+remotemachine+":"+tmpdir
        if not verbose:
            rcmd+=" > /dev/null 2>&1"
        os.system(rcmd)
        if verbose: print rcmd

    machfile="/usr/lib/mpich-mpd/share/machines.LINUX"
    logfile="%s-nlog.txt"%brainname
    if procnum is not None:
        # we are to execute on machine number indicated in procnum, only.
        # future:  allow nprocs number of machines starting at procnum
        # future:  invoke a brainlab script with a command line option instead
        # of doing this crufty egrep/head/tail thing
        nprocs=1
        procnum=`int(procnum)`
        machfile+=procnum
        ncmd="cd "+tmpdir+"; cat mach | egrep -v '^#' | head -"+procnum+" | tail -1 > "+machfile+""
        if remoteexec:
            # dynamically create the mach file on remote by extracting the procnumth
            # non-comment line from the base mach file (which we assume contains a
            # list of functioning nodes) 
            rcmd='ssh '+remotemachine+' '+'"'+ncmd+'"'
            if verbose: print "mach file creation command is:", rcmd
            os.system(rcmd)
            #logfile="nlog"+procnum+".txt"
        else:
            # just create the file in the local dir 
            os.system(ncmd)

    if nolocal: nlcl="-nolocal"
    else: nlcl=""
    #cmd='/opt/mpich/myrinet/gnu/bin/mpirun'
    # old way, where tmpdir was prepended to most paths:
    #ncmd="cd "+tmpdir+"; "+mcmd+" "+nlcl+" -np "+`nprocs`+\
    #     " -machinefile "+tmpdir+machfile+" "+tmpdir+ncscmd+" "+\
    #     tmpdir+brainname+".in -d "+tmpdir   # end quote after I/O redir
    # new way, where paths are assumed to be absolute, or relative to tmpdir:
    ncmd="cd "+tmpdir+"; "+mcmd+" -machinefile "+machfile+" "+nlcl+\
	 " -np "+`nprocs`+\
	 " "+ncscmd+" "+\
         brainname+".in -d ./"   # end quote after I/O redir
    print "command is:", ncmd
    fp=-1
    if not showprogress:       # save results to log file and then examine log file
        ncmd+=" > "+logfile+" 2>&1"             # results will go into exec directory (where we cd to to run cmd)
        #if verbose: print rcmd
        if remoteexec:
            rcmd="ssh "+remotemachine+" \""+ncmd+"\""
        else:
            rcmd=ncmd
        if remoteexec and verbose: print "run:  invoking NCS on "+remotemachine+" (with status to log file)"
        if remoteexec and verbose: print "remote command is:", rcmd
        f=os.popen(rcmd)
        l=f.readline()
        while l:
            if verbose: print l
            l=f.readline()
        f.close()

        if verbose: print "run:  verifying completion"
        if remoteexec:
            rcmd="rm -f "+logfile+"; scp -C "+remotemachine+":"+tmpdir+logfile+" . > /dev/null 2>&1"
            #if verbose: print rcmd
            os.system(rcmd)

        # check logfile to see if run completed OK; if it didn't, raise exception
        try:
            f=open(logfile, "r")
        except:
            print logfile+" does not exist"
        if not f:
            print "run:  no "+logfile+"!  run must have failed"
            return False
        # note that you cannot rely on end of nlog.txt to be "thinking finished" from invoke
        # node; the Node complete messages can be interleaved with the invoke node lines.  blargh.
        # we'll just check the entire file for "thinking finished".  costly, but oh well.
        #el=f[-1]
        #f.seek(-200, 2)
        #for l in f: pass        # inefficient without seek -200
        #if verbose: print "last line is", l
        # NOTE!  sometimes one of the .dat files isn't being copied over--NFS issue, trying to copy
        # before NFS let's us see the compute node has written the file?
        # moved that copy until after nlog.txt copy and scan . . . seemed to make it reliable
        try:
            f.seek(-4096, 2)    # seek past "Cortical Simulator over" messages from compute nodes
        except:
            if verbose: print "run:  could not seek back in result file"
        l=f.readline()
        #for l in f:
        while l:
            fp=l.find("Total run time = ")
            if fp >=0:
                if verbose: print "run: ", l,
                break
            l=f.readline()
        if fp < 0:
            print "NCS run did not complete.  Examine local file "+logfile
            return False
    else:   # read NCS progress from network
        if not remoteexec:
            print "Running with progress status is only supported for remote execution for now.  Complain"
            sys.exit(0)
        if verbose: print "run:  invoking NCS on "+remotemachine+" (with status read)"
        ncmd+=" 2> "+tmpdir+logfile+"\""
        rcmd="ssh "+remotemachine+" "+ncmd+" 2> /dev/null"
        if verbose: print rcmd
        f=os.popen(rcmd)
        nl=0
        l=f.readline()
        while l:
            #if verbose: print l
            fp=l.find("Total run time = ")
            if fp >=0:
                if verbose: print "run:  line "+`nl`+":"+l,
                break
            nl+=1
            if nl%1000 == 0:
                if verbose: print "run:  line "+`nl`+":"+l,
            l=f.readline()
        f.close()
        if fp < 0:
            print "NCS run did not complete.\nLook in %s on remote or try this command directly:\n%s" %(logfile, rcmd)
            return False

    if remoteexec:
        if 1:
            if verbose: print "run:  NOT copying *.txt reports back"
        else:   # copy on demand (we may not copy the full reports, just get list of spikes from remote)
            if verbose: print "run:  copying *.txt reports back"
            rcmd="scp -C "+remotemachine+":"+tmpdir+"/*.txt ."
            if not verbose:
                rcmd+=" > /dev/null 2>&1"
            os.system(rcmd)

        # figure out how to copy multiple file extensions with wildcards in one command (use {})
        if 1:
            if verbose: print "run:  NOT copying *.dat brain maps back"
        else:
            if verbose: print "run:  copying *.dat brain maps back"
            rcmd="scp -C "+remotemachine+":"+tmpdir+"/*.dat . > /dev/null 2>&1"
            os.system(rcmd)

    # clear away temporary workdir (not using temporary workdirs for now!)
    if 1:
        if verbose: print "run:  NOT deleting workdir"
    else:
        if verbose: print "run:  deleting workdir"
        if remoteexec:
            ncmd="\'rm -rf "+tmpdir+" >/dev/null 2>&1\'"
            rcmd="ssh "+remotemachine+" "+ncmd
            #if verbose: print rcmd
            os.system(rcmd)

    if verbose: print "run:  complete OK"
    return True

# figure management:

def nextfigure(figsize=None, dpi=300):
    """ Wrapper for figure() to automatically get a new figure number each call.
        I thought figure() could automatically get a new figure with each call, but that
        does not seem to happen.  Even if you draw() in between.
        Unlike figure(), this returns int figure number instead of handle
        you can get the handle from the figure number via gcf() but apparently
        cannot get the figure number from the handle.
        At some point, figure out how to pass through all the arguments that figure()
        can take.
    """
    global fignum
    fn=fignum
    fignum+=1
    #print "figsize is", figsize
    figure(fn, figsize, dpi=dpi)
    return fn
    #return figure(fn, figsize)

def getfignum():
    global fignum
    return fignum

def addfignum(n):
    global fignum
    fignum+=n

# file loading/caching utilities:

def TimeFilterSpikeList(s, starttime, endtime):
    if starttime is None and endtime is None: return s
    ns=[]
    for l in s:
        nl=[v for v in l if ((starttime is None) or (v >= starttime)) and ((endtime is None) or (v < endtime))]
        print nl
        ns.append(nl)
    return ns

def FetchFromWorkDir(fn):
    #tmpdir=join("\$HOME", remdir)
    tmpdir=remdir
    rcmd="scp -C "+remotemachine+":"+tmpdir+fn+" . > /dev/null 2>&1"
    print rcmd
    os.system(rcmd)

def LoadSpikeData(brainname, f, starttime=None, endtime=None, fsv=10000, thresh=28.0, bigfile=True, rem=True, verbose=False):
    """ Get spike times from NCS voltage report f for brain brainname.

    Returns a list of lists of spike times.  List returned has one
    list for each cell in the indicated file.  So if only one
    cell, r[0] will be the only list of spike times.

    Spike times are offset in seconds from starttime as a base (that
    is, if starttime is 1.0, a spike at 1.5s will be returned as a
    spike at 0.5 seconds.

    A cache file will be saved to speed future loading
    (brainname-f-.txt.spk).  Be careful you don't have stray cache files
    laying around.  Tries to do performance optimization to prevent having
    to copy over a report file:
        1.  First, load a cached saved spike file with appropriate name
        2.  Try to execute LoadSpikeData on the remote, to create the
            .spk file, and just copy the spike file back
            instead of the entire voltage file
        3.  Failing that, copy the whole voltage file over and load that

    Assumes FSV (simulation time tick) is 10000.  This is used
    in converting the timestep values in the report into seconds.
    Override with fsv= arg.

    Change this at some point to return a numpy array instead
    of Python list.  Make this a keyword option?  retnumpy=True?

    bigfile True means line-by-line loading scheme can deal with very
    large files (as opposed to the regular LoadSpikeData which can be
    faster on smallish files but loads the whole file into memory at
    once and crashes on large files)  THIS OPTION NOT USED RIGHT NOW.

    If rem is False, won't try to do anything remotely.  Useful to prevent
    recursion when already invoked remotely (rem=False is default when
    invoked from command line)

    fsv and thresh only apply when file is initially loaded; when working
    from a stored .spk cache file, those parameters are ignored

    starttime and endtime are not ignored when working from a stored
    .spk cache file; the full spike data will be loaded and only the
    spikes in the indicated range will be returned
    """
    # new:  allow variables for brainname and filename
    if brainname is not None and type(brainname) != type(""):
        # assume it is a brain object and get the JOB name
        brainname=brainname.parms['JOB']
    if type(f) is not type(""):
        # assume it is a report object and get the filename
        f=f.parms['FILENAME']
        # this is sort of ugly
        if brainname!="" and f.endswith('.txt'):
            f=f[:-4]

    loadedq=False
    if brainname=="":
        fn=f
    else:
        fn=brainname+TXTSEP+f+".txt"
    dfn=fn+".spk"
    if verbose: print "cache file is "+dfn
    try:    # is the spike data itself stored here?
        f=open(dfn)
        s=cPickle.load(f)
        f.close()
        if verbose: print "loaded spike list directly from cache file"
        return TimeFilterSpikeList(s, starttime, endtime)
    except:
        if remoteexec and rem:
            # try to execute the command on remote to create the .spk cache file
            #tmpdir=join("\$HOME", remdir)
            tmpdir=remdir
            ncmd="\"cd "+tmpdir+"; python brainlab.py --ls -b "+brainname+" -r "+f+"\""
            # +" >/dev/null 2>&1\'"
            rcmd="ssh "+remotemachine+" "+ncmd
            if verbose: print rcmd
            os.system(rcmd)
            rcmd="scp -C "+remotemachine+":"+tmpdir+dfn+" . > /dev/null 2>&1"
            if verbose: print rcmd
            os.system(rcmd)
            f=open(dfn)
            s=cPickle.load(f)
            f.close()
            if verbose: print "loaded spike list directly"
            return TimeFilterSpikeList(s, starttime, endtime)
        # make sure full report file is here, or fetch it from remote 
        try:
            f=open(fn)
            f.close()
        except:
            if verbose: print "file "+fn+" does not exist locally, fetching from work dir"
            if remoteexec:
                FetchFromWorkDir(fn)
            else:
                # print "file not found"
                return False

    fsv=float(fsv)
    if starttime is not None:
        starttimestep=starttime*fsv
    else:
        starttimestep=-1
        starttime=0.0
    if endtime is not None:
        endtimestep=endtime*fsv
    else:
        endtimestep=None
    # get the number of data elements per line
    f=open(fn)
    sp=[]
    l=f.readline()
    d=l.split()
    d=d[1:]
    # start with an empty list of spikes for each cell
    for v in d:
        sp.append([])
    f.close
    # now scan for the spikes 
    f=open(fn)
    #for l in f.readlines():
    #for l in f.xreadlines():
    ld=len(d)
    #print "ld is", ld
    for l in f:
        d=l.split()
        t=int(d[0])
        #if not t%1000: print t
        if t < starttimestep:
            continue
        if endtimestep is not None:
            if t >= endtimestep:
                break
        i=0
        if 0:
            for v in d[1:]:
                v=float(v)
                if v > thresh:
                    sp[i].append((float(t)/float(fsv))-starttime)
                i+=1
        elif 1:
            # this is slightly faster than the above (with psyco enabled)
            # d[0] is the timestep
            #print d
            gi=[i for i in range(1, ld+1) if float(d[i]) > thresh]
            #print "here", gi
            for i in gi:
                sp[i-1].append((float(t)/float(fsv))-starttime)
        else:
            # this is really slow.  why?
            # (also not tested yet)
            d=map(float, d[1:])
            s=greater(d, thresh) 
            p=numpy.nonzero(s)    # returns a tuple of arrays
            for i in p[0]:          # get the first array in tuple
                sp[i].append((float(t)/fsv)-starttime)
    f.close()
    # save a local copy of spikes, for speed on later reloads
    # but what if fn is a full path?  this will fail.  fall
    # back to local directory?
    try:
        f=open(dfn, "w")
        cPickle.dump(sp, f)
        f.close()
    except:
        print "failed to save spike cache file to %s" % dfn
    return sp

def LoadReport(brainname, f):
    """ Load text report data from NCS report f for brain brainname into an array.

        Returns numpy array.  First column in file is assumed to be timestep and is
        discarded.  Data is assumed to have same number of data values on each line.
    """
    if brainname=="":
        fn=f
    else:
        fn=brainname+TXTSEP+f+".txt"
    try:
	print "Loading report"
        a=LoadReportDataText(fn)       # returns array
    except:
        FetchFromWorkDir(fn)
        a=LoadReportDataText(fn)
    return a

def LoadReportDataTextSlow(fn):
    """
        Slow, using readlines
    """
    # first get number of elements per line
    f=open(fn)
    l=len(f.readline().split())
    #print "els per line:", l
    f.close()
    f=open(fn)
    dd=[]
    for i in f.readlines():
        d=i.split()
        dd.append(d) 
    f.close()
    return dd

def LoadReportDataText(fn, brainname="", verbose=False):
    """
        Faster, reading entire file as one string
        Pretty memory hungy though and won't work on big files . . .

        Requires local file.  Any fetching from remote should be done prior to call.
        brainname should already be prepended to files
        only operates on one file; list of file processing should be done by caller

        Change to allow reading only part of the data, within time range?
    """
    f=open(fn)
    l=len(f.readline().split())
    if verbose: print "els per line:", l
    f.close()

    f=open(fn)
    s=f.read()      # read whole file as one string
    if verbose: print "read data into string"
    words=s.split()
    if verbose: print "done with split", len(words), "words"
    # why can't I put shape in initial assignment?
    #n=numarray.array(map(float, words), shape=(l,))  # convert list to array
    n=numpy.array(map(float, words))  # convert list to array
    if verbose: print "done converting to array, map(float)"
    n.shape=(-1, l)         # first number is rows, second is cols, -1 means fit to other dimension
    if verbose: print "done changing shape"
    f.close()
    return n

def CountSpikes(brainname, rn, thresh=28.0):
    """
        examine spike report file rn, return a list of spikecounts for each cell
        for entire report
        FUTURE:  allow a duration to examine instead of entire report

        each spike should have only 1 value greater than thresh!

        change to use LoadSpikeData?
    """
    if brainname=="":
        fn=rn
    else:
        fn=brainname+TXTSEP+rn+".txt"
    f=open(fn)
    sp=[]
    l=f.readline()
    d=l.split()
    d=d[1:]
    for v in d:
        v=float(v)
        if v > thresh:
            sp.append(1)
        else:
            sp.append(0)
    for l in f.readlines():
        d=l.split()
        d=d[1:]
        i=0
        for v in d:
            v=float(v)
            if v > thresh:
                sp[i]+=1
            i+=1
    f.close
    return sp

# plot utilities:

def ThreeDPlot(b, verbose=False):   # formerly plot()
    """
        get cell and synapse (and later, spike) data back
        show onscreen in 3d view
        assumes sim has already been run, and results copied back
    """
    #run(b)
    #print "plot:  retrieving results from cortex"

    brainname=b.GetBrainJob()
    brainmap=brainname+".cells.dat"
    synfile=brainname+".synapse.dat"
    (cells, idxstart, maxcell)=ReadBrainmap2(brainmap)
    (syns, esyns, isyns)=ReadSynmap2(synfile, idxstart, maxcell)
    NetPlot(cells, idxstart, maxcell, esyns, isyns, syns)

def SpikePatternPlot(brainname, filelist, starttime=None, endtime=None, fsv=10000, thresh=28.0, newfigure=True, xlab=None, ylab=None, xrange=None):
    """ Scatter plot showing only spike times
        The first method takes up lots of memory.  Recode to avoid loading the entire thing into memory.
        Change to use LoadSpikeData.
        set xlab="" to have no x axis label, or some other string, otherwise default will be used
        set ylab="" to have no y axis label, or some other string, otherwise default will be used
        FIXME:  change to use list of filenames?
    """
    # handle multiple files?  how plot them all together?
    # for now, just do first item in list, if list
    if type(filelist)==type([]):
        f=filelist[0]
    else: f=filelist

    if newfigure:  nextfigure()
    if brainname=="":
        fn=f
    else:
        fn=brainname+TXTSEP+f+".txt"
    if 0:       # memory hungry way that loads into string and then converts to numpy array
        n=LoadReportDataText(fn)
        r,c=n.shape
        for i in range(1, c):
            s=greater(n[:,i], thresh) 
            f=numpy.nonzero(s)    # returns a tuple of arrays
            f=f[0]          # get the first array in tuple
            tr=f.shape
            cellno=i*ones(tr)    # an array of tr rows of value i (cell number)
            #scatter(cellno, f)
            if len(f) > 0:      # error if we do a scatter on empty list
                scatter(f, cellno)  # put time on x axis
    else:    # less memory hungry way, maybe slower since data loaded line by line
        n=LoadSpikeData(brainname, f, starttime=starttime, endtime=endtime, fsv=fsv, thresh=thresh)
        i=1
        for l in n:
            cellno=len(l)*[i]
            #scatter(l, cellno)
            if len(l) > 0:  # error if we do a scatter on empty list
                scatter(l, cellno, marker='d', s=8, label="spike")      # label doesn't seem to work in scatter plots
            i+=1
    # so cells don't plot right on border, put an extra empty space at top and bottom:
    xmin, xmax, ymin, ymax=axis()
    axis([xmin, xmax, ymin-1, ymax+1])
    if xlab is None: xlabel("Time (sec)")
    else: xlabel(xlab)
    if ylab is None: ylabel("Cell number")
    else: ylabel(ylab)
    if xrange is not None:
        l,h=xrange
        xlim(l, h)

def ReportSpikePlot(brainname, filelist, usematplotlib=True, newfigure=True, xrange=None):
    """ A neuroplot style false-color plot, typically used when the
        number of cells is large.

        No direct Gnuplot version of this; matplotlib version works though.
    """
    if newfigure:  nextfigure()
    if usematplotlib:
        for f in filelist:
            if brainname=="":
                fn=f
            else:
                fn=brainname+TXTSEP+f+".txt"
            try:
                a=LoadReportDataText(fn)       # returns array
            except:
                FetchFromWorkDir(fn)
                a=LoadReportDataText(fn)
            if xrange is not None:
                l,h=xrange
                a=a[l:h,:]
            # skip col 0 which is timestamp. works, somewhat slow:
            a=transpose(a[:,1:])
            # change to pass to LoadReportData?
            # the transpose is pretty quick, but the call to pcolor takes a while
            if 0:
                pcolor(a, shading='flat')
            # also works, much faster, but seems to do some smoothing that is not desired:
            elif 1:
                # interp='neareset' does away with smoothing
                im=imshow(a, cmap=cm.jet, interpolation='nearest')
            else:
                # figimage will not scale things up, but it is fastest
                # unless there are a lot of cells, things will look pretty squished
                figimage(a)

def ReportPlot(brainname, filelist, cols=None, usematplotlib=True, plottype=None, plottitle=None, xlab=None, ylab=None, linelab=None, dosave=False, newfigure=True, legendloc=None, xrange=None, filter=None):
    """
        A voltage/current vs. time line plot of one or more cells.

        Add countspikes param to add spike count to title on separate line?
        Or more general way of fetching data (if needed) and analyzing data
        (with stat package like R, perhaps).

        If cols is None, plot all the cols in the file.  Otherwise, it should be a list
        of cell numbers to plot.  1 is the lowest numbered cell (FIXME:  compare to SpikePlot . . . )

        If filter is not None, plot only every filter'th element.  Useful when result will
        be converted to postscript and you don't want a huge file.

        FIXME:  now takes a single title, needs to be a list of titles if more than one file . . .
        should check to see if filelist is actually a list

        caller must do a show() if using matplotlib
        Pass dosave=".ps" to save postscript, dosave=".png" to save png.
    """
    if type(filelist)==type(""):
        filelist=[filelist]
    if usematplotlib:
        if newfigure:  nextfigure()
        #rc('xtick', labelsize=2)
        ln=0        # index into line label list
        for f in filelist:
	    print "File: "+f
            if brainname=="":
                fn=f
            else:
                fn=brainname+TXTSEP+f+".txt"
            try:
		print "LoadReportDataSlow (was without Slow)"
                a=LoadReportDataText(fn)       # returns array
            except:
                #print "fetching file from remote"
                FetchFromWorkDir(fn)
                a=LoadReportDataText(fn)        # returns array

	    print "We have loaded the data report"

            #print "data is", a
            #plot(a)
            #plot(a[:,0], a[:,1:-1])        # can't have more than 1 y value?
            if plottype=="scatter":
                # scatter plot (typically of USE or RSE vals) where each line has a timestep followed by some
                # number of data values we wish to plot for that timestep.  should be same number of datapts on each line.
                #print "scatter plot"
                if type(a)==type([]):
                    print "ReportPlot FIXME:  plot from list not working"
                else:
                    svals, yvals=a.shape
                    print "svals:", svals, "yvals:", yvals
                    if 0:       # old, seemingly broken way
                        for yv in range(1, yvals):
                            #print yv, ; sys.stdout.flush()
                            ts=a[yv,0]
                            #print "ts:", ts
                            #print "first line:", a[yv,1:]
                            #scatter(a[yv,1:], (svals-1)*[ts])  # time on y axis
                            scatter((svals-1)*[ts], a[yv,1:])   # time on x axis
                    else:
                        # example:  we have three cols: ts, USEcell1, USEcell2 x 3000 lines (timesteps) in file
                        # this will step through for each cell and plot its value (on y) for that timestep (on x)
                        # this is pretty much what regular plot, below, will do except points won't be connected
                        if cols is None: cols=range(1, yvals)
                        ln=0
                        for yv in cols:
                            #print "on %d" % yv
                            ts=a[0:, 0]
                            scatter(ts, a[0:, yv])
                    if xlab is not None: xlabel(xlab)
                    else: xlabel("Timestep (1e4=1sec)")
                    if ylab is not None: ylabel(ylab)
                    if plottitle is not None: title(plottitle)
                        #sys.exit(0)
                    if xrange is not None:
                        l,h=xrange
                        xlim(l, h)
                    if dosave:
                        #print "saving"
                        savefig(fn+dosave) 
            else:
                # default plot with one line for each y series vs x
		print "THIS IS REACHED BEFORE KILL?"
                if type(a)==type([]):
                    print "ReportPlot FIXME:  plot from list not working"
                else:
                    svals, yvals=a.shape
                    if cols is None: cols=range(1, yvals)
                    #print "cols is", cols
                    for yv in cols:
                        x=a[:,0]
                        y=a[:,yv]
                        if filter is not None:
                            # take only every filter'th element.  this can cause missing spike peaks of course
                            x=x[::filter]
                            y=y[::filter]
                        if linelab:
                            #print "plotting, ln:", ln
                            plot(x, y, label=linelab[ln]);
                            ln+=1
                        else: plot(x, y)
                    #print "plotted"
                    if xlab is not None: xlabel(xlab)
                    else: xlabel("Timestep (1e4=1sec)")
                    if ylab is not None: ylabel(ylab)
                    else: ylabel("Voltage (mV)")
                    if plottitle is not None: title(plottitle)
                    if linelab:
                        if legendloc is not None:
                            legend(loc=legendloc)
                        else:
                            legend(loc='lower right')
                        #legend(loc='best')
                    if xrange is not None:
                        l,h=xrange
                        xlim(l, h)
                    if dosave:
                        #print "saving"
                        savefig(fn+dosave) 
    else:
        print "ReportPlot FIXME:  this may no longer be working" 
        # old, direct Gnuplot method:
        cmd="echo \"\
        set xlabel 'Time (s)';\
        set title '"+plottitle+"';\
        set ylabel 'Voltage (mV)';\
        "
        #unset grid;"
        #cmd=cmd+"set xrange [0:"+`avgxrange`+"];"
        #if avgyrange!=None:
        #    cmd=cmd+"set yrange ["+avgyrange+"];"

        cmd=cmd+"plot "
        nn=0

        for f in filelist:
            fn=brainname+TXTSEP+f+".txt"
            fi=open(fn)
            l=fi.readline()
            d=l.split()
            nd=len(d)-1
            fi.close()
            di=2
            # plot each cell in that file as a separate line
            for v in d[1:]:
                if(nn>0):
                    cmd=cmd+","     # separate each plot datum
                linetitle=f+" cell "+`di-1`
                cmd=cmd+"'"+fn+"' using (\$1 / 10000):"+`di`+" plottitle '"+linetitle+"' with lines"
                #cmd=cmd+"'"+fn+"' using 1:2 title '"+linetitle+"' with lines"
                di+=1
                nn+=1

        # conclude plot command
        cmd=cmd+"; \
        set term post eps; set output 'toplotavg.ps'; replot;\
        set term png color; set output 'toplot"+`nn`+".png'; replot;\
        \" | gnuplot -persist"

        #print "cmd is", cmd
        os.system(cmd)

def DocPlot(brain, col, hints=None, allinhib=None):
    """ Generate a .eps of layer view, using pyx, for inclusion in scientific papers etc.

        should this be called from a brain.method()?

        hmm, in current models all biological layers are compressed into one NCS layer
        and just treated as different cell groups . . . 
    """
    ca=pyx.canvas.canvas()
    textattrs = [pyx.text.halign.center, pyx.text.vshift.middlezero]
    xs=10.0
    ys=8.0

    # 0,0 is lower left corner, positive y up 

    lays=col.parms['LAYER_TYPE']
    ln=1
    # layers numbered from top down

    nlays=len(lays)

    rxs=xs
    if allinhib is not None:    # assume it is in layer list
        nlays-=1
        rxs=.6*xs

    vs=2        # leave this many times slays space above and below
    slays=ys/float(nlays+vs+vs)       # extra spacing
    ln=1
    # assume cols are in top down order
    # maybe sort by shell start fraction?

    for l in lays:
        na=l.parms['TYPE']
        if na==allinhib:        # skip a shared inhib pseudo-layer
            ytop=ys-vs*slays
            ybot=vs*slays
            b=pyx.box.polygon(corners=[(rxs, ybot), (rxs, ytop), (xs, ytop), (xs, ybot)])
            ca.stroke(b.path(), [pyx.color.rgb.green])
            ca.text(1.0, (ybot+ytop)/2.0, na, textattrs)
            continue
        print 'layer %s' % na
        cellgroups=l.parms['CELL_TYPE']
        ybot=ys-ln*slays
        ytop=ybot + slays
        print ybot, ytop
        b=pyx.box.polygon(corners=[(0, ybot), (0, ytop), (rxs, ytop), (rxs, ybot)])
        ca.stroke(b.path(), [pyx.color.rgb.green])
        ca.text(1.0, (ybot+ytop)/2.0, na, textattrs)
        for c in cellgroups:
            if type(c)==type(""):
                c=brain.celltypes[c]
            print "cellgroup", c.parms['TYPE']
        ln+=1

    ca.writeEPSfile('doc.eps')

if __name__ == "__main__":
    """ sample invocation:
        ./brainlab.py --ls -b areabrain -r EMRep -o my.out
    """
    import getopt

    brainname=""
    outfile=None
    infile=None
    action=None
    o,a=getopt.getopt(sys.argv[1:], "o:b:r:s:e:", ["ls"])
    for opt, val in o:
        if opt=="--ls":
            #print "got loadspikes", val
            action="loadspikes"
        elif opt=="-o":
            outfile=val
        elif opt=="-b":
            brainname=val
        elif opt=="-r":
            infile=val

    # invoked remotely to create the .spk file, to speed copying data across network
    if action=="loadspikes":
        print "loadspikes on brain", brainname, "report name", infile, "to file", outfile
        r=LoadSpikeData(brainname, infile, rem=False)
        if outfile is not None:
            print "FIXME:  loadspikes would save spikes here"
        # (otherwise, it saves to reportname.spk cache file)
        sys.exit(0)

    # otherwise, do performance tests:

    brainname="areabrain"
    bigfn="EMRep"       # 95 MB file.  causes great swappage on my laptop in LoadReportData (Slow or Fast)
    fn="testspikedata.txt"          # smaller test file
    #ReportPlot("", [fn], usematplotlib=True)

    doall=False

    if 1 or doall:
        print "Testing LoadReport()"
        a=LoadReport("brainlab", "testreport")
        print a

    if 0 or doall:
        ts=time.time()
        figure(1)
        SpikePatternPlot("", fn) 
        #SpikePatternPlot(brainname, bigfn)              # too much memory for my laptop w/ load-into-string
        te=time.time()
        print "SpikePatternPlot elapsed time:", te-ts

    if 0 or doall:
        ts=time.time()
        s=CountSpikes("areabrain", bigfn)
        #s=CountSpikes("", fn)
        te=time.time()
        print "CountSpikes elapsed time:", te-ts
        print s

    if 0 or doall:
        ts=time.time()
        figure(2)
        ReportSpikePlot("", [fn], usematplotlib=True)
        te=time.time()
        print "ReportSpikePlot elapsed time:", te-ts

    fn+=".txt"

    if 0:   # speed test of text spike file load routines and conversion to numpy array
        for i in range(0, 4):
            ts=time.time()
            if i%2==1:
                LoadReportDataTextSlow(fn)
                te=time.time()
                print "slow, elapsed time", te-ts
            else:
                LoadReportDataText(fn)
                te=time.time()
                print "fast, elapsed time", te-ts

    show()
