from bs4 import BeautifulSoup as BS
from discord.ext import commands
import requests



start_url = 'https://class.whsh.tc.edu.tw/111-2/top.asp'
base_url = 'https://class.whsh.tc.edu.tw/111-2/down.asp'
section = '?sqlstr={}&type=class&class=&weekno=&selArrange=L&selWindow=Self'

proxies = {
  'http': 'http://127.0.0.1:8080',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'DNT': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Upgrade-Insecure-Requests': '1',
}
days = 6

class_id = [
  101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,
  201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,
  301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,
  391,392,393,394,395
]

class ClassroomIdNotFound(commands.CommandError):
  """找不到課程代碼"""

class classroom_inf:
  def __init__(self,list) -> None:
      if len(list)==1:
        self.name = "空堂"
        self.teacher = "無"
      else:
        self.name= str(list[0])
        self.teacher = str(list[1])


def search_curriculum_from_class(cls:str):
  if int(cls) not in class_id:raise ClassroomIdNotFound(f'找不到班級代號 {cls}')
  session = requests.Session()
  session.headers.update(headers)
  r = session.get(start_url, proxies=proxies)
  r.encoding = 'big5'
  ul = section.format(cls)
  session.headers.update({'Referer': base_url + ul})
  rs = session.get(base_url + ul, proxies=proxies)
  rs.encoding = 'big5'
  table= BS(rs.text,'html.parser').select('.tdColumn')
  a = [
    [
      classroom_inf([k for k in table[v].getText().split(" ") if k != ''])
      for v in range(len(table)) if v%days==i
    ]
    for i in range(days)
  ]
  return a

###顯示周一課表
# print([n.name for n in search_curriculum_from_class('212')[0]])