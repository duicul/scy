import numpy as np
import matplotlib.pyplot as plt
import json
import traceback
import requests
import matplotlib.dates
import datetime
import time
import os
import random
import concurrent.futures
from scipy.stats import norm
import math


def generate_graphs_confirmed(countries):
    x=[]
    y=[]
    xgrow=[]
    ygrow=[]
    for c in countries:
        r = requests.get('https://api.covid19api.com/live/country/'+c+'/status/active')
        print(c)
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
                    init=abs(int(rec["Active"]))+init
                else :
                    init+=rec["Active"]
                    xaux.append(d)
                    yaux.append(abs(init))
                    xgrowa.append(d)
                    ygrowa.append(init-prev_app)
                    prev_app=init
                    init=0#int(rec["Cases"])
                    date_init=d
        else:
            for rec in r.json():
                #print(rec)
                if int(rec["Confirmed"]) ==0:
                    continue
                try:
                    prov=rec["Province"]
                    if len(rec["Province"])!=0:
                        continue
                except KeyError:
                    pass
                d=datetime.datetime.strptime(rec["Date"], "%Y-%m-%dT%H:%M:%SZ")
                init+=rec["Active"]
                xaux.append(d)
                yaux.append(abs(init))
                xgrowa.append(d)
                ygrowa.append(int(rec["Active"])-prev_app)
                prev_app=init
                init=0#int(rec["Cases"])
                date_init=d
        #print(xaux)
        #print(yaux)
        #print(xgrowa)
        #print(ygrowa)
        x.append(xaux)
        y.append(yaux)
        xgrow.append(xgrowa)
        ygrow.append(ygrowa)
    for i in range(len(xgrow)):
        xgrow[i].pop()
        ygrow[i].pop()
    return (x,y,xgrow,ygrow,countries)

def generate_data(miu,sig,fact):
    datalen=60
    middle=60/2
    vals=[norm.pdf(x,miu,sig) for x in range(int(-middle),int(middle))]
    #print("fact "+str(fact)+" sigma "+str(sig)+" miu "+str(miu+middle)+"  val miu "+str(vals[int(miu+middle)]))
    fact=fact/vals[int(miu+middle)]
    vals=list(map(lambda x:int(x*fact),vals))
    return vals

def plot_datset(dataset,dates):
    plt.plot(dates,np.array(dataset))
    plt.show()
    plt.close('all')

def plot_predict(pred,real,dates):
    #plt.plot(dates,np.array(real),label="Real values")
    plt.plot(dates,np.array(pred),label="Predict")
    plt.legend()
    plt.show()
    plt.close('all')

def optimize(countries,polgrade,dura):
    if not os.path.exists("regression"):
        os.makedirs("regression")
    (x,y,xgrow,ygrow,countries)=generate_graphs_confirmed(countries)
    for i in range(len(x)):
        initdate=x[i][0]
        #print(initdate)
        #print(len(x[i]))
        daterange=[initdate + datetime.timedelta(days=x) for x in range(dura[i][0])]
        daterangegr=[initdate + datetime.timedelta(days=x) for x in range(dura[i][1])]
        xdata=[i for i in range(len(x[i]))]
        ydata=y[i]
        xdatagr=[i for i in range(len(xgrow[i]))]
        ydatagr=ygrow[i]
        #print("fit")
        poly_fit = np.poly1d(np.polyfit(xdata,ydata,polgrade[i][0]))
        poly_fitgr = np.poly1d(np.polyfit(xdatagr,ydatagr,polgrade[i][1]))
        #print(poly_fit)
        #print(poly_fitgr)

        fig, ax = plt.subplots()
        plt.title(str(countries[i])+" real data + regression")
        plt.xlabel("Date")
        plt.ylabel("Cases")
        ax.xaxis.set_tick_params(rotation=30, labelsize=10)
        yregr=[poly_fit(i) for i in range(dura[i][0])]
        dataregr=[{'date':datarange[i],'value':yregr[i]} for i in len(dura[i][0])]
        json.dump(open("regression/"+str(countries[i])+"polyregrvsreal.txt"),dataregr)
        
        plt.plot(np.array(daterange),np.array(yregr),label="regression")
        plt.plot(np.array(x[i]),np.array(y[i]),label="real")
        plt.legend()
        plt.savefig("regression/"+str(countries[i])+"polyregrvsreal.png")
        plt.close('all')

        fig, ax = plt.subplots()
        plt.title(str(countries[i])+" real growth + regression")
        plt.xlabel("Date")
        plt.ylabel("Increase")
        ax.xaxis.set_tick_params(rotation=30, labelsize=10)
        yregrgr=[poly_fitgr(i) for i in range(dura[i][1])]
        dataregrgr=[{'date':datarangegr[i],'value':yregrgr[i]} for i in len(dura[i][0])]
        json.dump(open("regression/"+str(countries[i])+"polyregrvsrealgr.txt"),dataregr)
        plt.plot(np.array(daterangegr),np.array(yregrgr),label="regression")
        plt.plot(np.array(xgrow[i]),np.array(ygrow[i]),label="real")
        plt.legend()
        plt.savefig("regression/"+str(countries[i])+"polyregrvsrealgr.png")
        plt.close('all')

if __name__ == "__main__":
    countries=["romania"]#,"germany","spain"]#,"bulgaria"]#,"united-states","china","denmark","austria","hungary","serbia","bulgaria"]
    polgrades=[[3,3]]#,[5,5],[3,3]]#,[2,2]]#,[10,10],[10,10],[10,10],[10,10],[10,10],[10,10],[10,10]]
    dura=[[31,10]]#,[10,10],[100]]#,[100]]#,[100],[100],[100],[100],[100],[100],[100]]
    optimize(countries,polgrades,dura)#,"ukraine","spain","portugal","germany","poland","united-states","austria","denmark"],"covid1.h5")
