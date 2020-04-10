import numpy as np
import matplotlib.pyplot as plt
import json
import traceback
import requests
import matplotlib.dates
import datetime
countries=["romania","germany","italy","hungary","spain","portugal"]
x=[]
y=[]
xgrow=[]
ygrow=[]
for c in countries:
    r = requests.get('https://api.covid19api.com/dayone/country/'+c+'/status/confirmed/live')
    #print(r.json())
    startval=0
    xaux=[]
    yaux=[]
    xgrowa=[]
    ygrowa=[]
    cnt=0
    init=0
    for rec in r.json():
        d=datetime.datetime.strptime(rec["Date"], "%Y-%m-%dT%H:%M:%SZ")
        xaux.append(d)
        yaux.append(rec["Cases"])
        xgrowa.append(d)
        ygrowa.append(int(rec["Cases"])-init)
        init=int(rec["Cases"])
    x.append(xaux)
    y.append(yaux)
    xgrow.append(xgrowa)
    ygrow.append(ygrowa)


fig, ax = plt.subplots()   
plt.title("Countries covid data")
plt.xlabel("Date")
plt.ylabel("Cases")
ax.xaxis.set_tick_params(rotation=30, labelsize=10)
for i in range(len(x)):
    print(countries[i])
    xi=np.array(x[i])
    yi=np.array(y[i])
    plt.plot_date(xi,yi, xdate=True, ydate=False,label=countries[i])

plt.legend()        
plt.savefig("graphval.png")
plt.close()

fig, ax = plt.subplots()   
plt.title("Countries covid growth")
plt.xlabel("Date")
plt.ylabel("Increase")
ax.xaxis.set_tick_params(rotation=30, labelsize=10)
for i in range(len(xgrow)):
    print(countries[i])
    xi=np.array(xgrow[i])
    yi=np.array(ygrow[i])
    plt.plot_date(xi,yi, xdate=True, ydate=False,label=countries[i])

plt.legend()        
plt.savefig("graphgrow.png")
plt.close()
