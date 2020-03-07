from copy import copy

def collector(region_list):
    data_list = []
    error_idx = []
    for i in range(len(region_list)):
        now = region_list[i]
        try:
            data_list.insert(i, now())
        except:
            try:
                print(u"Error occured. Retry : %s"%(now.__name__))
                data_list.insert(i, now())
            except:
                error_idx.append(i)
                print(u"Error occured at : %s"%(now.__name__))

    for i in error_idx:
        data_list.insert(i, region_list[i]())
        # 이 과정에서 Daegu() 클래스가 초기화되지 않아 누적

    return data_list