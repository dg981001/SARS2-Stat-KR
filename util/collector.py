from copy import copy

def collector(region_list):
    data_list = []
    error_idx = []
    for i in range(len(region_list)):
        temp_method = copy(region_list[i])
        try:
            data_list.insert(i, temp_method())
        except:
            error_idx.append(i)
            print("Error occured at : %s"%(region_list[i].__name__))

    for i in error_idx:
        temp_method = copy(region_list[i])
        data_list.insert(i, region_list[i]())
        # 이 과정에서 Daegu() 클래스가 초기화되지 않아 누적

    return data_list