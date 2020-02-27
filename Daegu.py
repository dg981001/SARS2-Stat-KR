import requests, copy
from bs4 import BeautifulSoup
from selenium import webdriver
from form import form

class Daegu():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)

        self.db = {
                    '확진자' : 0,
                    '자가격리자' : 0
                    }
        
    def bukgu(self):
        bukgu = requests.get('http://www.buk.daegu.kr/#')
        bukgu_data = BeautifulSoup(bukgu.content, 'html.parser')
        table = bukgu_data.find('tbody').find_all('td')
        # 전국  |  북구  |  자가격리
        self.db['확진자'] += int(table[1].text[:-1].replace(',', '')) # 북구 확진자
        self.db['자가격리자'] += int(table[2].text[:-1].replace(',', '')) # 북구 자가격리자

    def namgu(self):
        namgu = requests.get('http://www.nam.daegu.kr/')
        namgu_data = BeautifulSoup(namgu.content, 'html.parser')
        table = namgu_data.find('tbody').find_all('td')
        # 전국  |  남구  |  자가격리
        self.db['확진자'] += int(table[1].text[:-1].replace(',', '')) # 남구 확진자
        self.db['자가격리자'] += int(table[2].text[:-1].replace(',', '')) # 남구 자가격리자


    def dalseogu(self):
        driver = copy.copy(self.driver)
        driver.get('http://www.dalseo.daegu.kr/')
        driver.implicitly_wait(5)
        #print(driver.page_source)
        table = driver.find_element_by_tag_name('tbody').text.split(" ")
        # 전국  |  대구시  |  달서구  |  자가격리
        self.db['확진자'] += int(table[2][:-1].replace(',', '')) # 달서구 확진자
        self.db['자가격리자'] += int(table[3][:-1].replace(',', '')) # 달서구 자가격리자


    def seogu(self):
        seogu = requests.get('https://www.dgs.go.kr/inc/popup.php?pop_open_site=seogu_k&pop_idx=36')
        seogu_data = BeautifulSoup(seogu.content, 'html.parser')
        table = seogu_data.find('tbody').find_all('td')
        # 전국  |  대구시  |  서구  |  자가격리
        self.db['확진자'] += int(table[2].text[:-1].replace(',', '')) # 서구 확진자
        self.db['자가격리자'] += int(table[3].text[:-1].replace(',', '')) # 서구 자가격리자

    def suseonggu(self):
        suseonggu = requests.get('http://www.suseong.kr/index.do')
        suseonggu_data = BeautifulSoup(suseonggu.content, 'html.parser')
        table = suseonggu_data.find('tbody').find_all('td')
        # 전국  |  수성구  |  자가격리
        self.db['확진자'] += int(table[1].text[:-1].replace(',', '')) # 수성구 확진자
        self.db['자가격리자'] += int(table[2].text[:-1].replace(',', '')) # 수성구 자가격리자

    def junggu(self):
        junggu = requests.get('http://www.jung.daegu.kr/new/pages/main/')
        junggu_data = BeautifulSoup(junggu.content, 'html.parser')
        table = junggu_data.find('tbody').find_all('td')
        # 전국  |  대구시  |  중구  |  자가격리
        self.db['확진자'] += int(table[2].text[:-1].replace(',', '')) # 중구 확진자
        self.db['자가격리자'] += int(table[3].text[:-1].replace(',', '')) # 중구 자가격리자

    def donggu(self):
        donggu = requests.get('http://www.dong.daegu.kr/main/main.htm')
        donggu_data = BeautifulSoup(donggu.content, 'html.parser')
        table = donggu_data.find('ul', class_='cB').find_all("span", class_="t2")
        #  동구  |  자가격리
        self.db['확진자'] += int(table[0].text[:-1].replace(',', '')) # 동구 확진자
        self.db['자가격리자'] += int(table[1].text[:-1].replace(',', '')) # 동구 자가격리자

    def dalseonggun(self):
        driver = copy.copy(self.driver)
        driver.get('http://dalseong.daegu.kr/')
        driver.implicitly_wait(5)
        table = driver.find_element_by_tag_name('tbody').text.split(" ")
        # 누계  |  확진환자  |  자가격리  |  능동감시  | 감시종료
        self.db['확진자'] += int(table[1][:-1].replace(',', '')) # 달성군 확진자
        self.db['자가격리자'] += int(table[2][:-1].replace(',', '')) # 달성군 자가격리자
        
    def collect(self):
        # 1. reqeusts 라이브러리를 활용한 HTML 페이지 요청 
        res = requests.get('http://www.daegu.go.kr/')
        # 2) HTML 페이지 파싱 BeautifulSoup(HTML데이터, 파싱방법)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 3) 필요한 데이터 검색
        li = soup.find('div', class_='con_r').find_all('li')
     
        self.bukgu()
        self.dalseogu()
        self.namgu()
        self.seogu()
        self.suseonggu()
        self.junggu()
        self.donggu()
        self.dalseonggun()
    
        stat = copy.copy(form)
        
        stat['지역'] = '대구'
        stat['확진자'] = format(self.db['확진자'], ',')
        stat['사망자'] = li[3].text.split(' ')[1]
        stat['격리자'] = format(self.db['확진자'] - int(stat['사망자'].replace(',','')) - int(li[1].text.split(' ')[1].replace(',','')), ",") 
        stat['자가격리자'] = format(self.db['자가격리자'], ',')
        stat['완치'] = li[1].text.split(' ')[1]
    
        print("pass : ", stat['지역'])
        
        return stat