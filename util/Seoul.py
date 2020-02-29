import requests, copy
from bs4 import BeautifulSoup
from selenium import webdriver
from util.form import form
import platform

dir_name = "util"

class Seoul():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        f_driver = ''
        if platform.system() == 'Linux':
            f_driver = '%s/chromedriver'%(dir_name)
        elif platform.system() == 'Darwin':
            f_driver = '%s/chromedriver_darwin'%(dir_name)
        else:
            f_driver = '%s/chromedriver.exe'%(dir_name)
        self.driver = webdriver.Chrome(f_driver, chrome_options=options)

        self.db = {
            '지역'          :  0,
            '확진자'        :  0,
            '격리자'        :  0,
            '사망자'        :  0,
            '의사환자'      :  0,
            '검사중'        :  0,
            '결과음성'      :  0,
            '자가격리자'    :  0,
            '감시중'        :  0,
            '감시해제'      :  0,
            '완치'          :  0,
            }
    
    def yeongdeungpo_gu(self):
        driver = copy.copy(self.driver)
        driver.get('https://www.ydp.go.kr/site/corona/index.html')
        driver.implicitly_wait(2)
        table_init = driver.find_element_by_tag_name('tbody')
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ') 
        self.db['확진자'] += int(table[0][:-1]) # 확진자
        self.db['자가격리자'] += int(table[1][:-1]) # 자가격리자
        self.db['감시중'] += int(table[2][:-1]) # 능동감시자
    
    def yongsan_gu(self):
        res = requests.get('http://www.yongsan.go.kr/site/kr/index.jsp')
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table_init = soup.find('tbody')
        # 확진자  |  완치자  |  격리 |  자가격리/능동감시(자가격리자)
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ') 

        self.db['확진자'] += int(table[0][:-1]) # 확진자
        self.db['자가격리자'] += int(table[1][:-1]) # 확진자
    
    def eunpyeong_gu(self):
        res = requests.get('https://www.ep.go.kr/CmsWeb/viewPage.req?idx=PG0000004918')
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table_init = soup.find('tbody')
        # 확진자  |  완치자  |  격리 |  자가격리/능동감시(자가격리자)
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ') 

        self.db['확진자'] += int(table[1][:-1]) # 확진자
        #self.db['추가확진자'] += int(table[0][:-1]) # 
        #self.db['완치'] += 
        #self.db['자가격리자'] += 
        
    def jongno_gu(self):
        res = requests.get('http://www.jongno.go.kr/portalMain.do;jsessionid=edgF6qdhxN6YfuSesu3MBWaoxB1zxK13M4zajh2nSIWcitqm4UVSX7ITFaNU1Rdb.was_servlet_engine1')
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table_init = soup.find('tbody')
        # 확진자  |  완치자  |  격리 |  자가격리/능동감시(자가격리자)
        table = ' '.join(table.text.replace("\n"," ").split()).split(' ') 

        self.db['확진자'] += int(table[0][:-1]) # 확진자
        self.db['격리자'] += int(table[1][:-1]) # 입원
        self.db['완치'] += int(table[2][:-1]) # 퇴원
        self.db['자가격리자'] += int(table[3][:-1]) # 자가격리자
        
    def jung_gu(self):
        res = requests.get('http://www.junggu.seoul.kr/index.jsp')
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table_init = soup.find('tbody')#, class_='point_txt')#.find_all('span')
        #li = table.find_all('td')[1:11]
        
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        self.db['확진자'] += int(table[0])
        self.db['자가격리자'] += int(table[1])
        self.db['감시자'] += int(table[2])    
    
    def jungnang_gu(self):
        res = requests.get('https://www.jungnang.go.kr/portal/main.do')
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table = soup.find('span', class_='point_txt')
        # 전국  |  북구  |  자가격리
        self.db['확진자'] += int(table.text) # 북구 확진자
        # self.db['자가격리자'] += int(    ) # 북구 자가격리자

        
    def collect(self):
        # 1. reqeusts 라이브러리를 활용한 HTML 페이지 요청 
        res = requests.get('http://www.daegu.go.kr/')
        # 2) HTML 페이지 파싱 BeautifulSoup(HTML데이터, 파싱방법)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 3) 필요한 데이터 검색
        li = soup.find('div', class_='con_r').find_all('li')
     
        self.buk_gu()
        
        self.yeongdeungpo()
        self.yongsan_gu()
        self.eunpyeong_gu()
        self.jongno_gu()
        self.jung_gu()
        self.jungnang_gu()
    
        stat = copy.copy(form)
        
        stat['지역'] = '서울'
        stat['확진자'] = format(self.db['확진자'], ',')
        stat['사망자'] = li[2].text.split(' ')[1]
        stat['격리자'] = format(self.db['확진자'] - int(stat['사망자'].replace(',','')), ",")
        stat['자가격리자'] = self.db['자가격리자']
    
        print("pass : ", stat['지역'])
        
        return stat