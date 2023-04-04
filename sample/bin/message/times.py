from dateutil import tz
from core import TIME_ZONE
from datetime import datetime,date,timedelta


#時區轉換
def TimeZoneChange(time:str,type:str):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(TIME_ZONE)
    utc = datetime.strptime(time, type)
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    return central

#類型分割
def RewriteTime(time:datetime,returntype):
    return time.strftime(returntype)

#取得片段時間
def getTempNowTime(String:str):
    return int(datetime.now().strftime(String))

#距今時間計算
def dateCalculate(year,month,day):
    Calculate = date(year,month,day)-date.today()
    return Calculate.days
    
def timeCalculate(h:int=0,m:int=0,s:int=1):
    return datetime.now()+timedelta(hours=h,minutes=m,seconds=s)

class timemethod:
    
    @staticmethod
    def after(d:int=0,h:int=0,min:int=0,s:int=0):
        t = datetime.now()+timedelta(days=d,hours=h,minutes=min,seconds=s+1)
        return int(t.timestamp())

#TimeZoneChange(RewriteTime('2022-02-06T14:39:26+0000',WHSH_FUCK_TIME),WHSH_FUCK_TO_TIME)
"""時間串表示法"""

WHSH_FUCK_TO_TIME = '%Y年%m月%d日 %H:%M:%S'


"""初始轉換時間串""" ####勿動，動者後果自負####

WHSH_FUCK_TIME = '%Y-%m-%dT%H:%M:%S+0000'