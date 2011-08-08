# MOVE DATA FILES TO DIFFERENT FOLDER
from os import system

folder='./exp10-data/'
x_start=89
x_end=100
y_start=0
y_end=100
x=x_start
y=y_start
stop=False

while x <= x_end and stop is False:
	while y <= y_end and stop is False:
		print x,y
		system('mv vb-exp'+str(x)+'-'+str(y)+'-JReport.txt '+folder)
		system('mv vb-exp'+str(x)+'-'+str(y)+'-MReport.txt '+folder)
		system('mv vb-exp'+str(x)+'-'+str(y)+'-XReport.txt '+folder)
		system('mv vb-exp'+str(x)+'-'+str(y)+'-YReport.txt '+folder)
		system('mv vb-exp'+str(x)+'-'+str(y)+'-APReport.txt '+folder)
		system('mv vb-exp'+str(x)+'-'+str(y)+'-OPReport.txt '+folder)
		system('mv vb-exp'+str(x)+'-'+str(y)+'-AQReport.txt '+folder)
		system('mv vb-exp'+str(x)+'-'+str(y)+'-OQReport.txt '+folder)
		system('mv vb-exp'+str(x)+'-'+str(y)+'-IReport.txt '+folder)
		y=y+1
#		if y > 85 and x > 87:
#			stop=True
	y=0
	x=x+1
