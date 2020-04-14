import requests, copy
from bs4 import BeautifulSoup
#from selenium import webdriver
from util.form import form
import platform, json, re
from time import sleep

dir_name = "util"

user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
headers = {'User-Agent': user_agent}

class Incheon():
    def __init__(self):
#        options = webdriver.ChromeOptions()
#        options.add_argument('headless')
#        f_driver = ''
#        if platform.system() == 'Linux':
#            f_driver = '%s/chromedriver'%(dir_name)
#        elif platform.system() == 'Darwin':
#            f_driver = '%s/chromedriver_darwin'%(dir_name)
#        else:
#            f_driver = '%s/chromedriver.exe'%(dir_name)
#        self.driver = webdriver.Chrome(f_driver, chrome_options=options)
        self.db = {
            '지역'          :  0,
            '확진자'        :  0,
            '격리자'        :  0,
            '사망'        :  0,
            '의심환자'      :  0,
            '검사중'        :  0,
            '결과음성'      :  0,
            '자가격리자'    :  0,
            '감시중'        :  0,
            '감시해제'      :  0,
            '퇴원'          :  0,
            }

    def ic_jung_gu(self): # 인천 중구
        res = requests.get('http://www.icjg.go.kr/corona19', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자   |  완치자
        # 자가격리 | 검사중
        table = soup.find('div', 'state-box-wrap').find_all('span')
            
        self.db['확진자'] += int(table[1].text.replace(",",""))
        self.db['완치자'] += int(table[2].text.replace(",",""))
        self.db['자가격리자'] += int(table[3].text.replace(",",""))
        self.db['검사중'] += int(table[4].text.replace(",",""))

        print(u"# 인천 중구 : %d"%(int(table[1].text.replace(",",""))))

    def ic_dong_gu(self):
        res = requests.get('http://www.icdonggu.go.kr/covid-19/', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자   |  접촉자  |  검사현황  |  자가격리
        table = soup.find('div', class_='detail').find_all('strong')
            
        self.db['확진자'] += int(table[0].text.replace(",",""))
        self.db['접촉자'] += int(table[1].text.replace(",",""))
        self.db['검사중'] += int(table[2].text.replace(",",""))
        self.db['자가격리자'] += int(table[3].text.replace(",",""))

        print(u"# 인천 동구 : %d"%(int(table[0].text.replace(",",""))))

    def ic_yeonsu_gu(self):
        res = requests.get('http://www.yeonsu.go.kr/covid-19/', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자(완치자포함)   |  완치자  |  접촉자  |  검사중  |  자가격리
        table = soup.find('div', class_='detail').find_all('strong')
            
        self.db['확진자'] += int(table[0].text.replace(",",""))
        self.db['완치자'] += int(table[1].text.replace(",",""))
        self.db['접촉자'] += int(table[2].text.replace(",",""))
        self.db['검사중'] += int(table[3].text.replace(",",""))
        self.db['자가격리자'] += int(table[4].text.replace(",",""))

        print(u"# 인천 연수구 : %d"%(int(table[0].text.replace(",",""))))

    def ic_namdong_gu(self):
        res = requests.get('https://www.namdong.go.kr/covid-19/', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자(완치자 제외)   |  완치자  |  검사중  |  자가격리
        confirm = soup.find('dl', class_='confirmator').find_all('span')
        recover = soup.find('dl', class_='recover').find('span')
        inspection = soup.find('dl', class_='inspection').find('span')
        quarantine = soup.find('dl', class_='quarantine').find('span')

        self.db['확진자'] += int(confirm[1].text.replace(",",""))
        self.db['완치자'] += int(recover.text.replace(",",""))
        self.db['검사중'] += int(inspection.text.replace(",",""))
        self.db['자가격리자'] += int(quarantine.text.replace(",",""))

        print(u"# 인천 남동구 : %d"%(int(confirm[1].text.replace(",",""))))

    def ic_bupyeong_gu(self):
        res = requests.get('http://www.icbp.go.kr/covid-19/', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자(완치제외)   |  완치자  |  검사완료(음성)  |  자가격리
        table = soup.find('div', class_='detail').find_all('strong')
                
        self.db['확진자'] += int(table[0].text.replace(",",""))
        self.db['접촉자'] += int(table[1].text.replace(",",""))
        self.db['검사완료'] += int(table[2].text.replace(",",""))
        self.db['자가격리자'] += int(table[3].text.replace(",",""))

        print(u"# 인천 부평구 : %d"%(int(table[0].text.replace(",",""))))


    def ic_gyeyang_gu(self):
        res = requests.get('http://www.gyeyang.go.kr/covid-19/', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자(완치제외)   |  자가격리  |  검사중
        table = soup.find('div', class_='detail').find_all('dd')
                
        self.db['확진자'] += int(table[0].text[:-8].replace("명",""))
        self.db['자가격리자'] += int(table[1].text.replace("명",""))
        self.db['검사중'] += int(table[2].text.replace("명",""))

        print(u"# 인천 계양구 : %d"%(int(table[0].text[:-8].replace("명",""))))

    def ic_seo_gu(self):
        res = requests.get('http://www.seo.incheon.kr/covid-19/', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 국내확진  |  해외유입  |  완치  |  자가격리  |  검사중
        confirm = soup.find('div', class_='detail').find_all('td')
        cure = soup.find('dl', class_='cure').find('dd')
        quarantine = soup.find('dl', class_='quarantine').find('dd')
        inspection = soup.find('dl', class_='inspection').find('dd')
                
        self.db['확진자'] += (int(confirm[0].text) + int(confirm[1].text))
        self.db['완치자'] += int(cure.text)
        self.db['자가격리자'] += int(quarantine.text)
        self.db['검사중'] += int(inspection.text)


        print(u"# 인천 서구 : %d"%(int(confirm[0].text) + int(confirm[1].text)))

    def ic_ganghwa_goon(self):
        res = requests.get('http://www.ganghwa.go.kr/open_content/main/#', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진
        confirm = soup.find('span', class_='wfont')
        self.db['확진자'] += int(confirm.text.replace("명","").replace("확진환자",""))
        print(u"# 인천 강화군 : %d"%(int(confirm.text.replace("명","").replace("확진환자",""))))

    def ic_ongjin_goon(self):
        res = requests.get('http://www.ongjin.go.kr/open_content/main/community/board/covid19.jsp', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진  |  검사  |  자가격리자
        confirm = soup.find('dl', class_='confirmator').find('strong')
        inspection = soup.find('dl', class_='contact').find('strong')
        quarantine = soup.find('dl', class_='quarantine').find('strong')
        self.db['확진자'] += int(confirm.text.replace("명",""))
        self.db['검사자'] += int(inspection.text.replace("명",""))
        self.db['자가격리자'] += int(quarantine.text.replace("명",""))

        print(u"# 인천 옹진군 : %d"%(int(confirm.text.replace("명",""))))

    def ic_michuhol_gu(self): # 미추홀구 사이트에서는 미추홀구 자체 데이터를 제공하지 않는 것으로 보임
        a = 2


    def collect(self):
        res = requests.get('https://www.incheon.go.kr/health/HE020409')
        soup = BeautifulSoup(res.content, 'html.parser')

        table_init = soup.find_all('tbody')[1] # 확진자, 검사중, 결과음성
        table = ' '.join(table_init.text.replace("\n", " ").split()).split(' ')

      
        self.db = {
            '지역'          :  0,
            '확진자'        :  0,
            '격리자'        :  0,
            '사망'        :  0,
            '의심환자'      :  0,
            '검사중'        :  0,
            '결과음성'      :  0,
            '자가격리자'    :  0,
            '감시중'        :  0,
            '감시해제'      :  0,
            '퇴원'          :  0,
            }


        self.ic_jung_gu
        self.ic_dong_gu
        self.ic_yeonsu_gu
        self.ic_namdong_gu
        self.ic_bupyeong_gu
        self.ic_gyeyang_gu
        self.ic_seo_gu
        self.ic_ganghwa_goon
        self.ic_ongjin_goon

        stat = copy.copy(form)

        
        stat['지역'] = '인천'
        stat['확진자'] = format(self.db['확진자'], ',')
        stat['격리자'] = format(self.db['확진자'], ',')
        stat['결과음성'] = table[5]
        stat['검사중'] = format(int(table[3].replace(',', '')) + int(table[4].replace(',', '')), ',')
        stat['의심환자'] = format(int(stat['검사중'].replace(',', '')) + int(stat['결과음성'].replace(',', '')), ',')    
        # stat['사망'] = li[2].text.split(' ')[1]
        #stat['퇴원'] = format(int(stat['퇴원'].replace(',','')) - 1, ',')
        #stat['격리자'] = format(int(stat['확진자'].replace(",", "")) - int(stat['퇴원'].replace(",", "")), ",")
    
        print("pass : ", stat['지역'])
        
        return stat
