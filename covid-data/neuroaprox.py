import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation,SimpleRNN
from keras.optimizers import SGD
from keras import backend as K
from keras.models import load_model
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
def generate_graphs_confirmed():
    x=[]
    y=[]
    xgrow=[]
    ygrow=[]
    r = requests.get("https://covid19.geo-spatial.org/api/dashboard/getDailyCases")
    #print(r.json())
    startval=0
    cnt=0
    init=0
    date_init=None
    prev_app=0
    data_api=r.json()['data']['data']
    for rec in data_api:
        d=datetime.datetime.strptime(rec["Data"], "%Y-%m-%d")
        init+=rec["Cazuri active"]
        x.append(d)
        y.append(abs(init))
        xgrow.append(d)
        ygrow.append(int(rec["Cazuri active"])-prev_app)
        prev_app=init
        init=0#int(rec["Cases"])
        date_init=d
    xgrow.pop()
    ygrow.pop()
    return (x,y,xgrow,ygrow)

def apply_poly(coef,x): # coef are in increasing power value
    return sum([coef[ci]*(x**ci) for ci in range(len(coef))])
    

def generate_data(coef):
    vals=[]
    datalen=60
    middle=60/2
    vals=[apply_poly(coef,x) for x in range(int(-middle),int(middle))]
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
   
def train(inps,outps,modelname):
        model = Sequential()
        print(len(inps[0]))
        model.add(Dense(int(len(inps[0])), activation='sigmoid', input_dim=len(inps[0])))
        
        for i in range(2):
            curr_size=int(len(inps[0])/(i+2))
            model.add(Dense(curr_size, activation='sigmoid'))
            #model.add(SimpleRNN(curr_size, activation='sigmoid'))
                
        model.add(Dense(len(outps[0]), activation='sigmoid'))
        sgd = SGD(lr=0.5, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='mean_squared_error',optimizer=sgd,metrics=['accuracy'])
        total_time=time.process_time_ns()
        data_total=[]
        loss=1
        acc=0
        count_loops=0
        plateau_loops=0
        loss=1
        acc=0
        dloss=0
        train_str=""
        timeout=0
        while (loss > 0.005 or acc < 0.995) and count_loops<100 :
            outstring="Training batch {} \n".format(count_loops)
            time_count=time.process_time_ns()
            model.fit(inps,outps,epochs=300,verbose=0,shuffle=True)#batch_size=50
            time_count=time.process_time_ns()-time_count
            loss_metr=model.evaluate(inps,outps,verbose=1)
            if dloss < 0  or dloss<(loss_metr[0]-loss)/2:
                plateau_loops=plateau_loops+1
            else :
                plateau_loops=0
            #K.set_value(model.optimizer.lr,0.5)  
            #dloss=loss_metr[0]-loss
            loss=loss_metr[0]
            acc=loss_metr[1]
            outstring+="loss={}% acc={} \n".format(loss,acc)
            count_loops=count_loops+1
            if plateau_loops >= 3 :
                plateau_loops=0
            #K.set_value(model.optimizer.lr,K.get_value(model.optimizer.lr)*3/4)
            outstring+="{} Loss + metrics {} , lr = {}\n".format(plateau_loops,loss_metr,K.get_value(model.optimizer.lr))
            outstring+=str(model.metrics_names)+"\n"
            outstring+="Training time {} = {}s \n".format(time_count,time_count/1000000000)
            print(outstring)
        model.save(modelname)

def predict(inp,modelname):
    inp=np.array(inp)
    print(len(inp))
    model = load_model(modelname)
    t=model.predict(np.array(inp),verbose=0)
    return t

def optimize(modelname):
    (x,y,xgrow,ygrow)=generate_graphs_confirmed()
    romaniaval=y
    initdate=x[0]
    print(initdate)
    print(len(x))
    daterange=[initdate + datetime.timedelta(days=x) for x in range(60)]
    """actualval=[]
    for i in range(len(y)):
        acv=y[i]
        last_val=int(acv[len(acv)-2]/2)
        print("last_val "+str(last_val)+" country "+str(countries[i]))
        for i in range(60-len(acv)):
            acv.append(last_val)
        actualval.append(acv)"""
    inps=[]
    outps=[]
    #miu=random.randint(0,15)
    #sigma=random.randint(10,20)
    polgrade=4
    #fact=random.randint(int(last_val/2),last_val*3)
    for x in range(100):
        coef=[(random.random()/2-1)*50 for i in range(polgrade+1)]
        outps.append(coef)
        data=generate_data(coef)
        #data=list(map(lambda x : 1/(1+math.exp(-x)),data))
        #print([miu,sigma,fact])
        #print(data)
        plot_datset(data,daterange)
        inps.append(data)

    print(outps)   
    train(np.array(inps),np.array(outps),modelname)
    pred=predict([romaniaval],modelname)
    pred_val=generate_data(pred[0])
    print("predict "+str(pred))
    plot_predict(pred_val,romaniaval,daterange)    
    
if __name__ == "__main__":
    optimize("covid1.h5")
