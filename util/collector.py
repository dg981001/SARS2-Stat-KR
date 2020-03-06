def collector(region_list):
    data_list = []
    error_idx = []
    for i in range(len(region_list)):
        try:
            data_list.insert(i, region_list[i]())
        except:
            error_idx.append(i)
            print("Error occured at : %s"%(region_list[i].__name__))

    for i in error_idx:
        data_list.insert(i, region_list[i]())

    return data_list