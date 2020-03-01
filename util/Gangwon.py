class Gangwon():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        f_driver = ''
        if platform.system() == 'Linux':
            f_driver = './chromedriver'
        elif platform.system() == 'Darwin':
            f_driver = './chromedriver_darwin'
        else:
            f_driver = 'chromedriver.exe'
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
    
    def wonju(self):
        res = requests.get('https://www.wonju.go.kr/intro.jsp', verify=False)
        soup = BeautifulSoup(res.content, 'html.parser')
    
        table = soup.find('div', class_='conbox').find_all('p', class_='text')
        # 확진자  |  자가격리자  |  검사현황 |  검사중 |  결과음성
        
        self.db['확진자'] += int(table[0].text.replace(',', '')) 
        self.db['자가격리자'] += int(table[1].text.replace(',', ''))
        self.db['검사중'] += int(table[3].text.replace(',', ''))
        self.db['결과음성'] += int(table[4].text.replace(',', ''))
    


        
    def collect(self):
        # 1. reqeusts 라이브러리를 활용한 HTML 페이지 요청 
        res = requests.get('http://www.daegu.go.kr/')
        # 2) HTML 페이지 파싱 BeautifulSoup(HTML데이터, 파싱방법)
        soup = BeautifulSoup(res.content, 'html.parser')
        # 3) 필요한 데이터 검색
        li = soup.find('div', class_='con_r').find_all('li')
     
        self.wonju()
    
        stat = copy.copy(form)
        
        stat['지역'] = '강원도'
        stat['확진자'] = format(self.db['확진자'], ',')
        stat['사망자'] = li[2].text.split(' ')[1]
        stat['격리자'] = format(self.db['확진자'] - int(stat['사망자'].replace(',','')), ",")
        stat['자가격리자'] = self.db['자가격리자']
    
        print("pass : ", stat['지역'])
        
        return stat