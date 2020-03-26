import pandas as pd
from util.form import form
from numpy import nan
from util.KST import kst_time_for_file

class table():
    def __init__(self):
        self.DataFrame = pd.DataFrame(columns=list(form.keys()))
        self.Chart = '''
|  지역  | 확진자 |  격리자  |  사망  |  의심환자  |  검사중  |  결과음성  |  자가격리자  |  감시중  |  감시해제  |  퇴원  |
|:------:|:------:|:--------:|:--------:|:----------:|:--------:|:----------------:|:------------:|:--------:|:----------:|:--:|\n'''

    def generate(self, region_data):
        chart = pd.DataFrame(columns=list(form.keys()))
        for i in range(len(region_data)):
            chart = chart.append(region_data[i], ignore_index=True)

        chart = chart.replace('-', nan)

        for col in chart.columns[1:]:
            chart[col] = pd.to_numeric(chart[col].str.replace(',',''))

        chart = chart.set_index('지역')

        chart.loc['총합'] = chart.sum(skipna=True)
        chart = chart.fillna('-').astype('int', errors='ignore')
        self.DataFrame = chart
        self.DataFrame.to_excel("table/%s.xlsx"%(kst_time_for_file()))
        print("Save")


    # def to_markdown(self):
        ## 총합 맨 위 표기
        total_val = list(chart.loc['총합'])
        total = "|**%s**|"%('총합')
        for i in range(len(total_val)):
            try:
                total += '**' + format(int(total_val[i]), ',') + '**|'
            except:
                total += '**' + total_val[i] + '**|'
        total += '\n'
        self.Chart += total

        for idx in chart.index[:-1]:
            temp = list(chart.loc[idx])
            line = "|%s|"%idx
            for i in range(len(temp)):
                try:
                    line += format(int(temp[i]), ',') + '|'
                except:
                    line += temp[i] + '|'
            line += '\n'

            self.Chart += line

        self.Chart += total

        return self.Chart


