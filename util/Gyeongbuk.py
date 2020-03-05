import requests, copy
from bs4 import BeautifulSoup
from selenium import webdriver
from util.form import form
import platform, re

dir_name = "util"

class Gyeongbuk():
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
            '사망'        :  0,
            '의사환자'      :  0,
            '검사중'        :  0,
            '결과음성'      :  0,
            '자가격리자'    :  0,
            '감시중'        :  0,
            '감시해제'      :  0,
            '완치'          :  0,
            }
    
    def gyeongsan(self):
        res = requests.get('http://gbgs.go.kr/programs/corona/corona.do', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table = soup.find('div', class_='gbgs_wrap').find_all("span")
        #table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        # 확진자  |  완치(확진해제자)  |  자가격리  
        
        self.db['확진자'] += int(table[0].text.replace(',', ''))
        self.db['격리자'] += int(table[1].text.replace(',', ''))
        self.db['사망'] += int(table[2].text.replace(',', ''))
        self.db['자가격리'] += int(table[3].text.replace(',', ''))
        self.db['의사환자'] += int(table[5].text.replace(',', ''))
        self.db['검사중'] += int(table[7].text.replace(',', ''))
        self.db['결과음성'] += int(table[8].text.replace(',', ''))
        self.db['감시중'] += int(table[10].text.replace(',', ''))
        self.db['감시해제'] += int(table[11].text.replace(',', ''))


    def cheongdo(self):
        res = requests.get('http://www.cheongdo.go.kr/', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table = soup.find('tbody').find_all("td")
        #table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        # 확진자  |  완치(확진해제자)  |  자가격리  
        self.db['확진자'] += int(table[0].text.replace(',', ''))
        self.db['사망'] += int(table[4].text.replace(',', ''))
        self.db['격리자'] += int(table[0].text.replace(',', '')) - int(table[4].text.replace(',', '')) 


    def chilgok(self):
        res = requests.get('http://www.chilgok.go.kr/covid19/', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table = soup.find_all('em')#.find_all("td")
        #table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        # 확진자  |  완치(확진해제자)  |  자가격리  
        self.db['확진자'] += int(table[0].text.replace(',', ''))
        self.db['자가격리자'] += int(table[2].text.replace(',', ''))
        self.db['검사중'] += int(table[3].text.replace(',', ''))
       
    
    def seongju(self):
        res = requests.get('http://www.sj.go.kr/design/corona.jsp?design#', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table = soup.find('tbody').find_all("td")
        # 총계 | 격리  |  완치(확진해제자)  |  사망  |  자가격리  |  해제  
        self.db['확진자'] += int(table[0].text.replace(',', ''))
        self.db['격리자'] += int(table[1].text.replace(',', ''))
        self.db['완치'] += int(table[2].text.replace(',', ''))
        self.db['사망'] += int(table[3].text.replace(',', ''))
        self.db['자가격리자'] += int(table[4].text.replace(',', ''))

    def yeongcheon(self):
        res = requests.get('https://www.yc.go.kr/', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table = soup.find('ul').find_all("p", class_='')
        # 확진자 | 추가확진자  |  검사중  |  자가격리  |  사망  |  비고(퇴원)  
        self.db['확진자'] += int(table[0].text.replace(',', ''))
        self.db['검사중'] += int(table[2].text.replace(',', ''))
        self.db['자가격리자'] += int(table[3].text.replace(',', ''))
        self.db['사망'] += int(table[4].text.replace(',', ''))
        self.db['완치'] += int(table[5].text[2:-1].replace(',', ''))
        

    def gyeongju(self):
        res = requests.get('http://www.gyeongju.go.kr/open_content/ko/index.do', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table = soup.find('div', class_='status').find_all('li')
        #re.findall("\d+",table[0].text)[0]
        # 총계 | 격리  |  완치(확진해제자)  |  사망  |  자가격리  |  해제  
        self.db['확진자'] += int(re.findall("\d+",table[0].text)[0].replace(',', ''))
        self.db['격리자'] += int(re.findall("\d+",table[1].text)[0].replace(',', ''))
        self.db['완치'] += int(re.findall("\d+",table[2].text)[0].replace(',', ''))
        self.db['사망'] += int(re.findall("\d+",table[3].text)[0].replace(',', ''))
        self.db['의사환자'] += int(re.findall("\d+",table[4].text)[0].replace(',', ''))
        self.db['검사중'] += int(re.findall("\d+",table[5].text)[0].replace(',', ''))
        self.db['결과음성'] += int(re.findall("\d+",table[6].text)[0].replace(',', ''))
        self.db['자가격리자'] += int(re.findall("\d+",table[9].text)[0].replace(',', ''))
        
    def pohang(self):
        driver = copy.copy(self.driver)
        driver.get('http://www.pohang.go.kr/COVID-19.html')
        driver.implicitly_wait(2)
        table_init = driver.find_elements_by_class_name('status_list')[0].text
        table = ' '.join(table_init.replace("\n"," ").split()).split(' ') 
        
        # ['26', '확진자(합계)', '0', '사망', '0', '완치', '635', '검사완료', '406', '자가격리']
        self.db['확진자'] += int(table[0])
        self.db['완치'] += int(table[4])
        self.db['사망'] += int(table[2])
        self.db['결과음성'] += int(table[6]) - int(table[0])
        self.db['자가격리자'] += int(table[8])

    def uiseong(self):
        res = requests.get('https://www.usc.go.kr/tabBoard/detail.tc?mn=2510&viewType=sub&mngNo=423&pageIndex=1&boardName=CORONASLKD1&boardNo=3029311&pageSeq=1700&preview=&previewTempl=&previewTempl=&tabBoardSeq=51&type=&tabOrder=&searchCondition=0&searchKeyword=', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table = soup.find('tbody').find_all('tr')[10].find_all('td')
        # table[4] = 검사결과 음성
        # 매일 확인할 것  
        self.db['확진자'] += int(table[3].text)
        self.db['검사중'] += int(table[2].text)
        self.db['결과음성'] += int(table[4].text)
    
    def gumi(self):
        res = requests.get('http://www.gumi.go.kr/', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table = soup.find('div', class_='box_group').find_all('p', class_='counter')

        self.db['확진자'] += int(table[0].text)
        self.db['격리자'] += int(table[1].text)
        self.db['사망'] += int(table[2].text)
        self.db['검사중'] += int(table[4].text)
        self.db['결과음성'] += int(table[5].text)
        self.db['자가격리자'] += int(table[6].text)
        self.db['감시중'] += int(table[7].text)
        self.db['감시해제'] += int(table[8].text)

    def collect(self, suspect='-', testing='-', negative='-'):
        # 1. reqeusts 라이브러리를 활용한 HTML 페이지 요청 
        #res = requests.get('http://www.daegu.go.kr/')
        # 2) HTML 페이지 파싱 BeautifulSoup(HTML데이터, 파싱방법)
        #soup = BeautifulSoup(res.content, 'html.parser')
        # 3) 필요한 데이터 검색
        #li = soup.find('div', class_='con_r').find_all('li')
     
        self.gyeongsan()
        self.cheongdo()
        self.chilgok()
        self.seongju()
        self.yeongcheon()
        self.gyeongju()
        self.pohang()
        self.uiseong()
        self.gumi()

        stat = copy.copy(form)
        
        stat['지역'] = '경상북도'
        stat['확진자'] = format(self.db['확진자'], ',')
        stat['사망'] = format(self.db['사망'], ',')
        stat['검사중'] = '%s'%(testing) # format(self.db['검사중'], ',')
        stat['결과음성'] = '%s'%(negative) # format(self.db['결과음성'], ',')
        stat['의사환자'] = '%s'%(suspect) # format(self.db['의사환자'], ',')
        stat['자가격리자'] = format(self.db['자가격리자'], ',')
        stat['격리자'] = format(self.db['확진자'] - int(stat['사망']), ",")
    
        print("pass : ", stat['지역'])
        
        return stat