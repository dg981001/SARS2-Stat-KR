import requests, copy, re
from bs4 import BeautifulSoup
#from selenium import webdriver
from util.form import form

dir_name = "util"
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
headers = {'User-Agent': user_agent}

class Daegu():
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

    def buk_gu(self):
        bukgu = requests.get('https://www.buk.daegu.kr/index.do', verify=False)
        bukgu_data = BeautifulSoup(bukgu.content, 'html.parser')
        table = bukgu_data.find('tbody').find_all('td')
        # 전국  |  북구  |  자가격리
        confirmed = int(table[1].text.split("(")[0].split()[0][:-1].replace(',', ''))
        self_quarantined = int(table[2].text.split("(")[0].split()[0][:-1].replace(',', ''))
        #print(int(table[1].text[:-1].replace(',', '')))
        self.db['확진자'] += confirmed # 북구 확진자
        self.db['자가격리자'] += self_quarantined # 북구 자가격리자
        print(u"#  북구 : ", confirmed)

    def nam_gu(self):
        namgu = requests.get('http://nam.daegu.kr/index.do#')
        namgu_data = BeautifulSoup(namgu.content, 'html.parser')
        table = namgu_data.find('tbody').find_all('td')
        # 전국  |  남구  |  자가격리
        confirmed = int(table[0].text.split('(')[0].replace(',', ''))

        self.db['확진자'] += confirmed # 남구 확진자
        # self.db['자가격리자'] += int(table[2].text[:-1].replace(',', '')) # 남구 자가격리자
        print(u"#  남구 : ", confirmed)

    def dalseo_gu(self):
        res = requests.get('https://www.dalseo.daegu.kr/icms/popup/getLayerPopup.do?popup_id=POPUP_00000000000021')
        temp = BeautifulSoup(res.content, 'html.parser')
        cookie = temp.find("script").text.split("\r\n")[1].replace("document.cookie = '", '').replace("'", "")
        headers = {'Cookie' : cookie}
        res = requests.get('https://www.dalseo.daegu.kr/icms/popup/getLayerPopup.do?popup_id=POPUP_00000000000021', headers=headers)
        table = BeautifulSoup(res.content, 'html.parser').find('tbody').find_all('td')
        # 전국  |  대구시  |  달서구  |  자가격리
        #print(int(table[2][:-1].replace(',', '')))
        confirmed = int(table[2].text.replace('\t', '').replace('\r', '').replace('\n', '').split('명')[0].replace(',', ''))
        self_quarantined = int(table[3].text.replace('\t', '').replace('\r', '').replace('\n', '').split('명')[0].replace(',', ''))
        self.db['확진자'] += confirmed # 달서구 확진자
        self.db['자가격리자'] += self_quarantined # 달서구 자가격리자
        print(u"#  달서구 : ", confirmed)

    def seo_gu(self):
        seogu = requests.get('https://www.dgs.go.kr/inc/popup.php?pop_open_site=seogu_k&pop_idx=36')
        seogu_data = BeautifulSoup(seogu.content, 'html.parser')
        table = seogu_data.find('tbody').find_all('td')
        # 전국  |  대구시  |  서구  |  자가격리
        #print(int(table[2].text[:-1].replace(',', '')))
        self.db['확진자'] += int(table[2].text[:-1].replace(',', '')) # 서구 확진자
        self.db['자가격리자'] += int(table[3].text[:-1].replace(',', '')) # 서구 자가격리자
        print(u"#  서구 : ", int(table[2].text[:-1].replace(',', '')))

    def suseong_gu(self):
        suseonggu = requests.get('http://www.suseong.kr/index.do')
        suseonggu_data = BeautifulSoup(suseonggu.content, 'html.parser')
        table = suseonggu_data.find('tbody').find_all('tr')[1].find_all('td')
        # 전국  |  수성구  |  자가격리
        #print(int(table[1].text[:-1].replace(',', '')))
        # cared = int(table[0].text.replace(',','').split('명')[0])
        repositive = int(table[2].text.replace(',','').split('명')[0])
        #quarantine = int(table[3].text.replace(',','').split('명')[0])
        #death = int(table[2].text.replace(',','').split('명')[0])
        self_qurantine = int(table[3].text.replace(',','').split('명')[0])

        confirmed = int(table[0].text.replace(',','').split('명')[0])

        self.db['확진자'] += confirmed # 수성구 확진자
        self.db['자가격리자'] += self_qurantine # 수성구 자가격리자
        #self.db['재확진자'] += repositive
        print(u"#  수성구 : ", confirmed)

    def jung_gu(self):
        junggu = requests.get('http://www.jung.daegu.kr/new/pages/main/')
        junggu_data = BeautifulSoup(junggu.content, 'html.parser')
        temp = junggu_data.find('ul', class_='count')
        table = re.findall('<dd>(.*?)<span>명', str(temp))
        # 전국  |  대구시  |  중구  |  자가격리
        confirmed = int(table[0].replace(',', ''))
        cured = int(table[1].replace(',', ''))
        quarantined = int(table[2].replace(',', ''))
        self_quarnatined = int(table[3].replace(',', ''))
        self.db['확진자'] += confirmed # 중구 확진자
        self.db['자가격리자'] += self_quarnatined # 중구 자가격리자
        print(u"#  중구 : ", confirmed)


    def dong_gu(self):
        res = requests.get('http://www.dong.daegu.kr/main/main.htm', headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 확진자  |  능동감시자
        temp = soup.find('div', class_='covid_box').find('ul', class_='cB')
        table = re.findall('<p class="txt02">(.*?)</p>',str(temp))
        #  동구  |  자가격리
        #print(int(table[0].text[:-1].replace(',', '')))
        confirmed = int(table[0].replace(',', ''))
        cared = int(table[1].replace(',', ''))
        self_quarantined = int(table[2].replace(',', ''))
        quarantined = int(table[3].replace(',', ''))
        self.db['확진자'] += int(confirmed) # 동구 확진자
        self.db['자가격리자'] += int(self_quarantined) # 동구 자가격리자
        print(u"#  동구 : ", int(confirmed))

    def dalseonggun(self):
        res = requests.get('http://dalseong.daegu.kr/icms/popup/getLayerPopup.do?popup_id=POPUP_00000000000051')
        dalseonggun_data = BeautifulSoup(res.content, 'html.parser')
        table = dalseonggun_data.find_all('tbody')[1].find_all('td')
        # 누계  |  확진환자  |  자가격리  |  능동감시  | 감시종료
        #print(int(table[1][:-1].replace(',', '')))
        self.db['확진자'] += int(table[0].text.split("(")[0].replace(',', '')) # 달성군 확진자
        # self.db['자가격리자'] += int(table[2].text.split("(")[0].replace(',', '')) # 달성군 자가격리자
        print(u"#  달성군 : ", int(table[0].text.split("(")[0].replace(',', '')))


    def collect(self):
        # 1. reqeusts 라이브러리를 활용한 HTML 페이지 요청 
        res = requests.get('http://www.daegu.go.kr/dgcontent/index.do')
        # 2) HTML 페이지 파싱 BeautifulSoup(HTML데이터, 파싱방법)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 3) 필요한 데이터 검색
        li = soup.find('div', class_='conunt_box').find_all('strong')
     
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

        self.buk_gu()
        self.dalseo_gu()
        self.nam_gu()
        self.seo_gu()
        self.suseong_gu()
        self.jung_gu()
        self.dong_gu()
        self.dalseonggun()
    
        stat = copy.copy(form)
        
        stat['지역'] = '대구'
        stat['확진자'] = format(self.db['확진자'], ',')
        stat['사망'] = li[3].text[:-1]
        stat['퇴원'] = li[1].text[:-1]
        stat['격리자'] = format(self.db['확진자'] - int(stat['사망'].replace(',','')) - int(stat['퇴원'].replace(',','')), ",") 
        stat['자가격리자'] = format(self.db['자가격리자'], ',')
        
    
        print("pass : ", stat['지역'])
        
        return stat