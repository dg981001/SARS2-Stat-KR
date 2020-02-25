import requests
from bs4 import BeautifulSoup

def seoul():
    res = requests.get('http://www.seoul.go.kr/coronaV/coronaStatus.do')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    li_num = soup.find_all('p', class_='counter')
    li_txt = soup.find_all('p', class_='txt')
    
    li_txt = [txt.text for txt in li_txt]
    li_num = [num.text for num in li_num]
    
    stat = {
        '지역'          : '-',
        '확진자'        : '-',
        '격리자'        : '-',
        '사망자'        : '-',
        '의사환자'      : '-',
        '검사중'        : '-',
        '검사결과(음성)': '-',
        '자가격리자'    : '-',
        '감시중'        : '-',
        '감시해제'      : '-'
    }
    for i in range(0, len(li_txt)-4):
        stat[li_txt[i]] = li_num[i]
    
    stat['지역'] = '서울'
    return stat

def daegu():
    # 1. reqeusts 라이브러리를 활용한 HTML 페이지 요청 
    res = requests.get('http://www.daegu.go.kr/')
 
    # 2) HTML 페이지 파싱 BeautifulSoup(HTML데이터, 파싱방법)
    soup = BeautifulSoup(res.content, 'html.parser')
 
    # 3) 필요한 데이터 검색
    li = soup.find('div', class_='con_r').find_all('li')
 
    stat = {
        '지역'          : '-',
        '확진자'        : '-',
        '격리자'        : '-',
        '사망자'        : '-',
        '의사환자'      : '-',
        '검사중'        : '-',
        '검사결과(음성)': '-',
        '자가격리자'    : '-',
        '감시중'        : '-',
        '감시해제'      : '-'
    }
    
    stat['지역'] = '대구'
    
    stat['확진자'] = li[0].text.split(' ')[1]
    stat['격리자'] = li[1].text.split(' ')[1]
    stat['사망자'] = li[2].text.split(' ')[1]
    return stat