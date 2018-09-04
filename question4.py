import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# Draw sample from a distribution  
loc, scale = 2, 0.1
samples = np.random.gumbel(loc, scale, 1000)    

# Perform the transformation on the samples here ...
#samples = np.log(samples)
#samples = 1/samples
samples = np.sqrt(samples)
# samples = np.e(samples)
# samples = samples*samples
count, bins, ignored = plt.hist(samples, 100)
print "Mean = " + str(np.mean(samples))
print "STD = " + str(np.std(samples))
plt.show()