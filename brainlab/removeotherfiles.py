# REMOVE NON-DATA FILES
from os import system

x_start=0
x_end=88
y_start=0
y_end=100
x=x_start
y=y_start
stop=False

while x <= x_end:
	print x
	system('rm -rf vb-exp'+str(x)+'-*')
	x=x+1
