import urllib.request,urllib.parse
import ssl,json
ssl._create_default_https_context = ssl._create_unverified_context
def getList():
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-11-23&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=HHC&purpose_codes=ADULT'
    url2='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    req = urllib.request.Request(url2,headers=headers)
    res = urllib.request.urlopen(req)
    data=res.read().decode('utf-8')
    # dict = json.loads(data)
    # result = dict['data']['result']
    return data

if __name__=='__main__':
    station_names=getList()
    print(station_names)
    station_name_list=station_names.split('@')
    with open('station_info.txt','w')as f:
        count=0
        for i in station_name_list:
            print(i)
            if count==0:
                count+=1
                continue
            f.write(i+'\n')




# url = "https://kyfw.12306.cn/otn/leftTicket/init"
# req=urllib.request.Request(url)
# res=urllib.request.urlopen(req)
# data = res.read()
# print(data)