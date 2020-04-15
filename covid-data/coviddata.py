import numpy as np
import matplotlib.pyplot as plt
import json
import traceback
import requests
import matplotlib.dates
import datetime
import os
import concurrent.futures
        
def draw_data(countries,filename,x,y,xgrow,ygrow,val_type,dates,case_type):
    today=datetime.datetime.today()
    day=str(today.day)
    month=str(today.month)
    direcdate=day+"_"+month
    direcdate+="/"+case_type+"/"+str(val_type)
    if not os.path.exists(direcdate+"/point") and dates:
        os.makedirs(direcdate+"/point")
    if not os.path.exists(direcdate+"/line"):
        os.makedirs(direcdate+"/line")
    yconvval=[]

    if dates:
        fig, ax = plt.subplots()
        plt.title("Countries "+str(case_type)+" covid data")
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
        plt.close(fig)

    fig, ax = plt.subplots()   

    plt.title("Countries "+str(case_type)+" covid data")
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
    plt.close(fig)

    
    if dates:
        fig, ax = plt.subplots()   
        plt.title("Countries "+str(case_type)+" covid growth")
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
        plt.close(fig)

    fig, ax = plt.subplots()   
    plt.title("Countries "+str(case_type)+" covid growth")
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
    plt.close(fig)

def apply_convolution(x,y,xgrow,ygrow,conv_len):
    yconvval=[]
    for yi in y:
        yconva=[]
        conv_len_real=len(yi) if len(yi)<conv_len else conv_len
        last_conv=sum([yi[j] for j in range(conv_len_real)])/conv_len_real
        for i in range(conv_len_real-1):
            yconva.append(int(last_conv))
        for i in range(conv_len_real-1,len(yi)):
            last_conv=sum([yi[j] for j in range(i-conv_len_real+1,i+1)])/conv_len_real
            yconva.append(last_conv)

        predval=1 if yconva[len(yconva)-2]==0 else yi[len(yi)-2]/yconva[len(yconva)-2]
        yconva=list(map(lambda x : predval * x,yconva))
            
        yconvval.append(yconva)
    yconvgrow=[]
    for yi in ygrow:
        yconva=[]
        conv_len_real=len(yi) if len(yi)<conv_len else conv_len
        last_conv=sum([yi[j] for j in range(conv_len_real)])/conv_len_real
        for i in range(conv_len_real-1):
            yconva.append(int(last_conv))
            
        for i in range(conv_len-1,len(yi)):
            last_conv=sum([yi[j] for j in range(i-conv_len_real+1,i+1)])/conv_len_real
            yconva.append(last_conv)

        predval=1 if yconva[len(yconva)-2]==0 else yi[len(yi)-2]/yconva[len(yconva)-2]
        yconva=list(map(lambda x : predval * x,yconva))
            
        yconvgrow.append(yconva)
    
    return (yconvval,yconvgrow)

def pred_conv(x,xgrow,y,ygrow,yconvval,yconvgrow,filename,case_type):
    pred=[]
    for i in range(len(yconvval)):
        xi=x[i]
        yi=yconvval[i]
        yj=y[i]
        predval=yi[len(yi)-1] if yi[len(yi)-2]==0 else (yj[len(yj)-2]/yi[len(yi)-2])*yi[len(yi)-1]
        
        xig=xgrow[i]
        yig=yconvgrow[i]
        yjg=ygrow[i]
        predgrow=yig[len(yig)-1]#(yjg[len(yjg)-2]/yig[len(yig)-2])*
        
        pred.append({"country":countries[i],"val":predval,"growth":predgrow,"date":str(xi[len(xi)-1])})
    today=datetime.datetime.today()
    day=str(today.day)
    month=str(today.month)
    direcdate=day+"_"+month+"/"+case_type
    if not os.path.exists(direcdate):
        os.makedirs(direcdate)
    file = open(direcdate+"/"+filename+"prediction.txt", "w")
    json.dump(pred,file)
    file.close()

def generate_graphs_active_dead_recov(countries,filename,conv_len):
    xac=[]
    yac=[]
    xacgrow=[]
    yacgrow=[]
    
    xdead=[]
    ydead=[]
    xdeadgrow=[]
    ydeadgrow=[]

    xrec=[]
    yrec=[]
    xrecgrow=[]
    yrecgrow=[]
    
    for c in countries:
        r = requests.get('https://api.covid19api.com/live/country/'+c+'/status/active')
        #print(r.json())
        startval=0
        
        xaca=[]
        yaca=[]
        xacgrowa=[]
        yacgrowa=[]
        
        xdeada=[]
        ydeada=[]
        xdeadgrowa=[]
        ydeadgrowa=[]

        xreca=[]
        yreca=[]
        xrecgrowa=[]
        yrecgrowa=[]
        
        inita=0
        initd=0
        initr=0
        
        date_init=None
        
        prev_appa=0
        prev_appd=0
        prev_appr=0
        
        if c=="united-states" or c=="china":
            for rec in r.json():
                d=datetime.datetime.strptime(rec["Date"], "%Y-%m-%dT%H:%M:%SZ")
                if date_init != None and date_init.year == d.year and  date_init.month == d.month and date_init.day == d.day:
                    #print("yes")
                    #yaux.append(rec["Cases"]+init)
                    #ygrowa.append(int(rec["Cases"])-init)
                    inita=abs(int(rec["Active"]))+inita
                    initd=abs(int(rec["Deaths"]))+initd
                    initr=abs(int(rec["Recovered"]))+initr
                else :
                    inita+=rec["Active"]
                    initd+=rec["Deaths"]
                    initr+=rec["Recovered"]
                    
                    xaca.append(d)
                    yaca.append(abs(inita))
                    xacgrowa.append(d)
                    yacgrowa.append(inita-prev_appa)

                    xdeada.append(d)
                    ydeada.append(abs(initd))
                    xdeadgrowa.append(d)
                    ydeadgrowa.append(initd-prev_appd)

                    xreca.append(d)
                    yreca.append(abs(initr))
                    xrecgrowa.append(d)
                    yrecgrowa.append(initr-prev_appr)
                    
                    prev_appa=inita
                    prev_appd=initd
                    prev_appr=initr
                    
                    inita=0#int(rec["Cases"])
                    initd=0
                    initr=0
                    
                    date_init=d
        else:
            for rec in r.json():       
                if int(rec["Confirmed"]) == 0:
                    continue
                try:
                    prov=rec["Province"]
                    if len(prov) != 0:
                        continue
                except KeyError:
                    pass
                d=datetime.datetime.strptime(rec["Date"], "%Y-%m-%dT%H:%M:%SZ")

                inita+=rec["Active"]
                initd+=rec["Deaths"]
                initr+=rec["Recovered"]
                
                xaca.append(d)
                yaca.append(abs(inita))
                xacgrowa.append(d)
                yacgrowa.append(inita-prev_appa)

                xdeada.append(d)
                ydeada.append(abs(initd))
                xdeadgrowa.append(d)
                ydeadgrowa.append(initd-prev_appd)

                xreca.append(d)
                yreca.append(abs(initr))
                xrecgrowa.append(d)
                yrecgrowa.append(initr-prev_appr)

                prev_appa=inita
                prev_appd=initd
                prev_appr=initr
                
                inita=0#int(rec["Cases"])
                initd=0
                initr=0
                
                date_init=d
                
        xac.append(xaca)
        yac.append(yaca)
        xacgrow.append(xacgrowa)
        yacgrow.append(yacgrowa)

        xdead.append(xdeada)
        ydead.append(ydeada)
        xdeadgrow.append(xdeadgrowa)
        ydeadgrow.append(ydeadgrowa)

        xrec.append(xreca)
        yrec.append(yreca)
        xrecgrow.append(xrecgrowa)
        yrecgrow.append(yrecgrowa)
        
    """for i in range(len(xac)):
        xac[i].append(xac[i][len(xac)-1])
        yac[i].append(yac[i][len(yac)-1])

    for i in range(len(xdead)):
        xdead[i].append(xdead[i][len(xdead)-1])
        ydead[i].append(ydead[i][len(ydead)-1])

    for i in range(len(xrec)):
        xrec[i].append(xrec[i][len(xrec)-1])
        yrec[i].append(yrec[i][len(yrec)-1])"""
    
    (yconvvalac,yconvgrowac)=apply_convolution(xac,yac,xacgrow,yacgrow,conv_len)
    (yconvvaldead,yconvgrowdead)=apply_convolution(xdead,ydead,xdeadgrow,ydeadgrow,conv_len)
    (yconvvalrec,yconvgrowrec)=apply_convolution(xrec,yrec,xrecgrow,yrecgrow,conv_len)

    dump_data(countries,xac,xacgrow,yac,yacgrow,yconvvalac,yconvgrowac,filename,"Active")
    dump_data(countries,xdead,xdeadgrow,ydead,ydeadgrow,yconvvaldead,yconvgrowdead,filename,"Dead")
    dump_data(countries,xrec,xrecgrow,yrec,yrecgrow,yconvvalrec,yconvgrowrec,filename,"Recovered")


def generate_graphs_confirmed(countries,filename,conv_len):
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
                #print(rec)
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
                #print(rec)
                if int(rec["Cases"]) ==0:
                    continue
                try:
                    prov=rec["Province"]
                    if len(prov)!=0:
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
        
    (yconvval,yconvgrow)=apply_convolution(x,y,xgrow,ygrow,conv_len)   

    dump_data(countries,x,xgrow,y,ygrow,yconvval,yconvgrow,filename,"Confirmed")


def dump_data(countries,x,xgrow,y,ygrow,yconvval,yconvgrow,filename,case_type):
    try:
        pred_conv(x,xgrow,y,ygrow,yconvval,yconvgrow,filename,case_type)
    except :
        print(traceback.format_exc())
    try:
        draw_data(countries,filename,x,y,xgrow,ygrow,"data",True,case_type)
    except :
        print(traceback.format_exc())
    try:
        draw_data(countries,filename,x,yconvval,xgrow,yconvgrow,"conv",False,case_type)
    except :
        print(traceback.format_exc())
def generate_graphs(countries,filename):
    try:
        generate_graphs_confirmed(countries,filename,10)
    except :
        print(traceback.format_exc())
    try:
        generate_graphs_active_dead_recov(countries,filename,5)
    except :
        print(traceback.format_exc())



if __name__ == "__main__":
    countries=["romania","germany","italy","hungary","spain","portugal","austria","denmark"]#,"france"]#,"united-states"]
    generate_graphs(countries,"grapheurope")
    generate_graphs(["china"],"graphchina")
    generate_graphs(["romania","serbia","hungary","bulgaria","ukraine","moldova"],"graphbalkan")
    generate_graphs(["romania"],"graphromania")
    generate_graphs(["united-states"],"graphus")
    generate_graphs(["united-kingdom"],"graphuk")
    generate_graphs(["romania","denmark"],"graphroden")
    
