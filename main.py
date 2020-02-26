from mk_table import Mk_table
from region import *
import time

table = Mk_table()
region_list = [seoul(), 
               daegu(),    
               busan(),   
               daejeon(),
               gwangju(infected=9, quarantine=7, care=2),
               gyeongbuk(),
               gyeongnam(),
               gyeonggi(), 
               chungbuk(infected=6),
               chungnam(),
               gangwon(infected=6, suspect=1548, testing=509, negetive=1039),
               jeonbuk(infected=4, quarantine=3, self_quarantine=82, unmonitor=11, care=1),
               jeonnam()
        ]
table.generate(region_list)

readme = open('README.md', mode='wt', encoding='utf-8')
readme.write('''
## 대한민국 우한 코로나 바이러스 감염자 실시간 통계
{0}

각 시청, 도청 사이트에서 제공되는 정보를 수합하여 만든 통계입니다.
질병관리본부에서 발표되는 공식 수치와는 다를 수 있습니다.

{1}
'''.format(time.strftime(u'%Y.%m.%d %X KST', time.localtime(time.time())), table.table))
readme.close()
