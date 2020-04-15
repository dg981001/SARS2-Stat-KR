import requests, copy, re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from util.from import form

dir_name = "util"
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
headers = {'User-Agent': user_agent}

class Busan():
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

    def Haeundae_gu(self):
        with urlopen('http://www.haeundae.go.kr/index.do') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.select('div.corona19'):
                for anchor1 in anchor.select('table.type11'):
                    confirmed = int(anchor1.get_text().split('\n')[7].split('명')[0])

        self.db['확진자'] += confirmed
        # self.db['자가 격리자'] +=
        print(u"#  해운대구 : ", confirmed)

    def Suyeong_gu(self):
        with urlopen('http://www.suyeong.go.kr/index.suyeong?contentsSid=2180') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.select('table.tbl'):
                for anchor1 in anchor.select('tbody'):
                    confirmed = int(anchor1.get_text().split('\n')[2].split('명')[0])


        self.db['확진자'] += confirmed
        print(u"# 수영구 : ", confirmed)

    def Saha_gu(self):
        a = []
        with urlopen('https://www.saha.go.kr/corona.do') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.select('div.el'):
                for anchor1 in anchor.select('tbody'):
                    a.append(int(anchor1.get_text().split('\n')[2].split('명')[0]))
        confirmed = a[0]
        
        self.db['확진자'] += confirmed
        print(u"# 사하구 : ", confirmed)

    def Yeonje_gu(self):

        with urlopen('https://www.yeonje.go.kr/index2.jsp') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.select('ul.corona_li'):
                confirmed = anchor.get_text().split('\n')[3].split('명')[0]
        
        self.db['확진자'] += confirmed
        print(u"# 연제구 : ", confirmed)

    def Nam_gu(self):

        response = requests.get('https://www.bsnamgu.go.kr/index.namgu', verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        for anchor in soup.select('div.corona'):
            confirmed = int(anchor.get_text().split('\n')[5].split('명')[0])

        self.db['확진자'] += confirmed
        print(u"# 남구 : ", confirmed)

     
    def Seo_gu(self):

        with urlopen('http://www.bsseogu.go.kr/index.bsseogu?contentsSid=2560') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.select('div.cov_con'):
                for anchor1 in anchor.select('td.red'):
                    confirmed = int(anchor1.get_text().split('\n')[0].split('명')[0])

        self.db['확진자'] += confirmed
        print(u"# 서구 : ", confirmed)

    def Jung_gu(self):

        a = []
        with urlopen('http://www.bsjunggu.go.kr/index.junggu') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.select('div.tableBox'):
                for anchor1 in anchor.select('tr'):
                    a.append(anchor1.get_text().split('\n'))
        confirmed = int(a[1][2].split('명')[0])
        inspecting = int(a[1][3].split('명')[0])
        self_quarantined = int(a[1][4].split('명')[0])

        self.db['확진자'] += confirmed
        self.db['검사중'] += inspecting
        self.db['자가격리자'] += self_quarantined

        print(u"# 중구 : ", confirmed)

    def Buk_gu(self):

        a=[]
        with urlopen('https://www.bsbukgu.go.kr/index.bsbukgu?contentsSid=2317') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.select('table.co_state'):
                for anchor1 in anchor.select('td'):
                    a.append(anchor1.get_text().split('\n'))
                    
        confirmed = int(a[0][0].split('명')[0])
        cured = int(a[2][0].split('명')[0])

        self.db['확진자'] += confirmed
        self.db['퇴원'] += cured

        print(u"# 북구 : ", confirmed)

    def Dong_gu(self):

        a=[]
        with urlopen('http://www.bsdonggu.go.kr/index.donggu?contentsSid=1433') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.select('table.tbl'):
                for anchor1 in anchor.select('td'):
                    a.append(anchor1.get_text().split('\n'))
                    
        local_confirmed = a[0][1].split('\r')[0]
        foreign_confirmed = a[1][1].split('\r')[0]
        inspecting = a[2][1].split('\r')[0]
        negative_result = a[3][1].split('\r')[0]

        self.db['확진자'] = local_confirmed + foreign_confirmed
        self.db['검사중'] = inspecting
        self.db['결과음성'] = negative_result

        print(u"# 동구 : ", confirmed)

    # def Gijang_gu(self):
    # http://www.gijang.go.kr/index.gijang?contentsSid=1494
    #이미지 파일로 업로드하여 파싱 불가능

    # def Dongnae_gu(self):

    # 동래구청 http://www.dongnae.go.kr/index.dongnae?contentsSid=2136
    # html 주석처리  <!-- --> 읽어와야됨

    # 진구청, 영도구청, 강서구청, 금정구청, 사상구청 : 구청 사이트에 자료가 없음

     
    def collect(self):

        a=[]
        with urlopen('http://www.busan.go.kr/corona19/index') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.select('span'):
                a.append(anchor.get_text().split('\n'))
        confirmed = a[1][0].split('명')[0]
        add_confirmed = a[2][0].split('명')[0]
        cured = a[3][0].split('명')[0]
        curing = a[4][0].split('명')[0]
        death = a[5][0].split('명')[0]
        
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

        self.Haeundae_gu()
        self.Buk_gu()
        self.Jung_gu()
        self.Nam_gu()
        self.Saha_gu()
        self.Seo_gu()
        self.Suyeong_gu()
        self.Yeonje_gu()


        stat = copy.copy(form)
        
        stat['지역'] = '부산'
        stat['확진자'] = format(self.db['확진자'], ',')
        stat['사망'] = death
        stat['퇴원'] = cured
        stat['격리자'] = format(self.db['확진자'] - int(stat['사망'].replace(',','')) - int(stat['퇴원'].replace(',','')), ",") 
        stat['자가격리자'] = format(self.db['자가격리자'], ',')
        

        print("pass : ", stat['지역'])
        
        return stat




    