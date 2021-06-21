"""
获得全国每天平均数据和全国每年平均数据
"""

import csv
import json
import codecs
# from collections import defaultdict
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

final_data = [["date","PM2.5","SO2","NO2"]]
domestic_yearly_data = {"全国":{}}
times = len(idx_to_prov)

for year in range(2013,2019):
    yearly_temp = [0,0,0]
    for mon in range(1,13):
        for day in range(1,month[mon-1]+1):
            temp_data = [0,0,0]
            d = str(day).zfill(2)
            y = str(year)
            m = str(mon).zfill(2)
            filename = "pollution data/" + y + m + "/CN-Reanalysis-daily-" + y + m+d+"00.csv"
            with open(filename, "r", encoding="UTF-8") as f:
                data = list(csv.reader(f))
                for i in idx_to_prov.keys():
                    temp_data[0]+=(float(data[i][0].strip()))
                    temp_data[1]+=(float(data[i][2].strip()))
                    temp_data[2]+=(float(data[i][3].strip()))
                date = y + m+d
                temp = [round(temp_data[0]/times,2),round(temp_data[1]/times,2),round(temp_data[2]/times,2)]
                for i in range(3):
                    yearly_temp[i] += temp[i]
                final_data.append([date]+temp)
    domestic_yearly_data["全国"][str(year)] = {"PM2.5": round(yearly_temp[0]/365, 2),"SO2":round(yearly_temp[1]/365, 2),
                                             "NO2":round(yearly_temp[2]/365, 2)}

with codecs.open("domesticPollution.json", 'w', encoding="utf-8") as f:
    json.dump(domestic_yearly_data, f, ensure_ascii=False)

with open("provincedata/全国.csv","w",encoding="UTF-8", newline="") as f:
    csv_writer = csv.writer(f)
    csv_writer.writerows(final_data)
