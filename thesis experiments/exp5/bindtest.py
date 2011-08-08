#
# This is to test the "classical binding problem", i.e.,
# we have a green square and a blue triangle encoded in
# a network of 4 neurons.
#
# In order to ensure a favorable ratio for recurrence, i.e.,
# the network not dying out or getting overexcited, an
# inhibitory pool of 1 neuron (4:1 is the ratio) is added.

import brainsim
import brainalyze
import scipy
import numpy as np
import matplotlib.pyplot as plt

parameters = {
	'ESYN_MAXCONDUCTANCE':0, #0.05 ['']
	'ISYN_MAXCONDUCTANCE':0, #0.4
	'CONN_LATERAL':1, #0.02
	'CONN_INTERNAL':1, #0.02
	'ENDSIM':2, 
	'FSV':10000,
	'BRAINNAME':"prefix+num",#filled in by code
	'BRAINPREFIX':'vb-exp',
	'TAU_NOISE':0.020} #0.020

# Specified range for the NCS simulations
# make sure that both travel the same amount of steps
esynval_start=0.0
esynval_end=0.1
esynval_step=0.01
isynval_start=0.0
isynval_end=1.0
isynval_step=0.1
max_x=(esynval_end-esynval_start)/esynval_step
max_y=(isynval_end-isynval_start)/isynval_step

def run_simulations():
	esynval=esynval_start
	isynval=isynval_start
	x=0
	y=0
	while x < max_x:
		while y < max_y:
			parameters['ESYN_MAXCONDUCTANCE']=esynval
			parameters['ISYN_MAXCONDUCTANCE']=isynval
			parameters['BRAINNAME']='vb-exp'+str(x)+'-'+str(y)
			# Resulting reports:
			# vb-exp-[x]-[y]-BReport.txt
			# vb-exp-[x]-[y]-GReport.txt
			# vb-exp-[x]-[y]-TReport.txt
			# vb-exp-[x]-[y]-SReport.txt
			brainsim.simBrain(parameters)
			isynval=isynval+isynval_step
			y=y+1

		y=0 #reset
		isynval=isynval_start #reset

		esynval=esynval+esynval_step
		x=x+1

def run_analysis():
	x=0
	y=0
	corrBT=np.zeros((max_x,max_y)) # Blue Triangle
	corrGT=np.zeros((max_x,max_y)) # Green Triangle
	corrBS=np.zeros((max_x,max_y)) # Blue Square
	corrGS=np.zeros((max_x,max_y)) # Green Square
	frateB=np.zeros((max_x,max_y)) # Blue firing rate
	frateG=np.zeros((max_x,max_y)) # Green firing rate
	frateT=np.zeros((max_x,max_y)) # Triangle firing rate
	frateS=np.zeros((max_x,max_y)) # Square firing rate
	while x < max_x:
		while y < max_y:
			spikesB, spikesG, spikesT, spikesS = brainalyze.loadExperimentBind4('vb-exp', x, y)
			corrBT[x][y]=brainalyze.corr(spikesB,spikesT)
			corrGT[x][y]=brainalyze.corr(spikesG,spikesT)
			corrBS[x][y]=brainalyze.corr(spikesB,spikesS)
			corrGS[x][y]=brainalyze.corr(spikesG,spikesS)
			frateB[x][y]=brainalyze.frate(spikesB)
			frateG[x][y]=brainalyze.frate(spikesG)
			frateT[x][y]=brainalyze.frate(spikesT)
			frateS[x][y]=brainalyze.frate(spikesS)
			y=y+1
		y=0 #reset
		x=x+1

	# Save all numeric data
	np.save('corrBT.npy',corrBT)
	np.save('corrGT.npy',corrGT)
	np.save('corrBS.npy',corrBS)
	np.save('corrGS.npy',corrGS)
	np.save('frateB.npy',frateB)
	np.save('frateG.npy',frateG)
	np.save('frateT.npy',frateT)
	np.save('frateS.npy',frateS)
	return (corrBT,corrGT,corrBS,corrGS,frateB,frateG,frateT,frateS)

def run_plot_compare(f1,f2):
	f1 = np.load(f1)
	(x,y) = np.unravel_index(f1.argmax(), f1.shape)
	max=f1[x][y]
#	f1 = np.clip(f1, -max, max) # remove -1's to get a uniform plot
	
	f2 = np.load(f2)
	(x,y) = np.unravel_index(f2.argmax(), f2.shape)
	max=f2[x][y]
#	f2 = np.clip(f2, -max, max) # remove -1's to get a uniform plot

	data = f1 - f2 # numpy matrix substraction

	(x,y) = np.unravel_index(data.argmax(), data.shape)
	max=data[x][y]
	(x,y) = np.unravel_index(data.argmin(), data.shape)
	min=data[x][y]

	fig = plt.figure()
	ax = fig.add_subplot(111)

	cax = ax.imshow(data, interpolation='nearest')
	ax.set_title('Correlation Difference')
	plt.ylabel('Excitatory Conductance')
	plt.xlabel('Inhibitory Conductance')
	cbar = fig.colorbar(cax, ticks=[min, 0, max])
#	cbar.ax.set_yticklabels([str(-max), '0', str(max)])
	plt.show()

# Take differences between BT,GT and BS,GS, add to each
# other to find 'optimum'
def run_plot_compare4(f1,f2,f3,f4):
	f1 = np.load(f1)
#	(x,y) = np.unravel_index(f1.argmax(), f1.shape)
#	max=f1[x][y]
#	f1 = np.clip(f1, -max, max) # remove -1's to get a uniform plot
	
	f2 = np.load(f2)

	f3 = np.load(f3)
	f4 = np.load(f4)

	data1 = f1 - f2 # numpy matrix substraction
	data2 = f3 - f4
	data = (data1 + data2)/2

	(x,y) = np.unravel_index(data.argmax(), data.shape)
	max=data[x][y]
	(x,y) = np.unravel_index(data.argmin(), data.shape)
	min=data[x][y]

	fig = plt.figure()
	ax = fig.add_subplot(111)

	cax = ax.imshow(data, interpolation='nearest')
	ax.set_title('Correlation Difference')
	plt.ylabel('Excitatory Conductance')
	plt.xlabel('Inhibitory Conductance')
	cbar = fig.colorbar(cax, ticks=[min, 0, max])
#	cbar.ax.set_yticklabels([str(-max), '0', str(max)])
	plt.show()

#run_simulations()
#(cBT,cGT,cBS,cGS,fB,fG,fT,fS) = run_analysis()
#run_plot_compare('corrBT.npy','corrGT.npy') # is the triangle green or blue? find optimum learning-nolearning difference
#run_plot_compare('corrGS.npy','corrBS.npy') # is the triangle green or blue? find optimum learning-nolearning difference
run_plot_compare4('corrBT.npy','corrGT.npy','corrGS.npy','corrBS.npy')
