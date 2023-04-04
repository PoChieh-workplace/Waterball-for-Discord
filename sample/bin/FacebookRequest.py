import facebook
from sample.bin.json import open_json_FBpost, write_json_FBpost


def getFbPost(name):
    data = open_json_FBpost()
    id = data[name]["url"]
    token = data[name]["token"]
    took = facebook.GraphAPI(access_token=token, version ='2.10')
    getdata = took.request(id)
    return getdata


def getFbPhoto(type:str,post_id:str):
    data = open_json_FBpost()
    token = data[type]["token"]
    took = facebook.GraphAPI(access_token=token, version ='2.12')

    d = took.request("/{}?fields=full_picture,picture".format(post_id))
    if 'full_picture' in d:return d['full_picture']
    else:return None



def updateNowId(name,getdata):
    data = open_json_FBpost()
    data[name]["id"] = getdata['posts']['data'][0]["id"]
    write_json_FBpost(data)

def getCount(name,getdata):
    data = open_json_FBpost()
    for i in range(100):
        try:fbdata = getdata['posts']['data'][99-i]
        except:continue
        if(str(fbdata['id']) == data[name]["id"]):
            updateid = 99-i
            break
        else:updateid = -1
    return updateid

# print(getFbPhoto("whsh","138525675492804"))