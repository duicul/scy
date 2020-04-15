import numpy as np
import matplotlib.pyplot as plt
import json
import traceback
import requests
import matplotlib.dates
import datetime
import os

def apply_convolution(x,y,conv_len):
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
    
    return yconvval

def generate_graphs():
    direcdate="romania_data"
    if not os.path.exists(direcdate):
        os.makedirs(direcdate)
    x=[]
    
    ytot=[]
    yac=[]
    ydead=[]
    yrec=[]
    ytestzi=[]
    ynrtest=[]
    
    r = requests.get("https://covid19.geo-spatial.org/api/dashboard/getDailyCases")
    for rec in r.json()["data"]["data"]:
        #print(rec["Data"])
        d=datetime.datetime.strptime(rec["Data"], "%Y-%m-%d")
        x.append(d)
        ytot.append(rec["Total"])
        yac.append(rec["Cazuri active"])
        ydead.append(rec["Morti"])
        yrec.append(rec["Vindecati"])
        ytestzi.append(rec["Nr de teste pe zi"])
        ynrtest.append(rec["Nr de teste"])

    fig, ax = plt.subplots()
    plt.title("Cases status ")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.plot(np.array(x),np.array(ytot),label="Confitrmati")
    plt.plot(np.array(x),np.array(yac),label="Active")
    plt.plot(np.array(x),np.array(ydead),label="Morti")
    plt.plot(np.array(x),np.array(yrec),label="Recuperati")
    plt.legend()        
    plt.savefig(direcdate+"/case_status"+".png")
    plt.close(fig)

    fig, ax = plt.subplots()
    plt.title("Test status ")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.plot(np.array(x),np.array(ynrtest),label="Teste")
    plt.legend()        
    plt.savefig(direcdate+"/test_status1"+".png")
    plt.close(fig)

    fig, ax = plt.subplots()
    plt.title("Test status ")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.plot(np.array(x),np.array(ytestzi),label="Teste/zi")
    plt.legend()        
    plt.savefig(direcdate+"/test_status2"+".png")
    plt.close(fig)

    estim_duration=75
    print(x[0])
    daterange=[x[0] + datetime.timedelta(days=i) for i in range(estim_duration)]
    poly_fit_ac5 = np.poly1d(np.polyfit([i for i in range(len(yac))],yac,3))
    poly_fit_tot5 = np.poly1d(np.polyfit([i for i in range(len(ytot))],ytot,3))
    poly_fit_ac4 = np.poly1d(np.polyfit([i for i in range(len(yac))],yac,4))
    poly_fit_tot4 = np.poly1d(np.polyfit([i for i in range(len(ytot))],ytot,4))
    yregrac4=[poly_fit_ac4(i) for i in range(estim_duration)]
    yregrtot4=[poly_fit_tot4(i) for i in range(estim_duration)]
    yregrac5=[poly_fit_ac5(i) for i in range(estim_duration)]
    yregrtot5=[poly_fit_tot5(i) for i in range(estim_duration)]
    fig, ax = plt.subplots()
    plt.title("Regression Aproximation ")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.plot(np.array(daterange),np.array(yregrac5),label="Active_regr3")
    plt.plot(np.array(daterange),np.array(yregrtot5),label="Confirmati_regr3")
    plt.plot(np.array(daterange),np.array(yregrac4),label="Active_regr4")
    plt.plot(np.array(daterange),np.array(yregrtot4),label="Confirmati_regr4")
    plt.plot(np.array(x),np.array(ytot),label="Confitrmati")
    plt.plot(np.array(x),np.array(yac),label="Active")
    plt.legend()        
    plt.savefig(direcdate+"/regression_status"+".png")
    plt.close(fig)

    ycon=yac+[yac[len(yac)-1]]
    xcon=x+[x[len(x)-1]+datetime.timedelta(1)]
    pred_range=10
    for i in range(5):
        ycon+=[ycon[len(ycon)-1]]
        xcon+=[xcon[len(xcon)-1]+datetime.timedelta(1)]

    ycon = apply_convolution([xcon],[ycon],5)
    ycon=ycon[0]
    print(yac)
    print(ycon)
    fact_conv=ycon[len(yac)-1]/yac[len(yac)-1]
    print(fact_conv)
    ycon=list(map(lambda x:x/fact_conv,ycon))
    fig, ax = plt.subplots()
    plt.title("Convolution Aproximation ")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.plot(np.array(xcon),np.array(ycon),label="Active convolution")
    plt.plot(np.array(x),np.array(yac),label="Active ")
    plt.legend()        
    plt.savefig(direcdate+"/convolution_status"+".png")
    plt.close(fig)
            
    
if __name__=="__main__":
    generate_graphs()
