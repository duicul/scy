import numpy as np
import matplotlib.pyplot as plt
import json
import traceback
import requests
import matplotlib.dates
import datetime
import os

def generate_graphs(countries,filename):
    if not os.path.exists("point"):
        os.makedirs("point")
    if not os.path.exists("line"):
        os.makedirs("line")
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

    today=datetime.datetime.today()

    fig, ax = plt.subplots()   

    plt.title("Countries covid data")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    for i in range(len(x)):
        print(countries[i])
        xi=np.array(x[i])
        yi=np.array(y[i])
        plt.plot_date(xi,yi,label=countries[i], xdate=True, ydate=False)

    plt.legend()        
    plt.savefig("point/"+filename+"val"+str(today.day)+"_"+str(today.month)+".png")
    plt.close()

    fig, ax = plt.subplots()   

    plt.title("Countries covid data")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    for i in range(len(x)):
        print(countries[i])
        xi=np.array(x[i])
        yi=np.array(y[i])
        plt.plot(xi,yi,label=countries[i])#, xdate=True, ydate=False)

    plt.legend()        
    plt.savefig("line/"+filename+"val"+str(today.day)+"_"+str(today.month)+"line.png")
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
        plt.plot_date(xi,yi,label=countries[i], xdate=True, ydate=False)

    plt.legend()        
    plt.savefig("point/"+filename+"grow"+str(today.day)+"_"+str(today.month)+".png")
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
        plt.plot(xi,yi,label=countries[i])#, xdate=True, ydate=False)

    plt.legend()        
    plt.savefig("line/"+filename+"grow"+str(today.day)+"_"+str(today.month)+"line.png")
    plt.close()

if __name__ == "__main__":
    countries=["romania","germany","italy","hungary","spain","portugal","austria","denmark"]#,"france"]#,"united-states"]
    generate_graphs(countries,"grapheurope")
    generate_graphs(["china"],"graphchina")
    generate_graphs(["romania","serbia","hungary","bulgaria","ukraine","moldova"],"graphbalkan")
    generate_graphs(["romania"],"graphromania")
    generate_graphs(["united-states"],"graphus")
    generate_graphs(["united-kingdom"],"graphuk")
    
