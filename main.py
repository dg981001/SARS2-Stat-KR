from util.table import table
from util.region import *
from util.Daegu import Daegu
from util.Seoul import Seoul
#from util.Gangwon import Gangwon
from util.KST import kst_time
from util.collector import collector

regions = [Seoul().collect, 
               Daegu().collect,    
               busan,   
               daejeon,
               gwangju,
               ulsan,
               incheon,
               sejong,
               gyeongbuk,
               gyeongnam,
               gyeonggi, 
               chungbuk,
               chungnam,
               gangwon,
               jeonbuk,
               jeonnam,
               jeju,
               foreign,
        ]

if __name__=="__main__":
    table = table()
    data = collector(regions)
    try:
        table.generate(data)
    except:
        data = collector(regions)
        table.generate(data)

    readme = open('README.md', mode='wt', encoding='utf-8')
    readme.write('''
## 중국 우한 바이러스(SARS-CoV-2) 대한민국 확진자 통계
#### Confirmed cases of China-Virus in Korea
{0} KST

각 **시/도/구/군청** 사이트에 공개되어 있는 **공식 자료**를 수합하여 만든 통계입니다.
질병관리본부에서 발표되는 공식 수치와는 다를 수 있습니다.

{1}

** 부산, 경상남도 홈페이지에 표시된 수치가 질병관리본부 발표보다 적습니다. **<br>
#1 확진자(중국인) 제외
    '''.format(kst_time(), table.Chart))
    readme.close()
