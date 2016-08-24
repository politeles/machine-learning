import pandas as pd
import matplotlib.pyplot as plt





def run():
	""" compute stats for the learning rate """
	# load csv  files:
	learning_rate = pd.read_csv('testA05E09G01',header=None)
	gamma_rate = pd.read_csv('standard_G01_10')
	epsilon_rate = pd.read_csv('standard_E01_10')
	alpha_rate = pd.read_csv('standard_A01_10')
	best= pd.read_csv('testA05G01_E')
	try:
		print "dataset has {} samples with {} features each.".format(*learning_rate.shape)
		learning_rate.plot()
		gamma_rate.plot()
		epsilon_rate.plot()
		alpha_rate.plot()
		best.plot()

		plt.show()

	except:
    		print "Dataset could not be loaded. Is the dataset missing?"








if __name__ == '__main__':
    run()
