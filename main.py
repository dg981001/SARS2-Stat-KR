from util.mk_table import Mk_table
from util.region import *
from util.Daegu import Daegu
from util.KST import kst_time


if __name__=="__main__":
    table = Mk_table()
    region_list = [seoul(),
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
                   gangwon(infected=7, suspect=1881, testing=384, negative=1497),
                   jeonbuk(),
                   jeonnam(),
                   jeju(),
                   
                   ]
    table.generate(region_list)

    readme = open('README.md', mode='wt', encoding='utf-8')
    readme.write('''
## 대한민국 우한 코로나 바이러스 감염자 실시간 통계
{0} KST

** 빠른 시일 내에 서울특별시 구청별 통계 수합 코드를 작성하여 실시간 반영할 수 있도록 하겠습니다. **

각 **시/도/구/군청** 사이트에 공개되어 있는 **공식 자료**를 수합하여 만든 통계입니다.
질병관리본부에서 발표되는 공식 수치와는 다를 수 있습니다.

**이 통계에 대해 가짜정보라고 기사를 작성한 기자와 언론사를 상대로 언론중재위원회에 손해배상청구를 진행할 예정입니다**

{1}

#1 확진자(중국인) 제외
    '''.format(kst_time(), table.table))
    readme.close()
