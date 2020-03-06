from util.mk_table import Mk_table
from util.region import *
from util.Seoul import Seoul
from util.Daegu import Daegu
from util.Gangwon import Gangwon
from util.KST import kst_time

count_try = 0

def region_data():
    global count_try
    try:
        region_li = [seoul(),
                   Daegu().collect(),    
                   busan(),   
                   daejeon(),
                   gwangju(infected=13, quarantine=10, self_quarantine=1, care=2),
                   ulsan(),
                   incheon(),
                   sejong(),
                   gyeongbuk(),
                   gyeongnam(),
                   gyeonggi(), 
                   chungbuk(),
                   chungnam(),
                   gangwon(),
                   jeonbuk(),
                   jeonnam(),
                   jeju(),
                   
                   ]
        return region_li
    except:
        if count_try < 10:
            count_try += 1
            print("Retry %d"%count_try)
            region_data()
        else:
            print("Failed : some regions occur error ")

if __name__=="__main__":
    table = Mk_table()
    region_list = region_data()
    table.generate(region_list)

    readme = open('README.md', mode='wt', encoding='utf-8')
    readme.write('''
## 대한민국 우한 코로나 바이러스 감염자 실시간 통계
{0} KST

** 부산, 경상북도 홈페이지에 표시된 수치가 질병관리본부 발표보다 적습니다. **

각 **시/도/구/군청** 사이트에 공개되어 있는 **공식 자료**를 수합하여 만든 통계입니다.
질병관리본부에서 발표되는 공식 수치와는 다를 수 있습니다.

{1}

#1 확진자(중국인) 제외
    '''.format(kst_time(), table.table))
    readme.close()
