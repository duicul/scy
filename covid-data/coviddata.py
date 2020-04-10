import numpy as np
import matplotlib.pyplot as plt
import json
import traceback
import requests
import matplotlib.dates
import datetime
countries=["romania","germany","italy","hungary","spain","portugal","hungary","austria","denmark","france"]#,"united-states"]
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
    date_init=None
    prev_app=0
    if c=="united-states" or c=="china":
        for rec in r.json():
            d=datetime.datetime.strptime(rec["Date"], "%Y-%m-%dT%H:%M:%SZ")
            if date_init != None and date_init.year == d.year and  date_init.month == d.month and date_init.day == d.day:
                #print("yes")
                #yaux.append(rec["Cases"]+init)
                #ygrowa.append(int(rec["Cases"])-init)
                init=abs(int(rec["Cases"]))+init
            else :
                init+=rec["Cases"]
                xaux.append(d)
                yaux.append(abs(init))
                xgrowa.append(d)
                ygrowa.append(init-prev_app)
                prev_app=init
                init=0#int(rec["Cases"])
                date_init=d
    else:
        for rec in r.json():       
            if int(rec["Cases"]) ==0:
                continue
            try:
                prov=rec["Province"]
                continue
            except KeyError:
                pass
            d=datetime.datetime.strptime(rec["Date"], "%Y-%m-%dT%H:%M:%SZ")
            init+=rec["Cases"]
            xaux.append(d)
            yaux.append(abs(init))
            xgrowa.append(d)
            ygrowa.append(int(rec["Cases"])-prev_app)
            prev_app=init
            init=0#int(rec["Cases"])
            date_init=d
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
