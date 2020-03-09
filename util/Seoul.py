import requests, copy
from bs4 import BeautifulSoup
from selenium import webdriver
from util.form import form
import platform, json
from time import sleep

dir_name = "util"

user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
headers = {'User-Agent': user_agent}

class Seoul():
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
        self.db = dict()

    def gangnam_gu(self):
        res = requests.get('http://www.gangnam.go.kr/index.htm', headers=headers)
        data = BeautifulSoup(res.content, 'html.parser')
        table = data.find('div', class_='sBox').find_all('strong')
        # 계  |  강남주민  |  타지역
        self.db['확진자'] += int(table[0].text.replace(",","")) # 강남 확진자
        # 자가격리  |  능동감시
        self.db['자가격리자'] += int(table[1].text.replace(",","")) # 강남 자가격리자
        self.db['감시중'] += int(table[2].text.replace(",","")) # 강남 능동감시자
        
        print(u"# 강남구 : %d"%(int(table[0].text.replace(",",""))))

    def gangdong_gu(self):
        res = requests.get('https://www.gangdong.go.kr', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        self.db['확진자'] += int(soup.find('li', 'red').find('strong').text.replace(",","")) # 강동 확진자
        self.db['퇴원'] += int(soup.find('li', 'green').find('strong').text.replace(",","")) # 강동 퇴원자
        self.db['자가격리자'] += int(soup.find('li', 'blue').find('strong').text.replace(",","")) # 강동 자가격리자

        print(u"# 강동구 : %d"%(int(soup.find('li', 'red').find('strong').text)))

    def gangbuk_gu(self):
        res = requests.get('http://www.gangbuk.go.kr/intro_gb.jsp')
        temp = BeautifulSoup(res.content, 'html.parser')
        cookie = temp.find("script").text.split("\r\n")[1].replace("document.cookie = '", '').replace("'", "")
        headers = {'Cookie' : cookie}
        res = requests.get('http://www.gangbuk.go.kr/intro_gb.jsp', headers=headers)
        table = BeautifulSoup(res.content, 'html.parser').find('ul', class_='clearfix').find_all('p', class_='text')

        self.db['확진자'] += int(table[0].text.replace(',','')) # 강북 확진자
        self.db['자가격리자'] += int(table[1].text.replace(',','')) # 강북 자가격리자
        self.db['퇴원'] += int(table[3].text.replace(',','')) # 강북 능동감시자

        print(u"# 강북구 : %d"%(int(table[0].text.replace(',',''))))

    def gangseo_gu(self):
        res = requests.get('http://www.gangseo.seoul.kr/new_portal/index.jsp', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  능동감시자
        table = soup.find('table', 'table0226').find_all('tr')[1].find_all('td')
        self.db['확진자'] += int(table[0].text[:-1].replace(",","")) # 강서 확진자
        self.db['감시중'] += int(table[1].text[:-1].replace(",","")) # 강서 능동감시자
        # TODO: 퇴원자 추가하기
        print(u"# 강서구 : %d"%(int(table[0].text[:-1])))

    def gwanak_gu(self):
        res = requests.get('http://www.gwanak.go.kr/site/gwanak/main.do', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  자가격리자  |  능동감시자
        table1 = soup.find('div', 'corona_con').find_all('td')
        table2 = soup.find('div', 'corona_con').find_all('strong')
        
        self.db['확진자'] += int(table1[0].text[:-1].replace(",",""))
        self.db['격리자'] += int(table1[1].text[:-1].replace(",",""))
        self.db['퇴원'] += int(table1[2].text[:-1].replace(",",""))
        self.db['자가격리자'] += int(table2[0].text[:-1].replace(",",""))
        self.db['감시중'] += int(table2[1].text[:-1].replace(",",""))

        print(u"# 관악구 : %d"%(int(table1[0].text[:-1].replace(",",""))))

    def gwangjin_gu(self):
        res = requests.get('https://www.gwangjin.go.kr/portal/main/main.do', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 위기경보단계  |  확진환자  |  자가격리&능동감시자
        # 자가격리자와 능동감시자와 별개로 분류되어 있지 않으므로 자가격리자로 취급
        table = soup.find('ul', 'cpo_line').find_all('span')
        self.db['확진자'] += int(table[1].text.replace(",",""))
        self.db['자가격리자'] += int(table[2].text.replace(",",""))

        print(u"# 광진구 : %d"%(int(table[1].text.replace(",",""))))

    def guro_gu(self):
        res = requests.get('http://www.guro.go.kr/corona2.jsp', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 구분  |  확진자  |  자가격리자  |  능동감시자
        table = soup.find('tbody').find_all('td')
         # 확진자 수 뒤에 붙어있는 '강조' 텍스트 제거
        table[1].find('span').extract()

        self.db['확진자'] += int(table[1].text.replace(",",""))
        self.db['자가격리자'] += int(table[2].text.replace(",",""))
        self.db['감시중'] += int(table[3].text.replace(",",""))

        print(u"# 구로구 : %d"%(int(table[1].text.replace(",",""))))

    def geumcheon_gu(self):
        res = requests.get('https://www.geumcheon.go.kr/', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 구분  |  확진자  |  능동감시자(자가격리자)
        value1 = soup.find('li', class_='pink_line').find('span', class_='text2').text.split()[0][:-1].replace(',','')
        value2 = soup.find('li', class_='pink_line').find('span', class_='text2_2').text.split('명')

        self.db['확진자'] += int(value1)
        # 능동감시자와 자가격리자가 N명(M명) 의 형태로 표기되어 있어 별도로 분리
        self.db['감시중'] += int(value2[0].replace(' ', ''))
        self.db['자가격리자'] += int(value2[1].replace('(','').replace(' ', ''))

        print(u"# 금천구 : %d"%(int(value1)))

    def nowon_gu(self):
        res = requests.get('http://www.nowon.kr', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  의사환자  |  유증상자  |  자가격리자
        # 유증상자는 별도로 집계하지 않음
        table = soup.find('tbody').find_all('td')

        self.db['확진자'] += int(table[0].text[:-1].replace(' ', ''))
        self.db['퇴원'] += int(table[1].text[:-1].replace(' ', ''))
        self.db['격리자'] += int(table[3].text[:-1].replace(' ', ''))
        self.db['의사환자'] += int(table[2].text[:-1].replace(' ', ''))
        self.db['감시중'] += int(table[4].text[:-1].replace(' ', ''))
        self.db['자가격리자'] += int(table[4].text[:-1].replace(' ', ''))

        print(u"# 노원구 : %d"%(int(table[0].text[:-1].replace(' ', ''))))

    def dobong_gu(self):
        res = requests.get('http://www.dobong.go.kr/', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  자가격리자  |  능동감시자
        table = soup.find_all('em', class_='num')
        self.db['확진자'] += int(table[0].text.replace(' ', ''))
        self.db['자가격리자'] += int(table[1].text.replace(' ', ''))
        self.db['감시중'] += int(table[2].text.replace(' ', ''))

        print(u"# 도봉구 : %d"%(int(table[0].text.replace(' ', ''))))

    def dongdaemun_gu(self):
        res = requests.get('http://www.ddm.go.kr/life/presentCondition.jsp', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  검사중  |  결과음성
        table = soup.find('table', 'data5 indent2 center').find('tbody').find_all('td')
        self.db['확진자'] += int(table[0].text[:-1].replace(' ', ''))
        self.db['검사중'] += int(table[1].text[:-1].replace(' ', ''))
        self.db['결과음성'] += int(table[2].text[:-1].replace(' ', ''))

        print(u"# 동대문구 : %d"%(int(table[0].text[:-1].replace(' ', ''))))

    def dongjak_gu(self):
        res = requests.get('http://www.dongjak.go.kr', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  자가격리자  |  능동감시자
        table = soup.find('ul', 'status-ul').find_all('p', 'sta-data')
        self.db['확진자'] += int(table[0].text[:-1].replace(' ', ''))
        self.db['자가격리자'] += int(table[1].text[:-1].replace(' ', ''))
        self.db['감시중'] += int(table[2].text[:-1].replace(' ', ''))

        print(u"# 동작구 : %d"%(int(table[0].text[:-1].replace(' ', ''))))

    def mapo_gu(self):
        res = requests.get('http://www.mapo.go.kr/html/corona/intro.htm')#, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  자가격리자  |  능동감시자
        table = soup.find('div', class_='is-cont').find('ul').find_all('span')
        self.db['확진자'] += int(table[0].text.replace(' ', ''))
        self.db['자가격리자'] += int(table[1].text.replace(' ', ''))
        self.db['감시중'] += int(table[2].text.replace(' ', ''))

        print(u"# 마포구 : %d"%(int(table[0].text.replace(' ', ''))))

    def seodaemun_gu(self):
        res = requests.get('http://www.sdm.go.kr/index.do', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  퇴원자  |  자가격리자
        table = soup.find('ul', class_='corona-popup-number-box').find_all('span') 
        self.db['확진자'] += int(table[0].text.replace(' ', ''))
        self.db['퇴원'] += int(table[1].text.replace(' ', ''))
        self.db['자가격리자'] += int(table[2].text.replace(' ', ''))

        print(u"# 서대문구 : %d"%(int(table[0].text.replace(' ', ''))))

    def seocho_gu(self):
        res = requests.get('http://www.seocho.go.kr/site/seocho/main.do', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  능동감시자
        table = soup.find('div', id='virusPopup').find('table').find('tbody').find_all('td')
        self.db['확진자'] += int(table[0].text[:-1].replace(',',''))
        self.db['감시중'] += int(table[1].text[:-1].replace(',',''))

        print(u"# 서초구 : %d"%(int(int(table[0].text[:-1].replace(',','')))))

    def seongdong_gu(self):
        res = requests.get('http://www.sd.go.kr/sd/main.do', headers=headers)
        res.encoding='euc-kr'
        data = BeautifulSoup(res.text, 'html.parser')
        table = data.find('ul', class_='pop_status').find_all("span", class_='status_txt')
        # 디코딩에 실패하는 경우가 있어 최대 10번까지 시도

        # 확진자  |  의사환자  |  능동감시자  |  자가격리자  |  유증상자
        # 유증상자는 별도로 집계 안함
        self.db['확진자'] += int(table[0].text[:-1].replace(',',''))
        self.db['의사환자'] += int(table[1].text[:-1].replace(',',''))
        self.db['감시중'] += int(table[2].text[:-1].replace(',',''))
        self.db['자가격리자'] += int(table[3].text[:-1].replace(',',''))

        print(u"# 성동구 : %d"%(int(int(table[0].text[:-1].replace(',','')))))

    # 성북구는 텍스트로 된 자료를 제공하지 않아 크롤링 불가
    def seongbuk_gu(self):
        res = requests.get('http://www.sb.go.kr/')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 퇴원  |  격리자  |  자가격리 능동감시자
        table = soup.find_all('span', class_='num')

        self.db['퇴원'] += int(table[0].text.replace(',', ''))
        self.db['격리자'] += int(table[1].text.replace(',', ''))
        self.db['확진자'] += int(table[0].text.replace(',', '')) + int(table[1].text.replace(',', ''))
        #self.db['자가격리자'] += # int(table[2].text.replace(',', ''))
        print(u"# 성북구 : %d"%(int(table[0].text.replace(',', ''))))

    def songpa_gu(self):
        res = requests.get('http://www.songpa.go.kr/index.jsp', verify=True, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table_init = soup.find('tbody')
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        # 확진자  |  퇴원(확진해제자)  |  자가격리  
        
        self.db['확진자'] += int(table[3][:-1].replace(',', ''))
        self.db['퇴원'] += int(table[4][:-1].replace(',', ''))
        self.db['자가격리자'] += int(table[5][:-1].replace(',', ''))
        #self.db['결과음성'] += 
        #self.db['검사중'] += 
        print(u"# 송파구 : %d"%(int(table[3][:-1].replace(',', ''))))

    def yangcheon_gu(self):
        res = requests.get('http://www.yangcheon.go.kr/site/yangcheon/main.do', verify=False, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table_init = soup.find('tbody')
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        ## 전국  |  양천구  
        
        self.db['확진자'] += int(table[1][:-1].replace(',', ''))
        #self.db['결과음성'] += 
        #self.db['검사중'] += 
        #self.db['자가격리자'] += 
        print(u"# 양천구 : %d"%(int(table[1][:-1].replace(',', ''))))

    def yeongdeungpo_gu(self):
        res = requests.post('https://www.ydp.go.kr/selectDissInfoJSON.do', verify=False, headers=headers)
        table = json.loads(res.content)['dissInfo']

        self.db['확진자'] += int(table['cnt1']) # 확진자
        self.db['자가격리자'] += int(table['cnt2']) # 자가격리자
        self.db['감시중'] += int(table['cnt3']) # 능동감시자

        print(u"# 영등포구 : %d"%(int(table['cnt1'])))
    
    def yongsan_gu(self):
        res = requests.get('http://www.yongsan.go.kr/site/kr/index.jsp', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table_init = soup.find('tbody')
        # 확진자  |  퇴원자  |  격리 |  자가격리/능동감시(자가격리자)
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ') 

        self.db['확진자'] += int(table[0][:-1]) # 확진자
        self.db['자가격리자'] += int(table[1][:-1]) # 확진자

        print(u"# 용산구 : %d"%(int(table[0][:-1])))
    
    def eunpyeong_gu(self):
        res = requests.get('https://www.ep.go.kr/CmsWeb/viewPage.req?idx=PG0000004918', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table_init = soup.find_all('tbody')[1]
        # 확진자  |  퇴원자  |  격리 |  자가격리/능동감시(자가격리자)
        table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ') 

        self.db['확진자'] += int(table[1][:-1].replace(',','')) # 확진자
        #self.db['추가확진자'] += int(table[0][:-1]) # 
        #self.db['퇴원'] += 
        self.db['자가격리자'] += int(table[2][:-1].replace(',',''))
        
        print(u"# 은평구 : %d"%(int(table[1][:-1].replace(',',''))))
        
    def jongno_gu(self):
        res = requests.get('http://www.jongno.go.kr/portalMain.do;jsessionid=edgF6qdhxN6YfuSesu3MBWaoxB1zxK13M4zajh2nSIWcitqm4UVSX7ITFaNU1Rdb.was_servlet_engine1', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        # 확진자  |  퇴원자  |  격리  |  자가격리/능동감시(자가격리자)
        table = soup.find('div', 'coronal-table').find('tbody').find_all('td')

        self.db['확진자'] += int(table[0].text[:-1]) # 확진자
        self.db['퇴원'] += int(table[1].text[:-1]) # 퇴원자
        self.db['격리자'] += int(table[2].text[:-1]) # 치료중
        self.db['자가격리자'] += int(table[3].text[:-1]) # 자가격리자

        print(u"# 종로구 : %d"%(int(table[0].text[:-1])))
        
    def jung_gu(self):
        #res = requests.get('http://www.junggu.seoul.kr/', headers=headers)
        #soup = BeautifulSoup(res.content, 'html.parser')
        #
        #table_init = soup.find('tbody')#, class_='point_txt')#.find_all('span')
        ##li = table.find_all('td')[1:11]
        #
        #table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        self.db['확진자'] += 0     # int(table[0])
        self.db['자가격리자'] += 11 # int(table[1])
        self.db['감시중'] += 1      # int(table[2])

        print(u"# 중구 : %d"%(0))
    
    def jungnang_gu(self):
        res = requests.get('https://www.jungnang.go.kr/portal/main.do', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table = soup.find('span', class_='point_txt')
        # 전국  |  북구  |  자가격리
        self.db['확진자'] += int(table.text) # 
        # self.db['자가격리자'] += int(    ) # 

        print(u"# 중랑구 : %d"%(int(table.text)))
        
    def collect(self):
        res = requests.get('http://www.seoul.go.kr/coronaV/coronaStatus.do', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')

        li_num = soup.find_all('p', class_='counter')
        li_txt = soup.find_all('p', class_='txt')

        li_txt = [txt.text for txt in li_txt]
        li_num = [num.text for num in li_num]

        stat = copy.copy(form)
        for i in range(0, len(li_txt)-4):
            stat[li_txt[i]] = li_num[i]

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
            '퇴원'          :  0,
            }


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
        self.seongbuk_gu()
        self.songpa_gu()
        self.yangcheon_gu()
        self.yeongdeungpo_gu()
        self.yongsan_gu()
        self.eunpyeong_gu()
        self.jongno_gu()
        self.jung_gu()
        self.jungnang_gu()

        self.db['확진자'] += 13 # 기타

        print("# 기타 : %d"%(13))
        
        stat['지역'] = '서울'
        stat['확진자'] = format(self.db['확진자'], ',')
        # stat['사망'] = li[2].text.split(' ')[1]
        stat['퇴원'] = format(int(stat['퇴원'].replace(',','')) - 1, ',')
        stat['격리자'] = format(int(stat['확진자'].replace(",", "")) - int(stat['퇴원'].replace(",", "")), ",")
    
        print("pass : ", stat['지역'])
        
        return stat