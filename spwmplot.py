import numpy as np
import matplotlib.pyplot as plt
import json
import traceback
delays=[0,8,16,23,31,39,47,55,63,71,78,86,93,101,108,115,122,129,
136,143,149,156,162,168,174,180,185,191,196,201,206,210,215,219,223,
227,230,234,237,239,242,244,246,248,250,251,252,253,254,254,255,254,
254,253,252,251,250,248,246,244,242,239,237,234,230,227,223,219,215,
210,206,201,196,191,185,180,174,168,162,156,149,143,136,129,122,115,
108,101,93,86,78,71,63,55,47,39,31,23,16,8,0]
time=0;
val=0
x=[]
y=[]
fact=(1.0/50/2)/sum(delays)
print(len(delays))
print(sum(delays))
for delay in delays:
    x.append(time)
    y.append(val)
    time+=delay*fact
    val=1 if val==0 else 0
for delay in delays:
    x.append(time)
    y.append(val)
    time+=delay*fact
    val=-1 if val==0 else 0
print(x)
print(y)
xsin=np.linspace(0,0.02,1000)
ysin=np.sin(2*np.pi*50*xsin)
plt.plot(xsin,ysin,color="r")
plt.step(np.array(x), np.array(y),color="b")
plt.savefig('spwm.png')
plt.show()

