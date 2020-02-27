import requests, copy
from bs4 import BeautifulSoup
from form import form

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
    stat['격리자'] = stat['확진자']
    
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
    stat['사망자'] = li[2].text.split(' ')[1]
    
    print("pass : ", stat['지역'])
    
    return stat

def busan():
    res = requests.get('http://www.busan.go.kr/corona/index.jsp')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    li = soup.find('span', class_='item2')
    
    stat = copy.copy(form)
    
    stat['지역'] = '부산'
    stat['확진자'] = li.text[:-1]
    stat['격리자'] = li.text[:-1]
    
    print("pass : ", stat['지역'])
    
    return stat

def daejeon():
    res = requests.get('https://www.daejeon.go.kr/corona19/index.do')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    li_num2 = soup.find_all('span', class_='s-txt')
    li_txt2 = soup.find_all('span', class_='s-tit')
    
    stat = copy.copy(form)
    
    stat['지역'] = '대전'
    stat['확진자'] = soup.find('li', class_='tab-1').find('strong').text
    stat['격리자'] = soup.find('li', class_='tab-1').find('strong').text
    stat['사망자'] = soup.find('li', class_='tab-3').find('strong').text
    stat['감시중'] = li_num2[0].text[:-1] # 접촉자 격리
    stat['감시해제'] = str(int(li_num2[1].text[:-1].replace(",", "")) + int(li_num2[3].text[:-1].replace(",", ""))) # 접촉자 격리해제
    stat['의사환자'] = li_num2[2].text[:-1] # 의사환자 격리
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
        stat['완치'] = li[2].text
        stat['사망자'] = li[3].text
        stat['검사중'] = li[5].text
        stat['검사결과(음성)'] = li[6].text
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
    stat['격리자'] = table[1].text[:-1] # 추후 추가시 변경
    stat['검사중'] = table[3].text[:-1]
    stat['검사결과(음성)'] = table[5].text[:-1]
    stat['자가격리자'] = table[6].text[:-1]
    
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
    stat['완치'] = table[1].text
    stat['사망자'] = table[2].text
    
    print("pass : ", stat['지역'])
    
    return stat

def chungbuk(infected='-', quarantine='-', suspect='-', testing='-', negative='-', self_quarantine='-', unmonitor='-', care='-'):
    stat = copy.copy(form)

    stat['지역'] = '충청북도'
    stat['확진자'] = '%s'%(infected)
    stat['격리자'] = '%s'%(infected)
    stat['자가격리자'] = '%s'%(self_quarantine)
    stat['감시해제'] = '%s'%(unmonitor)
    
    print("pass : ", stat['지역'])
    
    return stat

def chungnam():
    res = requests.get('http://www.chungnam.go.kr/cnnet/content.do?mnu_cd=CNNMENU02418')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    table_init = soup.find('tbody').find_all('tr')[2]
    
    table = table_init.text.split('\n')[1:-1]
    
    stat = copy.copy(form)
    
    stat['지역'] = '충청남도'
    stat['확진자'] = table[1]
    stat['격리자'] = table[1]
    stat['검사중'] = table[6]
    stat['검사결과(음성)'] = table[5]
    stat['자가격리자'] = table[7].split(' ')[1]
    
    print("pass : ", stat['지역'])
    
    return stat

def gangwon(infected='-', quarantine='-', suspect='-', testing='-', negative='-', self_quarantine='-', unmonitor='-', care='-'):
    # https://www.provin.gangwon.kr/gw/portal/sub05_01?articleSeq=164918&mode=readForm&curPage=1&boardCode=BDAADD02
    stat = copy.copy(form)

    stat['지역'] = '강원도'
    stat['확진자'] = '%s'%(infected)
    stat['격리자'] = '%s'%(infected)
    stat['의사환자'] = '%s'%(suspect)
    stat['검사중'] = '%s'%(testing)
    stat['검사결과(음성)'] = '%s'%(negative)
    stat['자가격리자'] = '%s'%(self_quarantine)
    stat['감시해제'] = '%s'%(unmonitor)
    
    print("pass : ", stat['지역'])
    
    return stat

def gwangju(infected='-', quarantine='-', suspect='-', testing='-', negative='-', self_quarantine='-', unmonitor='-', care='-'):
    # https://www.gwangju.go.kr/
    stat = copy.copy(form)

    stat['지역'] = '광주'
    stat['확진자'] = '%s'%(infected)
    stat['격리자'] = '%s'%(quarantine)
    stat['의사환자'] = '%s'%(suspect)
    stat['검사중'] = '%s'%(testing)
    stat['검사결과(음성)'] = '%s'%(negative)
    stat['자가격리자'] = '%s'%(self_quarantine)
    stat['감시해제'] = '%s'%(unmonitor)
    stat['완치'] = '%s'%(care)
    
    print("pass : ", stat['지역'])
    
    return stat

def jeonbuk(infected='-', quarantine='-', suspect='-', testing='-', negative='-', self_quarantine='-', unmonitor='-', care='-'):
    # https://www.gwangju.go.kr/
    stat = copy.copy(form)

    stat['지역'] = '전라북도'
    stat['확진자'] = '%s'%(infected)
    stat['격리자'] = '%s'%(quarantine)
    stat['의사환자'] = '%s'%(suspect)
    stat['검사중'] = '%s'%(testing)
    stat['검사결과(음성)'] = '%s'%(negative)
    stat['자가격리자'] = '%s'%(self_quarantine)
    stat['감시해제'] = '%s'%(unmonitor)
    stat['완치'] = '%s'%(care)
    
    print("pass : ", stat['지역'])
    
    return stat

def jeonnam():
    res = requests.get('https://www.jeonnam.go.kr/M05040701/boardView.do?seq=0&menuId=jeonnam0504150400')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    table = soup.find('tbody').find_all('span')
    
    stat = copy.copy(form)
    
    stat['지역'] = '전라남도'
    stat['확진자'] = table[0].text
    stat['격리자'] = str(int(table[0].text.replace(",", "")) - int(table[4].text.replace(",", "")))
    stat['검사중'] = table[9].text
    stat['검사결과(음성)'] = table[7].text
    stat['감시해제'] = table[4].text
    stat['완치'] = table[4].text
    # stat['자가격리자'] = 
    
    print("pass : ", stat['지역'])
    
    return stat  

def ulsan(infected='-', quarantine='-', suspect='-', testing='-', negative='-', self_quarantine='-', unmonitor='-', care='-'):
    # https://www.gwangju.go.kr/
    stat = copy.copy(form)

    stat['지역'] = '울산'
    stat['확진자'] = '%s'%(infected)
    stat['격리자'] = '%s'%(quarantine)
    stat['의사환자'] = '%s'%(suspect)
    stat['검사중'] = '%s'%(testing)
    stat['검사결과(음성)'] = '%s'%(negative)
    stat['자가격리자'] = '%s'%(self_quarantine)
    stat['감시해제'] = '%s'%(unmonitor)
    stat['완치'] = '%s'%(care)
    
    print("pass : ", stat['지역'])
    
    return stat