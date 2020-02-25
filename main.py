from mk_table import Mk_table
from region import *
import time

table = Mk_table()
table.generate([seoul(), daegu()])

readme = open('README.md', mode='wt', encoding='utf-8')
readme.write('''
## 대한민국 우한 코로나 바이러스 감염자 실시간 통계
{0}

{1}
'''.format(time.strftime(u'%Y.%m.%d %X KST', time.localtime(time.time())), table.table))
readme.close()
