import numpy, scipy
from scipy.signal import square, sawtooth, correlate
from numpy import pi, random, sin
from matplotlib import pyplot

# Load data line per line (each line is one timestep)
# then take average of all neurons, so we get a list
# of the average output of the assembly per timestep
def LoadData(fn):
    f=open(fn)
    l=len(f.readline().split())
    f.close()
    f=open(fn)
    dd=[]
    for i in f.readlines():
        d=i.split()
	d.pop(0)
	#print d
	n=numpy.array(map(float, d))
	#dapp=numpy.average(n)
	dapp=d.pop(0)
        dd.append(dapp)
    f.close()
    return dd

listX = LoadData('../brainlab/vb-sync-XReport.txt')
listY = LoadData('../brainlab/vb-sync-YReport.txt')

A=numpy.array(listX)
B=numpy.array(listY)

xcorr = scipy.correlate(A, B)

period = 1.0
tmax = 2.0
nsamples = len(listX)
phase_shift = 0.6*pi #unused

t = numpy.linspace(0.0, tmax, nsamples, endpoint=False)
dt = numpy.linspace(-t[-1], t[-1], 2*nsamples-1)

recovered_time_shift = dt[xcorr.argmax()]
recovered_phase_shift = 2*pi*(((0.5 + recovered_time_shift/period) % 1.0) - 0.5)

print "xcorr = ", xcorr
print "xcorr.argmax = ", xcorr.argmax()
print "xcorr.len = ", len(xcorr)
print len(t)
print "Recovered time shift = ", recovered_time_shift
print "Recovered phase shift: %.2f pi" % (recovered_phase_shift/pi)

pyplot.plot(t, )
pyplot.show()
quit()

from pyx import canvas, graph, text, color, style, trafo, unit
from pyx.graph import axis, key

text.set(mode="latex")
text.preamble(r"\usepackage{txfonts}")
figwidth = 12
gkey = key.key(pos=None, hpos=0.05, vpos=0.8)
xaxis = axis.linear(title=r"Time, \(t\)")
yaxis = axis.linear(title="Signal", min=-5, max=17)
g = graph.graphxy(width=figwidth, x=xaxis, y=yaxis, key=gkey)
plotdata = [graph.data.values(x=t, y=signal+offset, title=label) for label, signal, offset in (r"\(A(t) = \mathrm{square}(2\pi t/T)\)", A, 2.5), (r"\(B(t) = \mathrm{sawtooth}(\phi + 2 \pi t/T)\)", B, -2.5)]
linestyles = [style.linestyle.solid, style.linejoin.round, style.linewidth.Thick, color.gradient.Rainbow, color.transparency(0.5)]
plotstyles = [graph.style.line(linestyles)]
g.plot(plotdata, plotstyles)
g.plot(graph.data.values(x=t, y=listX, title="Blah"), plotstyles)
g.text(10*unit.x_pt, 0.56*figwidth, r"\textbf{Cross correlation of noisy anharmonic signals}")
g.text(10*unit.x_pt, 0.33*figwidth, "Phase shift: input \(\phi = %.2f \,\pi\), recovered \(\phi = %.2f \,\pi\)" % (phase_shift/pi, recovered_phase_shift/pi))
xxaxis = axis.linear(title=r"Time Lag, \(\Delta t\)", min=-1.5, max=1.5)
yyaxis = axis.linear(title=r"\(A(t) \star B(t)\)")
gg = graph.graphxy(width=0.2*figwidth, x=xxaxis, y=yyaxis)
plotstyles = [graph.style.line(linestyles + [color.rgb(0.2,0.5,0.2)])]
#gg.plot(graph.data.values(x=dt, y=xcorr), plotstyles)
gg.plot(graph.data.values(x=dt, y=xcorr, title="Blah"), plotstyles)
gg.stroke(gg.xgridpath(recovered_time_shift), [style.linewidth.THIck, color.gray(0.5), color.transparency(0.7)])
ggtrafos = [trafo.translate(0.75*figwidth, 0.45*figwidth)]
g.insert(gg, ggtrafos)
g.writePDFfile("so-xcorr-pyx")
