class Mk_table():
    def __init__(self):
        self.title = '''
|  지역  | 확진자 |  격리자  |  사망자  |  의사환자  |  검사중  |  검사결과(음성)  |  자가격리자  |  감시중  |  감시해제  |  완치  |
|:------:|:------:|:--------:|:--------:|:----------:|:--------:|:----------------:|:------------:|:--------:|:----------:|:--:|\n'''
        
        self.total = {
        '지역'          : '총합',
        '확진자'        : 0,
        '격리자'        : 0,
        '사망자'        : 0,
        '의사환자'      : 0,
        '검사중'        : 0,
        '검사결과(음성)': 0,
        '자가격리자'    : 0,
        '감시중'        : 0,
        '감시해제'      : 0,
        '완치'          : 0
    }
        
    
    def add_region(self, stat):
        line = "|"
        for key, val in stat.items():
            line = line + str(val) + "|"
            try:
                self.total[key] = self.total[key] + int(val.replace(',', ''))
            except:
                self.total[key] = self.total[key]
                
        return line
    
    def add_total(self, stat):
        line = "|"
        for key, val in stat.items():
            try:
                line = line + format(val, ",") + "|"
            except:
                line = line + str(val) + "|"
                
        return line
    
    def generate(self, region_list):
        temp = ''
        for i in range(len(region_list)):
            temp = temp + self.add_region(region_list[i]) + '\n'
            
        for key, val in self.total.items():
            if self.total[key] == 0:
                self.total[key] = '-'
        
        table = """
        {0}{1}{2}
        """.format(self.title, temp, self.add_total(self.total))
        
        self.table = table
        return table