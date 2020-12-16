from shodan import Shodan
import json
api = Shodan('p23Wt7wDEYuYLreW4eKzkShMi05uKcJL')
file=open("log1.txt","w")
mess=[]
for i in range(100,110):
    print(i)
    for j in range(255):
        try:
            ip='79.113.'+str(i)+'.'+str(j+1)
            #print(ip)
            ipinfo = api.host(ip)
            print(ipinfo)
            #jsoninfo=json.loads(ipinfo)
            #print(jsoninfo)
            mess.append(ipinfo)
        except:
            pass
json.dump(mess,file)
file.close()
