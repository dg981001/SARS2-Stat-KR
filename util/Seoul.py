import requests, copy
from bs4 import BeautifulSoup
from selenium import webdriver
from util.form import form
import platform
import urllib3
from time import sleep

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

    def gangnam_gu(self):
        res = requests.get('http://www.gangnam.go.kr/index.htm')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 계  |  강남주민  |  타지역
        self.db['확진자'] += int(soup.find('table', 'corona_table1').find('tbody') \
                            .find('span').text) # 강남 확진자
        # 자가격리  |  능동감시
        self.db['자가격리자'] += int(soup.find('table', 'corona_table2').find('tbody') \
                               .find_all('span')[0].text) # 강남 자가격리자
        self.db['감시중'] += int(soup.find('table', 'corona_table2').find('tbody') \
                               .find_all('span')[1].text) # 강남 능동감시자

    def gangdong_gu(self):
        res = requests.get('https://www.gangdong.go.kr')
        soup = BeautifulSoup(res.content, 'html.parser')
        self.db['확진자'] += int(soup.find('li', 'red').find('strong').text) # 강동 확진자
        self.db['완치'] += int(soup.find('li', 'green').find('strong').text) # 강동 완치자
        self.db['자가격리자'] += int(soup.find('li', 'blue').find('strong').text) # 강동 자가격리자

    def gangbuk_gu(self):
        driver = copy.copy(self.driver)
        driver.get('http://www.gangbuk.go.kr/www/index.do')
        # 확진자  |  자가격리자  |  능동감시자
        table = driver.find_element_by_class_name('table_co') \
            .find_element_by_class_name('text_center').text.split(' ')
        self.db['확진자'] += int(table[0]) # 강북 확진자
        self.db['자가격리자'] += int(table[1]) # 강북 자가격리자
        self.db['감시중'] += int(table[2]) # 강북 능동감시자

    def gangseo_gu(self):
        res = requests.get('http://www.gangseo.seoul.kr/new_portal/index.jsp')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  능동감시자
        table = soup.find('table', 'table0226').find_all('tr')[1].find_all('td')
        self.db['확진자'] += int(table[0].text[:-1]) # 강서 확진자
        self.db['감시중'] += int(table[1].text[:-1]) # 강서 능동감시자
        # TODO: 완치자 추가하기

    def gwanak_gu(self):
        res = requests.get('http://www.gwanak.go.kr/site/gwanak/main.do')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  자가격리자  |  능동감시자
        table = soup.find('div', 'corona_con').find_all('strong')
        self.db['확진자'] += int(table[0].text[:-1])
        self.db['자가격리자'] += int(table[1].text[:-1])
        self.db['감시중'] += int(table[2].text[:-1])

    def gwangjin_gu(self):
        res = requests.get('https://www.gwangjin.go.kr/portal/main/main.do')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 위기경보단계  |  확진환자  |  자가격리&능동감시자
        # 자가격리자와 능동감시자와 별개로 분류되어 있지 않으므로 자가격리자로 취급
        table = soup.find('ul', 'cpo_line').find_all('span')
        self.db['확진자'] += int(table[1].text)
        self.db['자가격리자'] += int(table[2].text)

    def guro_gu(self):
        res = requests.get('http://www.guro.go.kr/www/NR_index.do')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 구분  |  확진자  |  자가격리자  |  능동감시자
        table = soup.find('table', 'table').find('tbody').find('tr').find_all('td')
        table[1].find('span').extract() # 확진자 수 뒤에 붙어있는 '강조' 텍스트 제거
        self.db['확진자'] += int(table[1].text)
        self.db['자가격리자'] += int(table[2].text)
        self.db['감시중'] += int(table[3].text)

    def geumcheon_gu(self):
        res = requests.get('https://www.geumcheon.go.kr/portal/index.do')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 구분  |  확진자  |  능동감시자(자가격리자)
        table = soup.find('div', 'corona_popup').find('div', 'table_box division3') \
                .find_all('span', 'text')
        self.db['확진자'] += int(table[1].text[:-1])
        # 능동감시자와 자가격리자가 N명(M명) 의 형태로 표기되어 있어 별도로 분리
        self.db['감시중'] += int(table[2].text.split('명')[0])
        self.db['자가격리자'] += int(table[2].text.split('명')[1].split('(')[1])

    def nowon_gu(self):
        res = requests.get('http://www.nowon.kr')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  의사환자  |  유증상자  |  자가격리자
        # 유증상자는 별도로 집계하지 않음
        table = soup.find('div', 'covid_pop').find('div', 'co_bd').find('table').find('tbody') \
                .find_all('td')
        self.db['확진자'] += int(table[0].text.replace(' ', '')[:-1])
        self.db['의사환자'] += int(table[1].text.replace(' ', '')[:-1])
        self.db['자가격리자'] += int(table[3].text.replace(' ', '')[:-1])

    def dobong_gu(self):
        res = requests.get('http://www.dobong.go.kr')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  자가격리자  |  능동감시자
        table = soup.find('div', id='corona_pop').find('div', 'body').find('div', 'bottom') \
                .find('table').find('tbody').find_all('em')
        self.db['확진자'] += int(table[0].text)
        self.db['자가격리자'] += int(table[2].text)
        self.db['감시중'] += int(table[4].text)

    def dongdaemun_gu(self):
        res = requests.get('http://www.ddm.go.kr/life/presentCondition.jsp')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  검사중  |  결과음성
        table = soup.find('table', 'data5 indent2 center').find('tbody').find_all('td')
        self.db['확진자'] += int(table[0].text[:-1])
        self.db['검사중'] += int(table[1].text[:-1])
        self.db['결과음성'] += int(table[2].text[:-1])

    def dongjak_gu(self):
        res = requests.get('http://www.dongjak.go.kr')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  자가격리자  |  능동감시자
        table = soup.find('ul', 'status-ul').find_all('p', 'sta-data')
        self.db['확진자'] += int(table[0].text[:-1])
        self.db['자가격리자'] += int(table[1].text[:-1])
        self.db['감시중'] += int(table[2].text[:-1])

    def mapo_gu(self):
        res = requests.get('https://www.mapo.go.kr/site/main/home')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  자가격리자  |  능동감시자
        table = soup.find('table', 'status-table3').find('tbody').find_all('td')
        self.db['확진자'] += int(table[0].text.split('명')[0])
        self.db['자가격리자'] += int(table[1].text[:-1])
        self.db['감시중'] += int(table[2].text[:-1])

    def seodaemun_gu(self):
        res = requests.get('http://www.sdm.go.kr/index.do')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  완치자  |  자가격리자
        table = soup.find('div', 'coPan').find_all('div')[1].find_all('p')
        self.db['확진자'] += int(table[0].text[:-1])
        self.db['완치'] += int(table[1].text[:-1])
        self.db['자가격리자'] += int(table[2].text[:-1])

    def seocho_gu(self):
        res = requests.get('http://www.seocho.go.kr/site/seocho/main.do')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  능동감시자
        table = soup.find('div', id='virusPopup').find('table').find('tbody').find_all('td')
        self.db['확진자'] += int(table[0].text[:-1])
        self.db['감시중'] += int(table[1].text[:-1])

    def seongdong_gu(self):
        url = 'http://www.sd.go.kr/sd/main.do'
        # 디코딩에 실패하는 경우가 있어 최대 10번까지 시도
        tries = 0
        max_tries = 10
        while True:
            try:
                tries += 1
                print('Try {0} for Seongdong-gu'.format(tries))
                res = urllib3.PoolManager().request('GET', url)
                soup = BeautifulSoup(res.data.decode('cp949'), 'html.parser')
                break
            except:
                if tries < max_tries:
                    sleep(2) # 2초 대기 후 재시도
                else:
                    print('All tries for Seongdong-gu failed.')
                    raise

        # 확진자  |  의사환자  |  능동감시자  |  자가격리자  |  유증상자
        # 유증상자는 별도로 집계 안함
        table = soup.find('ul', 'pop_status margin_l_28').find_all('span', 'status_txt')
        self.db['확진자'] += int(table[0].text[:-1])
        self.db['의사환자'] += int(table[1].text[:-1])
        self.db['감시중'] += int(table[2].text[:-1])
        self.db['자가격리자'] += int(table[3].text[:-1])

    # 성북구는 텍스트로 된 자료를 제공하지 않아 크롤링 불가
    #def seongbuk_gu(self):

    def songpa_gu(self):
        res = requests.get('http://www.songpa.go.kr/index.jsp', verify=True)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table_init = soup.find('tbody')
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        # 확진자  |  완치(확진해제자)  |  자가격리  
        
        self.db['확진자'] += int(table[3][:-1].replace(',', ''))
        self.db['완치'] += int(table[4][:-1].replace(',', ''))
        self.db['자가격리자'] += int(table[5][:-1].replace(',', ''))
        #self.db['결과음성'] += 
        #self.db['검사중'] += 

    def yangcheon_gu(self):
        res = requests.get('http://www.yangcheon.go.kr/site/yangcheon/main.do', verify=False)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table_init = soup.find('tbody')
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        ## 전국  |  양천구  
        
        self.db['확진자'] += int(table[1][:-1].replace(',', ''))
        #self.db['결과음성'] += 
        #self.db['검사중'] += 
        #self.db['자가격리자'] += 

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
    
        # 확진자  |  완치자  |  격리  |  자가격리/능동감시(자가격리자)
        table = soup.find('div', 'coronal-table').find('tbody').find_all('td')

        self.db['확진자'] += int(table[0].text[:-1]) # 확진자
        self.db['완치'] += int(table[1].text[:-1]) # 완치자
        self.db['격리자'] += int(table[2].text[:-1]) # 치료중
        self.db['자가격리자'] += int(table[3].text[:-1]) # 자가격리자
        
    def jung_gu(self):
        res = requests.get('http://www.junggu.seoul.kr/index.jsp')
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table_init = soup.find('tbody')#, class_='point_txt')#.find_all('span')
        #li = table.find_all('td')[1:11]
        
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        self.db['확진자'] += int(table[0])
        self.db['자가격리자'] += int(table[1])
        self.db['감시중'] += int(table[2])
    
    def jungnang_gu(self):
        res = requests.get('https://www.jungnang.go.kr/portal/main.do')
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table = soup.find('span', class_='point_txt')
        # 전국  |  북구  |  자가격리
        self.db['확진자'] += int(table.text) # 
        # self.db['자가격리자'] += int(    ) # 
        
    def collect(self):
        # 1. reqeusts 라이브러리를 활용한 HTML 페이지 요청 
        #res = requests.get('http://www.daegu.go.kr/')
        # 2) HTML 페이지 파싱 BeautifulSoup(HTML데이터, 파싱방법)
        #soup = BeautifulSoup(res.content, 'html.parser')
        # 3) 필요한 데이터 검색
        #li = soup.find('div', class_='con_r').find_all('li')

        self.gangnam_gu()
        self.gangdong_gu()
        self.gangbuk_gu()
        self.gangseo_gu()
        self.gwanak_gu()
        self.gwangjin_gu()
        self.guro_gu()
        self.geumcheon_gu()
        self.nowon_gu()
        self.dobong_gu()
        self.dongdaemun_gu()
        self.dongjak_gu()
        self.mapo_gu()
        self.seodaemun_gu()
        self.seocho_gu()
        self.seongdong_gu()
        #self.seongbuk_gu()
        self.songpa_gu()
        self.yangcheon_gu()
        self.yeongdeungpo_gu()
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