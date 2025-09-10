import requests
import csv
from datetime import datetime

api_url = "https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_allavailable.json"

try:
    res = requests.get(api_url)
    if res.status_code == 200:
        print("Success to connect")

    nowdata = res.json()
    get_data = nowdata["data"]["park"]

    nowtime = nowdata["data"]["UPDATETIME"][0:19]
    year = nowdata["data"]["UPDATETIME"][24:28]
    mergetime = year +" " + nowtime
    realtime=datetime.strptime(mergetime,"%Y %a %b %d %H:%M:%S")

    print(f"更新時間：{realtime}")
    
    # 建立 CSV 資料列，含欄位名稱
    csv_data = [["更新時間", "id", "可用車位數"]]

    for items in get_data:
        park_id = items.get('id', 'N/A')
        available_car = items.get('availablecar', 'N/A')
        '''
        # 預設無電動車位資訊
        ev_count = "N/A"

        # 如果有電動車資料，則進行統計
        ev_data = items.get('ChargeStation', 'N/A')
        if ev_data != 'N/A' and isinstance(ev_data, dict):
            count = 0
            for item in ev_data.get('scoketStatusList', []):
                if item.get('spot_status') == '待機中':
                    count += 1
            ev_count = count
        '''        
        # 加入這筆資料到清單中
        csv_data.append([realtime, park_id, available_car])

    with open("D:\\analysis project\\data\\taipei_parking_data.csv", mode="w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

    print("CSV 檔案已成功儲存為 taipei_parking_data.csv")

except Exception as e:
    print("發生錯誤：", e)
