import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 5, 0.1);
y1 = np.sin(x)
y2 = np.cos(x)
#plt.subplot(221)
plt.plot(x, y1,label="sin")
plt.legend()
plt.savefig("sin.png")
plt.close()
#plt.subplot(224)
plt.plot(x, y2,label="cos")

plt.title("Test 123\ndata")
plt.legend()
plt.savefig("cos.png")
plt.close()
