import requests, copy
from bs4 import BeautifulSoup
from selenium import webdriver
from util.form import form
import platform

dir_name = "util"

class Gangwon():
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
    
    def wonju(self):
        res = requests.get('https://www.wonju.go.kr/intro.jsp', verify=False)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table = soup.find('div', class_='conbox').find_all('p', class_='text')
        # 확진자  |  자가격리자  |  검사현황 |  검사중 |  결과음성
        
        self.db['확진자'] += int(table[0].text.replace(',', '')) 
        self.db['자가격리자'] += int(table[1].text.replace(',', ''))
        self.db['검사중'] += int(table[3].text.replace(',', ''))
        self.db['결과음성'] += int(table[4].text.replace(',', ''))
        print("# 원주 : %d"%(int(table[0].text.replace(',', '')) ))


    def chuncheon(self):
        res = requests.get('https://www.chuncheon.go.kr/index.chuncheon?menuCd=DOM_000000599001000000', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table = soup.find('ul', class_='cc_st_list').find_all("div", class_="cc_st_sub")#.find_all('p', class_='text')
        # 확진자  |  의심환자  |  검사중 |  결과음성  |  접촉자  |  자가격리자  |  파악중  
        
        self.db['확진자'] += int(table[0].text.replace(',', ''))
        self.db['의사환자'] += int(table[1].text.replace(',', ''))  #<
        self.db['검사중'] += int(table[2].text.replace(',', ''))
        self.db['결과음성'] += int(table[3].text.replace(',', ''))
        self.db['자가격리자'] += int(table[5].text.replace(',', ''))
        print("# 춘천 : %d"%(int(table[0].text.replace(',', '')) ))


    def gangneung(self):
        res = requests.get('https://www.gn.go.kr/www/contents.do?key=3158', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table = soup.find('div', class_='cont2').find("ul").find_all('span')
        # 확진자  |  결과음성  |  검사중  |  총계
        
        self.db['확진자'] += int(table[0].text[:-1].replace(',', ''))
        #self.db['의사환자'] += 
        self.db['결과음성'] += int(table[1].text[:-1].replace(',', ''))
        self.db['검사중'] += int(table[2].text[:-1].replace(',', ''))
        #self.db['자가격리자'] += 
        print("# 강릉 : %d"%(int(table[0].text[:-1].replace(',', '')) ))
    
    def sokcho(self):
        res = requests.get('http://www.sokcho.go.kr/portal', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        confirmed = soup.find_all('div', class_='tb_c_tit')[0].find('span', class_='point').text
        quarantine = soup.find('div', class_='tb_sub').find('span', class_='tb_c_r').text[:-1]
        suspected = soup.find_all('div', class_='tb_c_tit')[1].find("span").text
        table = soup.find('div', class_='tb_sub').find_all('span', class_='tb_c_r')
        # 확진자 | ~ 명
        # 의사환자  |  검사중/결과음성/결과양성
        # 조사대상 유증상자 | 검사중/결과음성/결과양성
        
        self.db['확진자'] += int(confirmed.replace(',', ''))
        self.db['의사환자'] += int(suspected.replace(',', ''))
        self.db['자가격리자'] += int(suspected.replace(',', '')) # 의사환자(자가격리자) 로 표기되어 있음
        self.db['결과음성'] += int(table[1].text[:-1].replace(',', '')) + int(table[4].text[:-1].replace(',', ''))
        self.db['검사중'] += int(table[0].text[:-1].replace(',', '')) + int(table[3].text[:-1].replace(',', ''))

        print("# 속초 : %d"%(int(confirmed.replace(',', '')) ))

    def samcheok(self):
        res = requests.get('http://www.samcheok.go.kr/02179/02696.web', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table_init = soup.find('tbody')
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        # 확진자  |  결과음성  |  검사중  |  자가격리  |  격리해제
        
        self.db['확진자'] += int(table[0][:-1].replace(',', ''))
        self.db['결과음성'] += int(table[1][:-1].replace(',', ''))
        self.db['검사중'] += int(table[2][:-1].replace(',', ''))
        self.db['자가격리자'] += int(table[3][:-1].replace(',', ''))

        print("# 삼척 : %d"%(int(table[0][:-1].replace(',', '')) ))
        
        
    def collect(self, suspect='-', testing='-', negative='-'):
        # 1. reqeusts 라이브러리를 활용한 HTML 페이지 요청 
        #res = requests.get('http://www.daegu.go.kr/')
        # 2) HTML 페이지 파싱 BeautifulSoup(HTML데이터, 파싱방법)
        #soup = BeautifulSoup(res.content, 'html.parser')
        # 3) 필요한 데이터 검색
        #li = soup.find('div', class_='con_r').find_all('li')
     
        self.wonju()
        self.chuncheon()
        self.gangneung()
        self.sokcho()
        self.samcheok()

        stat = copy.copy(form)
        
        stat['지역'] = '강원도'
        stat['확진자'] = format(self.db['확진자'], ',')
        stat['사망'] = format(self.db['사망'], ',')
        stat['검사중'] = '%s'%(testing) # format(self.db['검사중'], ',')
        stat['결과음성'] = '%s'%(negative) # format(self.db['결과음성'], ',')
        stat['의사환자'] = '%s'%(suspect) # format(self.db['의사환자'], ',')
        stat['자가격리자'] = format(self.db['자가격리자'], ',')
        stat['격리자'] = format(self.db['확진자'] - int(stat['사망']), ",")
    
        print("pass : ", stat['지역'])
        
        return stat