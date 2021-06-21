"""
将地图json文件修改，将每个省每月的平均污染物数据加入其中
"""

import json
import csv
import codecs

final_data = {}
province = []
month = [31,28,31,30,31,30,31,31,30,31,30,31]
ans = {"type":"FeatureCollection"}
with open("china.json", "r", encoding="UTF-8") as f:
    new_dict = json.load(f)
    temp_list = new_dict["features"]

    for work_dict in temp_list:
        name = work_dict['properties']['name']
        province.append(name)
    # MIN = [float("inf")]*3
    # MAX = [0]*3
    # for prov in province:
    #     with open("provincedata/" +prov+ ".csv", "r", encoding="UTF-8") as f:
    #         test_data = list(csv.reader(f))
    #         # temp = {}
    #         for x in test_data[1:]:
    #             for j in range(1,4):
    #                 MIN[j-1] = min(MIN[j-1], float(x[j]))
    #                 MAX[j-1] = max(MAX[j-1], float(x[j]))
    # print(MIN)
    # print(MAX)



    for prov in province:
        with open("provincedata/" +prov+ ".csv", "r", encoding="UTF-8") as f:
            test_data = list(csv.reader(f))
            temp = {}
            idx = 1
            for y in range(2013,2019):
                for m in range(1,13):
                    PM=[]
                    NO2=[]
                    SO2=[]
                    for _ in range(month[m-1]):
                        PM.append(float(test_data[idx][1]))
                        SO2.append(float(test_data[idx][2]))
                        NO2.append(float(test_data[idx][3]))
                        idx+=1
                    temp[test_data[idx-1][0][:6]] = {"PM2.5":round(sum(PM)/len(PM),2),
                                                     "SO2":round(sum(SO2)/len(SO2),2),
                                                     "NO2":round(sum(NO2)/len(NO2),2)}
            final_data[prov] = temp


    for t in temp_list:
        t = t['properties']
        del t['id']
        del t['size']
        del t['cp']
        del t['childNum']
        t['pollution'] = final_data[t['name']]
    ans["features"] = temp_list


with codecs.open("chinaMapWithPollutionData2.json", 'w', encoding="utf-8") as f:
    json.dump(ans, f, ensure_ascii=False)


