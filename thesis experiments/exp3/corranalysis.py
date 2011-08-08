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

data = np.load('scorr.npy') #np.flipud() to flip
(x,y) = np.unravel_index(data.argmax(), data.shape)
max=data[x][y]
data = np.clip(data, -max, max)
data = np.delete(np.delete(data,-1,0),-1,-1) #remove zeros

fig = plt.figure()
ax = fig.add_subplot(111)

cax = ax.imshow(data, interpolation='nearest')
#ax.set_title('Correlation over ESYN and ISYN')
#plt.ylabel('Excitatory Conductance')
#plt.xlabel('Inhibitory Conductance')
cbar = fig.colorbar(cax, ticks=[-max, 0, max])
cbar.ax.set_yticklabels([str(-max), '0', str(max)])
plt.show()

top10_max(data)
