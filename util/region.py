import requests, copy
from bs4 import BeautifulSoup
from util.form import form
from selenium import webdriver
import platform, json

dir_name = "util"

def seoul():
    res = requests.get('http://www.seoul.go.kr/coronaV/coronaStatus.do')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    li_num = soup.find_all('p', class_='counter')
    li_txt = soup.find_all('p', class_='txt')
    
    li_txt = [txt.text for txt in li_txt]
    li_num = [num.text for num in li_num]
    
    stat = copy.copy(form)
    for i in range(0, len(li_txt)-4):
        stat[li_txt[i]] = li_num[i]
    
    stat['지역'] = '서울'
    stat['퇴원'] = format(25, ',')
    stat['격리자'] = format(int(stat['확진자'].replace(",", "")) - int(stat['퇴원'].replace(",", "")), ",")
    
    
    print("pass : ", stat['지역'])
    
    return stat

def daegu():
    # 1. reqeusts 라이브러리를 활용한 HTML 페이지 요청 
    res = requests.get('http://www.daegu.go.kr/')
 
    # 2) HTML 페이지 파싱 BeautifulSoup(HTML데이터, 파싱방법)
    soup = BeautifulSoup(res.content, 'html.parser')
 
    # 3) 필요한 데이터 검색
    li = soup.find('div', class_='con_r').find_all('li')
 
    stat = copy.copy(form)
    
    stat['지역'] = '대구'
    
    stat['확진자'] = li[0].text.split(' ')[1]
    stat['격리자'] = li[1].text.split(' ')[1]
    stat['사망'] = li[2].text.split(' ')[1]
    
    print("pass : ", stat['지역'])
    
    return stat

def busan():
    res = requests.get('http://www.busan.go.kr/corona19/index')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    li = soup.find('div', class_='banner').find_all("span")
    
    stat = copy.copy(form)
    
    stat['지역'] = '부산'
    stat['확진자'] = li[1].text[:-1]
    stat['퇴원'] = li[3].text[:-1]
    stat['격리자'] = li[4].text[:-1]
    
    print("pass : ", stat['지역'])
    
    return stat

def daejeon():
    res = requests.get('https://www.daejeon.go.kr/corona19/index.do')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    li_num = soup.find_all('span', class_='s-txt')
    li_txt = soup.find_all('span', class_='s-tit')
    
    stat = copy.copy(form)
    
    stat['지역'] = '대전'
    stat['확진자'] = li_num[0].find("strong").text
    stat['퇴원'] = li_num[1].find("strong").text
    stat['격리자'] = li_num[2].find("strong").text
    stat['사망'] = li_num[3].find("strong").text
    stat['검사중'] = li_num[4].find("strong").text
    stat['결과음성'] = li_num[5].find("strong").text
    stat['자가격리자'] = li_num[6].find("strong").text
    stat['감시중'] = li_num[6].find("strong").text
    stat['감시해제'] = li_num[7].find("strong").text# 의사환자 격리
    # stat[''] = li_num[3].text[:-1] # 의사환자 격리해제
    
    print("pass : ", stat['지역'])
    
    return stat

def gyeongbuk():
    stat = copy.copy(form)
    stat['지역'] = '경상북도'
    try:
        res = requests.get('http://www.gb.go.kr/Main/open_contents/section/wel/page.do?mnu_uid=5760&LARGE_CODE=360&MEDIUM_CODE=10&SMALL_CODE=50&SMALL_CODE2=60mnu_order=2')
        soup = BeautifulSoup(res.content, 'html.parser')
        
        table = soup.find_all('table', class_='tbl_st1')[1]
        li = table.find_all('td')[1:11]
        
        stat['확진자'] = li[0].text
        stat['격리자'] = li[1].text
        stat['퇴원'] = li[2].text
        stat['사망'] = li[3].text
        stat['검사중'] = li[5].text
        stat['결과음성'] = li[6].text
        stat['감시중'] = li[8].text
        stat['감시해제'] = li[9].text
        
        print("pass : ", stat['지역'])
    
        return stat
    except:
        return stat

def gyeongnam():
    res = requests.get('http://www.gyeongnam.go.kr/corona.html')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    table = soup.find('div', class_='co_data').find_all('span')
    #li = table.find_all('td')[1:11]
    
    stat = copy.copy(form)
    
    stat['지역'] = '경상남도'
    stat['확진자'] = table[1].text[:-1]
    stat['퇴원'] = table[2].text[1:-1].split(" ")[1][:-1]
    stat['격리자'] = format(int(stat['확진자'].replace(",", "")) - int(stat['퇴원'].replace(",", "")), ",")
    stat['검사중'] = table[4].text[:-1]
    stat['결과음성'] = table[6].text[:-1]
    stat['자가격리자'] = table[7].text[:-1]
    stat['의사환자'] = format(int(stat['검사중'].replace(",", "")) + int(stat['결과음성'].replace(",", "")), ",")
    
    print("pass : ", stat['지역'])
    
    return stat

def gyeonggi():
    res = requests.get('https://www.gg.go.kr/bbs/boardView.do?bsIdx=464&bIdx=2296956&menuId=1535')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    table = soup.find('ul', class_='column-4').find_all('strong')
    
    stat = copy.copy(form)
    
    stat['지역'] = '경기도'
    stat['확진자'] = table[3].text
    stat['격리자'] = table[0].text
    stat['퇴원'] = table[1].text
    stat['사망'] = table[2].text
    
    print("pass : ", stat['지역'])
    
    return stat

def chungbuk():
    res = requests.get('http://www.chungbuk.go.kr/www/covid-19/index.html')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    table = soup.find('ul', class_="clearfix").find_all("p", class_='text') # 확진자, 검사중, 검사결과(음성)

    stat = copy.copy(form)
    
    stat['지역'] = '충청북도'
    stat['확진자'] = table[0].text
    stat['의사환자'] = table[1].text
    stat['검사중'] = table[2].text
    stat['결과음성'] = table[3].text
    stat['자가격리자'] = table[4].text
    stat['감시중'] = table[5].text
    stat['감시해제'] = table[6].text
    stat['격리자'] = stat['확진자']
    # stat['퇴원'] = 
    
    print("pass : ", stat['지역'])
    return stat

def chungnam():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    if platform.system() == 'Linux':
        f_driver = '%s/chromedriver'%(dir_name)
    elif platform.system() == 'Darwin':
        f_driver = '%s/chromedriver_darwin'%(dir_name)
    else:
        f_driver = '%s/chromedriver.exe'%(dir_name)
    driver = webdriver.Chrome(f_driver, options=options)
    driver.get('http://www.chungnam.go.kr/coronaStatus.do')
    driver.implicitly_wait(2)
    table = driver.find_elements_by_class_name('item')
    
    stat = copy.copy(form)
    
    stat['지역'] = '충청남도'
    stat['확진자'] = table[0].text.split("\n")[-1]
    stat['격리자'] = stat['확진자']
    stat['검사중'] = table[1].text.split("\n")[-1]
    stat['결과음성'] = table[2].text.split("\n")[-1]
    stat['자가격리자'] = table[3].text.split("\n")[1]
    #stat['감시해제'] = table[3].text.split("\n")[3]
    
    print("pass : ", stat['지역'])
    
    return stat

def gangwon():
    res = requests.get('https://www.provin.gangwon.kr/covid-19.html', verify=True)
    soup = BeautifulSoup(res.content, 'html.parser')
        
    table = soup.find('ul').find_all("span")
    
    stat = copy.copy(form)

    stat['지역'] = '강원도'
    stat['확진자'] = table[0].text[:-1]
    stat['자가격리자'] = table[1].text[:-1]
    stat['검사중'] = table[2].text[:-1]
    stat['퇴원'] = table[3].text[:-1]
    stat['격리자'] = format(int(stat['확진자'].replace(",", "")) - int(stat['퇴원'].replace(",", "")), ',')
    
    print("pass : ", stat['지역'])
    
    return stat

def gwangju(infected='-', quarantine='-', suspect='-', testing='-', negative='-', self_quarantine='-', unmonitor='-', care='-'):
    # https://www.gwangju.go.kr/
    stat = copy.copy(form)
    # before : gwangju(infected=13, quarantine=9, self_quarantine=1, care=3)
    stat['지역'] = '광주'
    stat['확진자'] = '%s'%(14) # (infected)
    stat['격리자'] = '%s'%(9) # (quarantine)
    stat['의사환자'] = '%s'%(suspect)
    stat['검사중'] = '%s'%(testing)
    stat['결과음성'] = '%s'%(negative)
    stat['자가격리자'] = '%s'%(2) # (self_quarantine)
    stat['감시해제'] = '%s'%(unmonitor)
    stat['퇴원'] = '%s'%(3) # (care)
    
    print("pass : ", stat['지역'])
    
    return stat

def jeonbuk():
    res = requests.get('http://www.jeonbuk.go.kr/index.jeonbuk')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    table = soup.find('ul', class_="tb_ul").find("ul").find_all('font')#.find_all('td')

    stat = copy.copy(form)
    
    stat['지역'] = '전라북도'
    stat['확진자'] = table[0].text
    stat['격리자'] = table[1].text
    stat['퇴원'] = table[2].text
    stat['자가격리자'] = table[3].text
#    stat['감시해제'] = table[3]
#    stat['감시중'] = table[4]
#    stat['결과음성'] = table[5]
#    stat['검사중'] = table[6]
#    stat['의사환자'] = format(int(stat['결과음성'].replace(',', '')) + int(stat['검사중'].replace(',', '')), ',')
#    
    print("pass : ", stat['지역'])
    return stat

def jeonnam():
    res = requests.get('https://www.jeonnam.go.kr/coronaMainPage.do')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    table = soup.find_all('p', class_='num')
    
    stat = copy.copy(form)
    
    stat['지역'] = '전라남도'
    stat['확진자'] = table[1].text.replace(',','')
    stat['퇴원'] = format(1,',')  
    stat['격리자'] = format(int(stat['확진자'].replace(",", "")) - int(stat['퇴원'].replace(",", "")), ',')
    stat['검사중'] = table[4].text.replace(',','')
    stat['결과음성'] = table[2].text.replace(',','')
    stat['감시중'] = table[5].text.replace(',','')
    stat['감시해제'] = table[6].text.replace(',','')
    # stat['자가격리자'] = 
    
    print("pass : ", stat['지역'])
    
    return stat  

def ulsan():
    res = requests.get('http://www.ulsan.go.kr/corona.jsp')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    table = soup.find('tbody').text.replace("\n\n", '').split("\n")#.find_all('td')
    
    stat = copy.copy(form)
    
    stat['지역'] = '울산'
    stat['확진자'] = table[0]
    stat['퇴원'] = table[1]
    stat['격리자'] = int(stat['확진자'].replace(',','')) - int(stat['퇴원'].replace(',',''))
    stat['감시해제'] = table[3]
    stat['감시중'] = table[4]
    stat['결과음성'] = table[5]
    stat['검사중'] = table[6]
    stat['의사환자'] = format(int(stat['결과음성'].replace(',', '')) + int(stat['검사중'].replace(',', '')), ',')
    
    print("pass : ", stat['지역'])
    return stat

def incheon():
    res = requests.get('https://www.incheon.go.kr/health/HE020409')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    table_init = soup.find_all('tbody')[1] # 확진자, 검사중, 결과음성
    table = ' '.join(table_init.text.replace("\n", " ").split()).split(' ')
#    table2 = soup.find('div', class_="list3").find_all('dd') # 감시중, 감시해제 (총합 : 자가격리자)

    stat = copy.copy(form)
    
    stat['지역'] = '인천'
    stat['확진자'] = table[1]
    stat['격리자'] = format(int(table[1].replace(',','')) - 2, ',')
    stat['퇴원'] = format(2, ',')
#    stat['퇴원'] = table[2].text
#    stat['감시중'] = table2[0].text[:-1]
#    stat['감시해제'] = table2[1].text[:-1]
#    stat['자가격리자'] = format(int(stat['감시중'].replace(',', '')) + int(stat['감시해제'].replace(',', '')), ',')
    stat['결과음성'] = table[5]
    stat['검사중'] = format(int(table[3].replace(',', '')) + int(table[4].replace(',', '')), ',')
    stat['의사환자'] = format(int(stat['검사중'].replace(',', '')) + int(stat['결과음성'].replace(',', '')), ',')    
#
    print("pass : ", stat['지역'])
#    return stat
    return stat

def jeju():
    headers = {'Referer': 'https://www.jeju.go.kr/index.htm'}
    res = requests.get('https://www.jeju.go.kr/api/corona.jsp', headers=headers)
    res.encoding = 'eur-kr'
    table = json.loads(res.content)
    # print(table[0].text.split("\n"))
    # print(table[1].text.split("\n"))
    # print(table[2].text.split("\n"))
    # print(table[3].text.split("\n"))
    stat = copy.copy(form)
    
    stat['지역'] = '제주도'
    stat['확진자'] = table['field2'] # 확진
    stat['사망'] = table['field3'] # 사망
    stat['검사중'] = table['field5'] # 검사중
    stat['자가격리자'] = table['field11'] # 자가격리
    stat['퇴원'] = table['field13'] # 퇴원
    stat['격리자'] = str(int(stat['확진자'].replace(",", "")) - int(stat['사망'].replace(",", "")) - int(stat['퇴원'].replace(",", "")))

    print("pass : ", stat['지역'])

    return stat

def sejong():
    res = requests.get('https://www.sejong.go.kr/prog/fluInfo/listAjax.do')#, headers=headers)
    table = json.loads(res.content)

    stat = copy.copy(form)
    
    stat['확진자'] = table['info1'] # 확진
    stat['격리자'] = table['info1'] # 격리자
    stat['검사중'] = table['info3'] # 검사중
    stat['결과음성'] = table['info4'] # 결과음성

    print("pass : ", stat['지역'])

    return stat