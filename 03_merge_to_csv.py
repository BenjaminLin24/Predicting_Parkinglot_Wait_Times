# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 14:30:25 2025

@author: BenjaminLin24
"""

import requests
from datetime import datetime, timedelta
import pandas as pd
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

def fetch_parking_data():
    api_url = "https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_allavailable.json"

    try:
        res = requests.get(api_url)
        if res.status_code == 200:
            print("Success to connect")
    
        #抓取停車場id和車位
        nowdata = res.json()
        get_data = nowdata["data"]["park"]

        #抓取時間
        nowtime = nowdata["data"]["UPDATETIME"][0:19]
        year = nowdata["data"]["UPDATETIME"][24:28]
        mergetime = year +" " + nowtime
        realtime=datetime.strptime(mergetime,"%Y %a %b %d %H:%M:%S")
        print(f"更新時間：{realtime}")
    
        #累積和寫入資料
        csv_data = []
        for items in get_data:
            park_id = items.get('id', 'N/A')
            available_car = items.get('availablecar', 'N/A')
            csv_data.append([realtime, park_id, available_car])

        df_dynamic=pd.DataFrame(csv_data,columns=["更新時間", "id", "可用車位數"])
        #print(df_dynamic.head())
        print("成功pd")

    except Exception as e:
        print("發生錯誤：", e)

    #抓取靜態資料(靜態資料來自另一json檔抓取後輸出的csv)
    df_staticinfo=pd.read_csv("D:\\yourdata.csv",encoding="utf-8")

    #合併資料
    merger = pd.merge(df_staticinfo, df_dynamic, on='id', how='outer')
    #print(merger.head())
    df_filmerger = merger[(merger["可用車位數"]!=0)&(merger["可用車位數"]!=-9)&(merger["可用車位數"]!=-3)&(merger["可用車位數"]!=-6)&(merger["可用車位數"].notna())&(merger["name"].notna())]

    #命名資料並寫入資料
    today=datetime.now().strftime("%m-%d")
    filename=f"{today}_parking_info.csv"
    #try:
        #    merger.to_csv(filename, mode="a", header=False, index=False, encoding="utf-8")
        #    print("檔案已經寫入")
        #except FileNotFoundError:
            #    merger.to_csv(filename, index=False, encoding="utf-8-sig")
            #    print("檔案已新增並寫入")
            #except Exception as e:
                #    print(f"寫入檔案時發生錯誤: {e}")
    header_exists = os.path.exists(filename)
    df_filmerger.to_csv(filename, mode="a", header=not header_exists, index=False, encoding="utf-8-sig")
    rightnow=datetime.now()
    print(f"{rightnow}成功寫入")


#使用排程，每天的早上6.到22.，每五分鐘執行
scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
trigger = CronTrigger(minute='*/5', hour='6-22', timezone="Asia/Shanghai")
scheduler.add_job(fetch_parking_data, trigger)
scheduler.start()

try:
    while True:
        time.sleep(1)  # 主程式維持執行
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()