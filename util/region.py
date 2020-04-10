import requests, copy
from bs4 import BeautifulSoup
from util.form import form
#from selenium import webdriver
import platform, json, re

dir_name = "util"
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
headers = {'User-Agent': user_agent}

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
    stat['사망'] = li[5].text[:-1]
    
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
    stat['감시해제'] = li_num[7].find("strong").text# 의심환자 격리
    # stat[''] = li_num[3].text[:-1] # 의심환자 격리해제
    
    print("pass : ", stat['지역'])
    
    return stat

def gyeongbuk():
    stat = copy.copy(form)
    stat['지역'] = '경상북도'
    try:
        res = requests.get('http://www.gb.go.kr/Main/open_contents/section/wel/page.do?mnu_uid=5760&LARGE_CODE=360&MEDIUM_CODE=10&SMALL_CODE=50&SMALL_CODE2=60mnu_order=2')
        soup = BeautifulSoup(res.content, 'html.parser')
        res_cdc = requests.get('http://ncov.mohw.go.kr/')#, headers=headers)
        soup_cdc = BeautifulSoup(res_cdc.content, 'html.parser')
        confirmed = soup_cdc.find('div', id='map_city15').find('span', class_='num').text.replace("명", '').replace(" ", "")
        
        table = soup.find_all('table', class_='tbl_st1')[1]
        li = table.find_all('td')[1:11]
        
        stat['확진자'] = confirmed
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
    
    res = requests.get('http://xn--19-q81ii1knc140d892b.kr/main/main.do#close')
    #soup = BeautifulSoup(res.content, 'html.parser')
    #table = soup.find_all('span', class_='num_people counter')
    table = re.findall('<span class="num_people counter.*?">(.*?)</span>', res.text)[:5]
    
    stat = copy.copy(form)
    
    stat['지역'] = '경상남도'
    stat['격리자'] = table[0]
    stat['퇴원'] = table[1]
    stat['확진자'] = table[2]
    # format(int(stat['확진자'].replace(",", "")) - int(stat['퇴원'].replace(",", "")), ",")
    stat['검사중'] = table[3]
    stat['결과음성'] = table[4]
    # stat['자가격리자'] = table[7].text[:-1]
    stat['의심환자'] = format(int(stat['검사중'].replace(",", "")) + int(stat['결과음성'].replace(",", "")), ",")
    
    print("pass : ", stat['지역'])
    
    return stat

def gyeonggi():
    res = requests.get('https://www.gg.go.kr/contents/contents.do?ciIdx=1150&menuId=2909')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    temp = soup.find('div', class_='s-w-covid19').find('div', class_='gg')
    table = re.findall('<strong id=".*?">(.*?)</strong>', str(temp))
    
    stat = copy.copy(form)
    
    stat['지역'] = '경기도'
    stat['확진자'] = table[0]
    stat['격리자'] = table[1]
    stat['퇴원'] = table[2]
    stat['사망'] = table[3]
    
    print("pass : ", stat['지역'])
    
    return stat

def chungbuk():
    res = requests.get('http://www1.chungbuk.go.kr/covid-19/index.do')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    table = soup.find('ul', class_="clearfix").find_all("p", class_='text')
    confirm_cure = soup.find('ul', class_="clearfix").find_all("p", class_='text2')

    stat = copy.copy(form)
    
    stat['지역'] = '충청북도'
    stat['확진자'] = confirm_cure[0].text
    stat['의심환자'] = table[0].text
    stat['검사중'] = table[1].text
    stat['결과음성'] = table[2].text
    stat['자가격리자'] = table[3].text
    stat['감시중'] = table[4].text
    stat['감시해제'] = table[5].text
    stat['퇴원'] = confirm_cure[1].text
    stat['격리자'] = format(int(stat['확진자'].replace(',', '')) - int(stat['퇴원'].replace(',', '')))
    
    print("pass : ", stat['지역'])

    return stat

def chungnam():
    res = requests.get('http://www.chungnam.go.kr/coronaStatus.do') #, headers=headers)
    data = BeautifulSoup(res.content, 'html.parser')
    init = data.find_all('ul', class_='small_list')
    self_quarantine = data.find('div', class_='item item03').find('li').find('strong').text
    
    table = []
    for i in range(len(init)):
        init[i].find_all('li')[1].find('span').extract()
        d = init[i].find_all('li')[1].text[:-1]
        table.append(d)

    stat = copy.copy(form)
    
    stat['지역'] = '충청남도'
    stat['확진자'] = table[2]
    stat['격리자'] = table[1]
    stat['퇴원'] = table[0]
    stat['사망'] = table[3]
    stat['검사중'] = table[4]
    stat['결과음성'] = table[5]
    stat['자가격리자'] = self_quarantine
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

def gwangju():
    res = requests.get('https://www.gwangju.go.kr/c19/')#, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    # 확진자  |  능동감시자
    temp = soup.find('div', 'person_box')
    table = re.findall(u"<span>(.*?)</span>명",str(temp))
    

    stat = copy.copy(form)
    stat['지역'] = '광주'
    stat['확진자'] = table[0]
    stat['퇴원'] = table[4]
    stat['격리자'] = format(int(stat['확진자'].replace(',', '')) - int(stat['퇴원'].replace(',', '')), ',')
    stat['검사중'] = table[8]
    stat['결과음성'] = table[7]
    stat['의심환자'] = table[5] # format(int(stat['검사중'].replace(',', '')) + int(stat['결과음성'].replace(',', '')), ',')
    stat['감시중'] = table[10] # (self_quarantine)
    stat['감시해제'] = table[11]
    stat['자가격리자'] = table[9] # format(int(stat['감시중'].replace(',', '')) + int(stat['감시해제'].replace(',', '')), ',')


    # before : gwangju(infected=13, quarantine=9, self_quarantine=1, care=3)
    #stat['지역'] = '광주'
    #stat['확진자'] = '%s'%(15) # (infected)
    #stat['격리자'] = '%s'%(12) # (quarantine)
    #stat['의심환자'] = '%s'%(suspect)
    #stat['검사중'] = '%s'%(testing)
    #stat['결과음성'] = '%s'%(negative)
    #stat['자가격리자'] = '%s'%(3) # (self_quarantine)
    #stat['감시해제'] = '%s'%(unmonitor)
    #stat['퇴원'] = '%s'%(3) # (care)
    
    print("pass : ", stat['지역'])
    
    return stat

def jeonbuk():
    try:
        res = requests.get('http://www.jeonbuk.go.kr/index.jeonbuk')
        soup = BeautifulSoup(res.content, 'html.parser')
        table = soup.find('ul', class_="tb_ul").find("ul").find_all('font')#.find_all('td')

    except:
        stat = copy.copy(form)
    
        stat['지역'] = '전라북도'
        return stat
    
    

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
#    stat['의심환자'] = format(int(stat['결과음성'].replace(',', '')) + int(stat['검사중'].replace(',', '')), ',')
#    
    print("pass : ", stat['지역'])
    return stat

def jeonnam():
    res = requests.get('https://www.jeonnam.go.kr/coronaMainPage.do', verify=False)
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
    #soup = BeautifulSoup(res.content, 'html.parser')
    #table = soup.find_all('span', class_='num_people counter')
    table = re.findall('<span class="num_people counter.*?">(.*?)</span>', res.text)
    
    stat = copy.copy(form)
    
    stat['지역'] = '울산'
    stat['격리자'] = table[0]
    stat['퇴원'] = table[1]
    stat['사망'] = table[2]
    stat['확진자'] = format(int(stat['격리자'].replace(',','')) + int(stat['퇴원'].replace(',','')), ',')
    stat['감시해제'] = table[4]
    stat['감시중'] = table[3]
    stat['자가격리자'] = format(int(stat['감시해제'].replace(',','')) + int(stat['감시중'].replace(',','')), ',')
    stat['결과음성'] = table[6]
    stat['검사중'] = table[5]
    stat['의심환자'] = format(int(stat['결과음성'].replace(',', '')) + int(stat['검사중'].replace(',', '')), ',')
    
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
    stat['격리자'] = format(int(table[1].replace(',','')), ',')
    #stat['퇴원'] = format(2, ',')
#    stat['퇴원'] = table[2].text
#    stat['감시중'] = table2[0].text[:-1]
#    stat['감시해제'] = table2[1].text[:-1]
#    stat['자가격리자'] = format(int(stat['감시중'].replace(',', '')) + int(stat['감시해제'].replace(',', '')), ',')
    stat['결과음성'] = table[5]
    stat['검사중'] = format(int(table[3].replace(',', '')) + int(table[4].replace(',', '')), ',')
    stat['의심환자'] = format(int(stat['검사중'].replace(',', '')) + int(stat['결과음성'].replace(',', '')), ',')    
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
    table = json.loads(res.content)[0]

    stat = copy.copy(form)
    
    stat['지역'] = '세종'
    stat['확진자'] = table['info1'] # 확진
    stat['격리자'] = table['info6'] # 격리자
    stat['검사중'] = table['info3'] # 검사중
    stat['퇴원'] = table['info5'] # 완치자
    stat['자가격리자'] = table['info4'].split("(")[0] # 결과음성

    print("pass : ", stat['지역'])

    return stat

def foreign():
    stat = copy.copy(form)
    
    stat['지역'] = '검역'
    stat['확진자'] = "352" # 확진
    stat['격리자'] = "349" # 격리자
    stat['퇴원'] = "3" # 퇴원
    #stat['결과음성'] =  # 결과음성

    print("pass : ", stat['지역'])

    return stat
