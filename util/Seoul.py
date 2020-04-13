import requests, copy
from bs4 import BeautifulSoup
#from selenium import webdriver
from util.form import form
import platform, json, re
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

    def gangnam_gu(self):
        res = requests.get('http://www.gangnam.go.kr/index.htm', headers=headers)
        data = BeautifulSoup(res.content, 'html.parser')
        table = data.find_all('script')
        
        confirmed = int(table[4].text.split('"counter8", ')[1].split(')')[0].replace(',',''))
        self.db['확진자'] += confirmed
        #self.db['확진자'] += int(table[0].text.replace(",","")) # 강남 확진자
        # 자가격리  |  능동감시
        #self.db['자가격리자'] += int(table[1].text.replace(",","")) # 강남 자가격리자
        #self.db['감시중'] += int(table[2].text.replace(",","")) # 강남 능동감시자
        
        print(u"# 강남구 : %d"%(confirmed))

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
        self.db['퇴원'] += int(table[2].text.replace(',','')) # 강북 능동감시자

        print(u"# 강북구 : %d"%(int(table[0].text.replace(',',''))))

    def gangseo_gu(self):
        res = requests.get('http://www.gangseo.seoul.kr/new_portal/index.jsp', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  능동감시자
        table = soup.find('table', 'table0226').find_all('tr')[1].find_all('td')
        self.db['확진자'] += int(table[0].text.replace(",","")) # 강서 확진자
        self.db['감시중'] += int(table[1].text.replace(",","")) # 강서 능동감시자
        # TODO: 퇴원자 추가하기
        print(u"# 강서구 : %d"%(int(table[0].text)))

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
        res = requests.get('https://www.gwangjin.go.kr/index1.html', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 위기경보단계  |  확진환자  |  자가격리&능동감시자
        # 자가격리자와 능동감시자와 별개로 분류되어 있지 않으므로 자가격리자로 취급
        table = soup.find('div', 'grey-box').find_all('strong')
        self.db['확진자'] += int(table[1].text.replace(",",""))
        self.db['자가격리자'] += int(table[2].text.replace(",",""))

        print(u"# 광진구 : %d"%(int(table[1].text.replace(",",""))))

    def guro_gu(self):
        res = requests.get('http://www.guro.go.kr/corona2.jsp', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 구분  |  확진자  |  자가격리자  |  능동감시자
        table = soup.find('table', class_='table_A').find('tbody').find_all('td')
         # 확진자 수 뒤에 붙어있는 '강조' 텍스트 제거

        self.db['확진자'] += int(table[0].text.replace(",",""))
        self.db['격리자'] += int(table[1].text.replace(",",""))
        self.db['퇴원'] += int(table[2].text.replace(",",""))
        self.db['자가격리자'] += int(table[3].text.replace(",",""))
        self.db['감시중'] += int(table[4].text.replace(",",""))

        print(u"# 구로구 : %d"%(int(int(table[0].text.replace(",","")))))

    def geumcheon_gu(self):
        res = requests.get('https://www.geumcheon.go.kr/', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 구분  |  확진자  |  능동감시자(자가격리자)
        value1 = soup.find('li', class_='pink_line clearfix')
        table = re.findall('(.*?)명', value1.text)

        confirmed = int(table[0].replace(',', ''))
        quarantined = int(table[1].replace(',', ''))
        cared = int(table[2].replace(',', ''))

        self.db['확진자'] += confirmed
        # 능동감시자와 자가격리자가 N명(M명) 의 형태로 표기되어 있어 별도로 분리
        #self.db['감시중'] += int(value2[0].replace(' ', ''))
        #self.db['자가격리자'] += int(value2[1].replace('(','').replace(' ', ''))

        print(u"# 금천구 : %d"%(confirmed))

    def nowon_gu(self):
        res = requests.get('http://www.nowon.kr', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  의심환자  |  유증상자  |  자가격리자
        # 유증상자는 별도로 집계하지 않음
        table = soup.find('tbody').find_all('td')

        self.db['확진자'] += int(table[0].text[:-1].replace(' ', ''))
        self.db['퇴원'] += int(table[1].text[:-1].replace(' ', ''))
        self.db['격리자'] += int(table[3].text[:-1].replace(' ', ''))
        self.db['의심환자'] += int(table[2].text[:-1].replace(' ', ''))
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
        res = requests.get('http://www.ddm.go.kr/', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  검사중  |  결과음성
        table = soup.find('tbody').find_all('strong')
        self.db['확진자'] += int(table[0].text.replace(' ', ''))
        self.db['감시중'] += int(table[1].text.replace(' ', ''))
        self.db['감시해제'] += int(table[2].text.replace(' ', ''))

        print(u"# 동대문구 : %d"%(int(table[0].text.replace(' ', ''))))

    def dongjak_gu(self):
        res = requests.get('https://www.dongjak.go.kr/')#, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  능동감시자
        temp = soup.find('tbody')
        table = re.findall('td>(.*?) 명</td>',str(temp))

        self.db['확진자'] += int(table[0].replace(',', ''))
        self.db['자가격리자'] += int(table[1].replace(',', ''))
        self.db['퇴원'] += int(table[2].replace(',', ''))

        print(u"# 동작구 : %d"%(int(table[0].replace(' ', ''))))

    def mapo_gu(self):
        res = requests.get('http://www.mapo.go.kr/html/corona/intro.htm')#, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  자가격리자  |  능동감시자
        table = soup.find('tbody').find_all('tr')[1].find_all('td')
        quarantined = int(table[0].text.replace(' ', ''))
        cared = int(table[1].text.replace(' ', ''))
        confirmed = quarantined + cared
        self.db['확진자'] += confirmed
        #self.db['자가격리자'] += int(table[1].text.replace(' ', ''))
        #self.db['감시중'] += int(table[2].text.replace(' ', ''))

        print(u"# 마포구 : %d"%(confirmed))

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

        treatment = int(table[0].text[:-1].replace(',',''))
        cured = int(table[1].text[:-1].replace(',',''))

        self.db['확진자'] += treatment + cured
        self.db['퇴원'] += cured

        print(u"# 서초구 : %d"%(treatment + cured))

    def seongdong_gu(self):
        res = requests.get('http://www.sd.go.kr/sd/intro.do', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        temp = soup.find('ul', class_='status_list')
        table = re.findall('<em>(.*?)명</em>',str(temp))

        # 확진자  |  의심환자  |  능동감시자  |  자가격리자  |  유증상자
        # 유증상자는 별도로 집계 안함
        quarantined = int(table[0].replace(',',''))
        cared = int(table[1].replace(',',''))
        confirmed = quarantined + cared
        self.db['확진자'] += confirmed
        #self.db['의심환자'] += int(table[1].text[:-1].replace(',',''))
        self.db['퇴원'] += cared
        #self.db['자가격리자'] += int(table[3].text[:-1].replace(',',''))

        print(u"# 성동구 : %d"%(confirmed))

    # 성북구는 텍스트로 된 자료를 제공하지 않아 크롤링 불가
    def seongbuk_gu(self):
        res = requests.get('http://www.sb.go.kr/')
        soup = BeautifulSoup(res.content, 'html.parser')
        # 퇴원  |  격리자  |  자가격리 능동감시자
        table = soup.find_all('span', class_='num')

        self.db['퇴원'] += int(table[0].text.replace(',', ''))
        self.db['격리자'] += int(table[1].text.replace(',', ''))
        confirmed = int(table[0].text.replace(',', '')) + int(table[1].text.replace(',', ''))
        self.db['확진자'] += confirmed
        #self.db['자가격리자'] += # int(table[2].text.replace(',', ''))
        print(u"# 성북구 : %d"%(confirmed))

    def songpa_gu(self):
        res = requests.get('http://www.songpa.go.kr/index.jsp', verify=True, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        init = soup.find('tbody')
        table = re.findall('\n(.*?)명', init.text)
        confirmed = int(table[0].replace(',', ''))
        quarantined = int(table[1].replace(',', ''))
        cared = int(table[2].replace(',', ''))
        # 확진자  |  퇴원(확진해제자)  |  자가격리  
        
        self.db['확진자'] += confirmed
        self.db['퇴원'] += cared
        #self.db['자가격리자'] += int(table[8][:-1].replace(',', ''))
        #self.db['결과음성'] += 
        #self.db['검사중'] += 
        print(u"# 송파구 : %d"%(confirmed))

    def yangcheon_gu(self):
        res = requests.get('http://www.yangcheon.go.kr/site/yangcheon/coronaStatusList.do') #, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        confirmed = int(soup.find('tbody').find_all('td')[1].text.split('명')[0].replace(',', ''))
        ## 전국  |  양천구  
        
        self.db['확진자'] += confirmed
        #self.db['결과음성'] += 
        #self.db['검사중'] += 
        #self.db['자가격리자'] += 
        print(u"# 양천구 : %d"%(confirmed))

    def yeongdeungpo_gu(self):
        res = requests.post('https://www.ydp.go.kr/selectDissInfoJSON.do', verify=False, headers=headers)
        table = json.loads(res.content)['dissInfo']

        quarantined = int(table['cnt1'])
        cared = int(table['cnt4'])
        confirmed = quarantined + cared
        self.db['확진자'] += confirmed
        self.db['격리자'] += quarantined # 확진자
        self.db['자가격리자'] += int(table['cnt2']) # 자가격리자
        self.db['퇴원'] += cared # 능동감시자

        print(u"# 영등포구 : %d"%(confirmed))
    
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
        res = requests.get('https://www.ep.go.kr/CmsWeb/viewPage.req?idx=PG0000004918')#, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table = soup.find_all('tbody')[1].find_all('td')

        confirmed = int(table[0].text.split('명')[0].replace(',',''))
        self.db['확진자'] += confirmed  # 확진자
        #self.db['추가확진자'] += int(table[0][:-1]) # 
        #self.db['퇴원'] += 
        #self.db['자가격리자'] += int(table[2].text[:-1].replace(',',''))
        
        print(u"# 은평구 : %d"%(confirmed))
        
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
        #li = table.find_all('td')[1:11]
        #
        #table = ' '.join(table_init.text.replace("\n"," ").split()).split(' ')
        self.db['확진자'] += 5 #int(table[0])
        self.db['자가격리자'] += 265 # int(table[1])
        self.db['감시중'] +=  0 # int(table[2])

        print(u"# 중구 : %d"%(5))
    
    def jungnang_gu(self):
        res = requests.get('https://www.jungnang.go.kr/intro.jsp', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table = soup.find('dl', class_='intro_tbl jn_intro_tbl').find_all('span')
        # 전국  |  북구  |  자가격리
        self.db['확진자'] += int(table[0].text.replace(',', ''))
        self.db['퇴원'] += int(table[1].text.replace(',', ''))
        self.db['감시중'] += int(table[2].text.replace(',', ''))
        self.db['감시해제'] += int(table[3].text.replace(',', ''))
        # self.db['자가격리자'] += int(    ) # 

        print(u"# 중랑구 : %d"%(int(table[0].text.replace(',', ''))))
        
    def collect(self):
        res = requests.get('http://www.seoul.go.kr/coronaV/coronaStatus.do?menu_code=01', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')

        li_num = soup.find_all('p', class_='counter')
        li_txt = soup.find_all('p', class_='txt')

        li_txt = [txt.text for txt in li_txt]
        li_num = [num.text for num in li_num]

        others = int(soup.find('span', class_='district district26').find('span', class_='num').text.replace(',', ''))

        stat = copy.copy(form)
        for i in range(0, len(li_txt)-4):
            stat[li_txt[i]] = li_num[i]

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

        self.db['확진자'] += others # 기타

        print("# 기타 : %d"%(others))
        
        stat['지역'] = '서울'
        stat['확진자'] = format(self.db['확진자'], ',')
        # stat['사망'] = li[2].text.split(' ')[1]
        stat['퇴원'] = format(int(stat['퇴원'].replace(',','')) - 1, ',')
        stat['격리자'] = format(int(stat['확진자'].replace(",", "")) - int(stat['퇴원'].replace(",", "")), ",")
    
        print("pass : ", stat['지역'])
        
        return stat