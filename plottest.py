import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5, 0.1);
y = np.sin(x)
plt.subplot(221)
plt.plot(x, y)
plt.subplot(224)
plt.plot(x, y)
plt.show()
