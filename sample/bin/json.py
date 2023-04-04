import json



def open_json_member_inf():
    with open('./docs/json/member_inf.json','r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def write_json_member_inf(data):
    with open('./docs/json/member_inf.json','w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)


def open_json_date():
    with open('./docs/json/DateCalculate.json','r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def write_json_date(data):
    with open('./docs/json/DateCalculate.json','w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)

#臉書介面
def open_json_FBpost():
    with open('./docs/json/facebook.json','r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def write_json_FBpost(data):
    with open('./docs/json/facebook.json','w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)



# 加入與離開訊息
def open_json_JoinAndLeave():
    with open('./docs/json/JoinAndLeave.json','r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def write_json_JoinAndLeave(data):
    with open('./docs/json/JoinAndLeave.json','w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)

# 權限
def open_json_permission():
    with open("./docs/json/permission.json",'r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def write_json_permission(data):
    with open("./docs/json/permission.json",'w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)


# 日期倒數

def openDate():
    with open('./docs/json/DateCalculate.json','r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def writeDate(data):
    with open('./docs/json/DateCalculate.json','w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)


# 私人頻道

def open_pc():
    with open('./docs/json/private_channel.json','r',encoding='utf8') as jfile:
        data = json.load(jfile)
    return data
def write_pc(data):
    with open('./docs/json/private_channel.json','w',encoding='utf8') as jfile:
        json.dump(data,jfile,indent=4)


def lan_data():
    with open('./docs/json/trans.json','r',encoding='utf-8') as jfile:
        return json.load(jfile)['data']

def openAnnounce():
  with open('./docs/json/announce.json','r',encoding='utf8') as jfile:
    data = json.load(jfile)
  return data
def writeAnnounce(data):
  with open('./docs/json/announce.json','w',encoding='utf8') as jfile:
    json.dump(data,jfile,indent=4)