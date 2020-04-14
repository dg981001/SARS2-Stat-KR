"""
대구광역시 데이터 파싱 파일
확진자는 각 구청별로 가져왔고, 나머지 데이터는 시청에서 가져왔습니다. (종류별 데이터가 없는 곳이 있기 때문)
"""

import requests
import copy
from bs4 import BeautifulSoup
from form import form
import platform
import json
import re
from time import sleep

dong_gu = 'https://www.donggu.go.kr/dg/kor/corona'
jung_gu = 'http://www.djjunggu.go.kr/corona.html'
seo_gu = 'https://www.seogu.go.kr/kor/content.do?mnucd=SGMENU0100704'
yuseong_gu = 'http://www.yuseong.go.kr/corona19/'
daedeok_gu = 'https://www.daedeok.go.kr/dpt/goContents.do?link=/dpt/dpt04/DPT04010501&menuId=DPT04010501'
daegeon_si = 'https://www.daejeon.go.kr/corona19/index.do'

dir_name = 'util'

user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
headers = {'User-Agent': user_agent}


class Daegeon():
    def __init__(self):
        self.db = {
            '지역':  0,
            '확진자':  0,
            '격리자':  0,
            '사망':  0,
            '의심환자':  0,
            '검사중':  0,
            '결과음성':  0,
            '자가격리자':  0,
            '감시중':  0,
            '감시해제':  0,
            '퇴원':  0,
        }

    def dong_gu(self):
        res = requests.get(dong_gu, headers=headers)
        data = BeautifulSoup(res.content, 'html.parser')
        confirmed = int(data.find(class_='first').get_text())
        self.db['확진자'] += confirmed

        print(f"동구 : {confirmed}")

    def jung_gu(self):
        res = requests.get(jung_gu, headers=headers)
        data = BeautifulSoup(res.content, 'html.parser')
        confirmed = int(data.find(class_='top_t').find('b').get_text())
        self.db['확진자'] += confirmed

        print(f"중구 : {confirmed}")

    def seo_gu(self):
        res = requests.get(seo_gu, headers=headers, verify=False)
        data = BeautifulSoup(res.content, 'html.parser')
        confirmed = int(data.find(class_='top_mar_15 sg_table_view_01').find(
            'thead').find_all('tr')[1].find_all('td')[1].get_text())
        self.db['확진자'] += confirmed

        print(f"서구 : {confirmed}")

    def yuseong_gu(self):
        res = requests.get(yuseong_gu, headers=headers)
        data = BeautifulSoup(res.content, 'html.parser')
        confirmed = int(data.find(class_='maintable t1').find(
            class_="big").get_text())
        self.db['확진자'] += confirmed

        print(f"유성구 : {confirmed}")

    def daedeok_gu(self):
        res = requests.get(daedeok_gu, headers=headers)
        data = BeautifulSoup(res.content, 'html.parser')
        confirmed = int(data.find(
            class_='minwontb covid-19-table').find_all('tr')[1].find('span').get_text())
        self.db['확진자'] += confirmed

        print(f"대덕구 : {confirmed}")

    def collect(self):
        res = requests.get(daegeon_si, headers=headers)
        data = BeautifulSoup(res.content, 'html.parser').find(class_='corona-1').find_all('strong')
        
        stat = copy.copy(form)

        self.db = {
            '지역':  0,
            '확진자':  0,
            '격리자':  0,
            '사망':  0,
            '의심환자':  0,
            '검사중':  0,
            '결과음성':  0,
            '자가격리자':  0,
            '감시중':  0,
            '감시해제':  0,
            '퇴원':  0,
        }

        self.dong_gu()
        self.jung_gu()
        self.seo_gu()
        self.yuseong_gu()
        self.daedeok_gu()

        stat['지역'] = '대전'
        stat['확진자'] = format(self.db['확진자'])
        stat['격리자'] = data[2].get_text()
        stat['사망'] = data[3].get_text()
        stat['검사중'] = data[4].get_text()
        stat['결과음성'] = data[5].get_text()
        stat['자가격리자'] = format(int(data[6].get_text())+int(data[7].get_text()))
        stat['감시중'] = data[6].get_text()
        stat['감시해제'] = data[7].get_text()
        stat['퇴원'] = data[1].get_text()

        return stat