import numpy as np
import matplotlib.pyplot as plt
import json
import traceback
import requests
import matplotlib.dates
import datetime
import os
import concurrent.futures
        
def draw_data(countries,filename,x,y,xgrow,ygrow,val_type,dates):
    today=datetime.datetime.today()
    direcdate=str(today.day)+"_"+str(today.month)+str(val_type)
    if not os.path.exists(direcdate+"/point"):
        os.makedirs(direcdate+"/point")
    if not os.path.exists(direcdate+"/line"):
        os.makedirs(direcdate+"/line")
    yconvval=[]
    fig, ax = plt.subplots()   

    if dates:
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
        plt.savefig(direcdate+"/point/"+filename+"val"+".png")
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
    plt.savefig(direcdate+"/line/"+filename+"val"+"line.png")
    plt.close()

    
    if dates:
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
        plt.savefig(direcdate+"/point/"+filename+"grow"+".png")
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
    plt.savefig(direcdate+"/line/"+filename+"grow"+"line.png")
    plt.close()

def apply_convolution(x,y,xgrow,ygrow,conv_len):
    yconvval=[]
    for yi in y:
        yconva=[]
        last_conv=0
        for i in range(conv_len-1):
            yconva.append(int(last_conv))
        
        for i in range(conv_len-1,len(yi)):
            last_conv=sum([yi[j] for j in range(i-conv_len+1,i+1)])/conv_len
            yconva.append(last_conv)

        
            
        yconvval.append(yconva)
    yconvgrow=[]
    for yi in ygrow:
        yconva=[]
        last_conv=0
        for i in range(conv_len-1):
            yconva.append(int(last_conv))
            
        for i in range(conv_len-1,len(yi)):
            last_conv=sum([yi[j] for j in range(i-conv_len+1,i+1)])/conv_len
            yconva.append(last_conv)

            
        yconvgrow.append(yconva)
    
    return (yconvval,yconvgrow)

def generate_graphs(countries,filename):
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
    for i in range(len(xgrow)):
        xgrow[i].pop()
        ygrow[i].pop()
        
    (yconvval,yconvgrow)=apply_convolution(x,y,xgrow,ygrow,10)
    
    pred=[]
    for i in range(len(yconvval)):
        xi=x[i]
        yi=yconvval[i]
        yj=y[i]
        predval=(yj[len(yj)-2]/yi[len(yi)-2])*yi[len(yi)-1]
        pred.append({"country":countries[i],"val":predval,"date":str(xi[len(xi)-1])})
        
    today=datetime.datetime.today()
    file = open(str(today.day)+"_"+str(today.month)+filename+"prediction.txt", "w")
    json.dump(pred,file)
    file.close()    

    draw_data(countries,filename,x,y,xgrow,ygrow,"data",True)
    draw_data(countries,filename,x,yconvval,xgrow,yconvgrow,"conv",False)
    
if __name__ == "__main__":
    countries=["romania","germany","italy","hungary","spain","portugal","austria","denmark"]#,"france"]#,"united-states"]
    generate_graphs(countries,"grapheurope")
    generate_graphs(["china"],"graphchina")
    generate_graphs(["romania","serbia","hungary","bulgaria","ukraine","moldova"],"graphbalkan")
    generate_graphs(["romania"],"graphromania")
    generate_graphs(["united-states"],"graphus")
    generate_graphs(["united-kingdom"],"graphuk")
    
