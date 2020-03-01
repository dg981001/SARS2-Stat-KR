from util.mk_table import Mk_table
from util.region import *
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
                   gwangju(infected=9, quarantine=6, self_quarantine=1, care=2),
                   ulsan(),
                   incheon(),
                   sejong(),
                   gyeongbuk(),
                   gyeongnam(),
                   gyeonggi(), 
                   chungbuk(),
                   chungnam(),
                   Gangwon().collect(suspect=2664, testing=623, negative=2041),
                   jeonbuk(),
                   jeonnam(),
                   jeju(),
                   
                   ]
        return region_li
    except:
        if count_try < 5:
            count_try += 1
            print("Retry %d"%count_try)
            region_data()
        else:
            print("Failed : some regions occur error ")
            exit(0)

if __name__=="__main__":
    table = Mk_table()
    region_list = region_data()
    table.generate(region_list)

    readme = open('README.md', mode='wt', encoding='utf-8')
    readme.write('''
## 대한민국 우한 코로나 바이러스 감염자 실시간 통계
{0} KST

** 3월 1일 현재 각 시/도/구/군청에서 갱신해주는 속도가 지연되어 질병관리본부 수치가 더 많습니다. **

각 **시/도/구/군청** 사이트에 공개되어 있는 **공식 자료**를 수합하여 만든 통계입니다.
질병관리본부에서 발표되는 공식 수치와는 다를 수 있습니다.

**이 통계에 대해 가짜정보라고 기사를 작성한 기자와 언론사를 상대로 언론중재위원회에 손해배상청구를 진행할 예정입니다**

{1}

#1 확진자(중국인) 제외
    '''.format(kst_time(), table.table))
    readme.close()
