"""
将每个省和全国每年的平均数据保存到一个json文件中
"""

import json
import csv
import codecs

final_data = {}
pollname = ["PM2.5", "SO2", "NO2"]
month = [31,28,31,30,31,30,31,31,30,31,30,31]
ans = {}
with open("chinaMapWithPollutionData2.json", "r", encoding="UTF-8") as f:
    new_dict = json.load(f)
    temp_list = new_dict["features"]
    for mydict in temp_list:
        tempdict = mydict["properties"]
        name = tempdict["name"]
        temp = {}
        for year in range(2013,2019):
            y = str(year)
            pollute = [0, 0, 0]
            for mon in range(1,13):
                m = str(mon).zfill(2)
                for i in range(3):
                    pollute[i]+=tempdict["pollution"][y+m][pollname[i]]*month[mon-1]
            temp[y] = {pollname[i]:round(pollute[i]/365,2) for i in range(3)}
            ans[name] = temp

with open("domesticPollution.json", "r", encoding="UTF-8") as f:
    new_dict = json.load(f)
    ans["全国"]=new_dict["全国"]

with codecs.open("yearlyData.json", 'w', encoding="utf-8") as f:
    json.dump(ans, f, ensure_ascii=False)


