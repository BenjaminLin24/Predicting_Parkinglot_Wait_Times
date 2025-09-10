import json
import pandas as pd

try:
    with open("D:\\TCMSV_alldesc.json","r",encoding="utf-8") as file:
        print("讀寫成功")
        json_data=json.load(file)
        real_data=json_data["data"]["park"]
        print(real_data)
except FileNotFoundError:
    print("找不到檔案")

pd_data=pd.json_normalize(real_data)
print(pd_data)

pd_data.to_csv("D:\\yourdata.csv", index=False, encoding="utf-8-sig")
print("轉換成功")
