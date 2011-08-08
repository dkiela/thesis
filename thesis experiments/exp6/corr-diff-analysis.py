import numpy as np
import matplotlib.pyplot as plt

# Print out top 10 maximum correlations, plus their indices
def top10_max(data):
	(x,y) = np.unravel_index(data.argmax(), data.shape)
	i=1
	max10=[]
	while i <= 10:
		(x,y) = np.unravel_index(data.argmax(), data.shape)
		max10.append((x,y,data[x][y]))
		data[x][y]=-1
		i=i+1
	print max10

f1 = np.load('corrBT.npy')
f2 = np.load('corrGT.npy')
f3 = np.load('corrBS.npy')
f4 = np.load('corrGS.npy')

# Corr(Blue,Blue)=1.1498987188956005
# Corr(Green,Green)=1.3479229292024695
cBmax=1.0045651267107822
cGmax=1.0486272477277805

def fmin(f):
	(x,y) = np.unravel_index(f.argmin(), f.shape)
	return abs(f[x][y])

avg_diff=np.zeros((100,100))
avgList=[]
x=0
y=0
while x < 100:
	while y < 100:
		#(x,y) = np.unravel_index(data.argmax(), data.shape)
		bTp=(f1[x][y]/(cBmax))*100
		gTp=(f2[x][y]/(cGmax))*100
		bSp=(f3[x][y]/(cBmax))*100
		gSp=(f4[x][y]/(cBmax))*100

		# only display when correct
		if gSp > bSp and bTp > gTp:
			print "Blue Triangle", bTp
			print "Green Triangle", gTp
			print "Blue Square", gSp
			print "Green Square", bSp
			avg_diff[x][y]=(abs(bTp-gTp)+abs(bSp-gSp))/2
			avgList.append((x,y,abs(bTp-gTp),abs(bSp-gSp),avg_diff[x][y]))
		else:
			avg_diff[x][y]=-1
		y=y+1
	y=0
	x=x+1

avgList.sort(key=lambda (x, y, z, p, q): q)
print avgList[-10:] #display ten best cases

#space=np.linspace(0.0,10000,len(diffT))
#plt.plot(space,diffT,space,diffS,space,diffAVG,'r')
#plt.show()
data=avg_diff
(x,y) = np.unravel_index(data.argmax(), data.shape)
max=data[x][y]
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.imshow(data, interpolation='nearest')
ax.set_title('Average Percentage Differentiation (distinguishability)')
plt.ylabel('Excitatory Conductance')
plt.xlabel('Inhibitory Conductance')
cbar = fig.colorbar(cax, ticks=[-1, 0, max])
plt.show()
