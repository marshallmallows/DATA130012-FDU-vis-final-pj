"""
将数据处理成了每个省份每天的平均值，只考虑了PM2.5、SO2和NO2三种污染物
"""

import csv
import json
# from collections import defaultdict
import math
# import numpy
def is_in_poly(p, poly):
    # 判断一个点是否在一个多边形内
    px, py = p
    is_in = False
    for i, corner in enumerate(poly):
        next_i = i + 1 if i + 1 < len(poly) else 0
        x1, y1 = corner
        x2, y2 = poly[next_i]
        if (x1 == px and y1 == py) or (x2 == px and y2 == py):
            is_in = True
            break
        if min(y1, y2) < py <= max(y1, y2):
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:
                is_in = True
                break
            elif x > px:
                is_in = not is_in
    return is_in


province = dict()
idx_to_prov = dict()


# 得到一个省份对应其多边形的字典province
with open("china.json", "r", encoding="UTF-8") as f:
    new_dict = json.load(f)
    temp_list = new_dict["features"]
    for work_dict in temp_list:
        name = work_dict['properties']['name']
        coordinates = work_dict['geometry']['coordinates'][0]
        province[name] = coordinates

province["河北省"] = province["河北省"][0]

# 得到一个数据与对应省份的字典idx_to_prov
with open("pollution data/201301/CN-Reanalysis-daily-2013010100.csv", "r", encoding="UTF-8") as f:
    test_data = csv.reader(f)
    test_data = list(test_data)
    count = 0
    for i in range(1, len(test_data)):
        lon,lat = float(test_data[i][-2]), float(test_data[i][-3])
        for prov,cod in province.items():
            if is_in_poly([lon,lat], cod):
                idx_to_prov[i] = prov
                break


month = [31,28,31,30,31,30,31,31,30,31,30,31]

final_data = {k: [["date","PM2.5","SO2","NO2"]] for k in province.keys()}
for year in range(13,19):
    for mon in range(1,13):
        for day in range(1,month[mon-1]+1):
            temp_data = {k: {"PM2.5": [], "SO2": [], "NO2": []} for k in province.keys()}
            d = str(day).zfill(2)
            y = "20"+str(year)
            m = str(mon).zfill(2)
            filename = "pollution data/" + y + m + "/CN-Reanalysis-daily-" + y+ m+d+"00.csv"
            with open(filename, "r", encoding="UTF-8") as f:
                data = list(csv.reader(f))
                for i in idx_to_prov.keys():
                    temp_data[idx_to_prov[i]]["PM2.5"].append(float(data[i][0].strip()))
                    temp_data[idx_to_prov[i]]["SO2"].append(float(data[i][2].strip()))
                    temp_data[idx_to_prov[i]]["NO2"].append(float(data[i][3].strip()))
                for k,temp_dict in temp_data.items():
                    final_data[k].append([y+m+d, round((sum(temp_dict["PM2.5"])/(len(temp_dict["PM2.5"])+1)),2),
                                          round((sum(temp_dict["SO2"])/(len(temp_dict["SO2"])+1)),2),
                                          round((sum(temp_dict["NO2"])/(len(temp_dict["NO2"])+1)),2)])


for prov, data in final_data.items():
    filename = "provincedata/" + prov+".csv"
    with open(filename,"w",encoding="UTF-8", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(data)
