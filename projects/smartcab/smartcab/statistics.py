import pandas as pd
import matplotlib.pyplot as plt
import scipy 
import math




def run():
	""" compute stats for the learning rate """
	# load csv  files:
	#learning_rate = pd.read_csv('testA05E09G01',header=None)
	#gamma_rate = pd.read_csv('standard_G01_10')
	#epsilon_rate = pd.read_csv('standard_E01_10')
	#alpha_rate = pd.read_csv('standard_A01_10')
	best= pd.read_csv('testA05G01_E')
	manhattan = pd.read_csv('start_end_deadline')
	optimal = pd.read_csv('optimal2')
	diff = pd.read_csv('diff')

	try:
		print "dataset has {} samples with {} features each.".format(*optimal.shape)
		# compute manhattan distance:
		#print "code"
		for idx,row in manhattan.iterrows():
			#print idx
			u = list()
			v = list()
			u.append(row.x1)
			u.append(row.y1)
			v.append(row.x2)
			v.append(row.y2)
			#print "U: {}, V : {}".format(u,v)
			md = math.fabs(row.x2-row.x1)+math.fabs(row.y2-row.y1)
			print "Deadline {}, distance {}, result: {}".format(row.deadline,md,row.deadline-md)
#

		#manhattan['distance'] = manhattan.apply(lambda row: sp.spatial.distance.cityblock([row['x1'],row['y1']],[row['x2'].row['y2']]), axis=1)

		#print manhattan

		#learning_rate.plot()
		#gamma_rate.plot()
		#epsilon_rate.plot()
		#alpha_rate.plot()
		best.plot()
		optimal.plot()
		diff.iloc[80:].plot()
##
		plt.show()

	except:
		print "Unexpected error:"
		raise
    #		print "Dataset could not be loaded. Is the dataset missing?"






if __name__ == '__main__':
	run()
