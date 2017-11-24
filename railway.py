import urllib.request, urllib.parse
import ssl, json,time,smtplib
from email.mime.text import MIMEText

ssl._create_default_https_context = ssl._create_unverified_context

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}


def updateStationInfoFile(version='1.1.9018'):
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?' + version
    req = urllib.request.Request(url, headers=headers)
    res = urllib.request.urlopen(req)
    data = res.read().decode('utf-8')
    with open('station_info.txt', 'w')as f:
        count = 0
        for i in data.split('@'):
            if count == 0:
                count = 1
                continue
            f.write(i + '\n')


def getStationCode(station_name):
    station_info_path = 'station_info.txt'
    with open(station_info_path, 'r') as f:
        line = f.readline()
        while (line):
            if station_name in line:
                return line.split('|')[2]
            line = f.readline()
        return None


def getStationName(station_code):
    station_info_path = 'station_info.txt'
    with open(station_info_path, 'r') as f:
        line = f.readline()
        while (line):
            if station_code in line:
                return line.split('|')[1]
            line = f.readline()
        return None


def parseInfo(raw_info):
    info_dict = {}
    splited_info = raw_info.split('|')
    info_dict['detail'] = splited_info[1]
    info_dict['train_code'] = splited_info[3]
    info_dict['from_station'] = getStationName(splited_info[6])
    info_dict['to_station'] = getStationName(splited_info[7])
    info_dict['start_time'] = splited_info[8]
    info_dict['end_time'] = splited_info[9]
    info_dict['total_time'] = splited_info[10]
    info_dict['business_seat'] = splited_info[32]
    info_dict['first_class_seat'] = splited_info[31]
    info_dict['second_class_seat'] = splited_info[32]
    info_dict['senior_soft_bed'] = splited_info[30]
    info_dict['soft_bed'] = splited_info[23]
    info_dict['hard_seat'] = splited_info[29]
    info_dict['hard_bed'] = splited_info[28]
    info_dict['stand_ticket'] = splited_info[26]
    return info_dict


def queryLeftTicket(train_date, from_station, to_station):
    from_station_code = getStationCode(from_station)
    to_station_code = getStationCode(to_station)
    query_url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=' + train_date + '&leftTicketDTO.from_station=' + from_station_code + '&leftTicketDTO.to_station=' + to_station_code + '&purpose_codes=ADULT'
    req = urllib.request.Request(query_url, headers=headers)
    res = urllib.request.urlopen(req)
    data = res.read().decode('utf-8')
    dict = json.loads(data)
    info_list = []
    if 'data' in dict.keys():
        result = dict['data']['result']
        for i in result:
            info_list.append(parseInfo(i))
    else:
        print('Can not get left ticket info')
    return info_list

def notifyByEmail(msg):
    mailto = '475212995@qq.com'
    mail_host = "smtp.163.com"
    mail_user = "m18519535426"
    mail_pass = "wy475212995"
    mail_postfix = "163.com"
    sender='余票提醒'+'<'+mail_user+'@'+mail_postfix+">"
    msg = MIMEText(msg,_subtype='plain')
    msg['Subject'] = '余票提醒'
    msg['From'] = sender
    msg['To'] = mailto
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)                            #连接服务器
        server.login(mail_user,mail_pass)               #登录操作
        server.sendmail(sender, mailto, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False

def monitorTicket(train_date,train_codes,from_station,to_station,seat_types):
    count=0
    timeflag=True
    timestamp=time.time()
    while True:
        if time.time()-timestamp>600:
            timestamp=time.time()
            timeflag=True
        count+=1
        print('###第%d次查询###'%count)
        result_list = queryLeftTicket(train_date, from_station, to_station)
        for item in result_list:
            if item['train_code'] in train_codes:
                for type in seat_types:
                    if not item[type]==None and not item[type]=='无':
                        msg='您关注的车次：'+item['train_code']+'\n'+item['from_station']+'开往'+item['to_station']+' \n起始时间：'+item['start_time']+'\n到达时间：'+item['end_time']+'\n历时：'+item['total_time']+'\n有余票了!\n'+str(item)
                        print(msg)
                        if timeflag==True:
                            result=notifyByEmail(msg)
                            if result==True:
                                timeflag=False

        time.sleep(5)




if __name__ == '__main__':
    # updateStationInfoFile()
    train_date = '2017-11-25'
    from_station = '北京'
    to_station = '呼和浩特'
    train_codes=['K1177']
    seat_types=['hard_bed']
    result_list = queryLeftTicket(train_date, from_station, to_station)
    for i in result_list:
        print(i)
    monitorTicket(train_date,train_codes,from_station,to_station,seat_types)

