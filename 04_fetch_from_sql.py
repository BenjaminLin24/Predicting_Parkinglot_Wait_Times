# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 14:30:25 2025

@author: BenjaminLin24
"""
import pymysql
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#輸入連接sql資訊
connect = pymysql.connect(
    host='xxx',
    user='xxx',
    db='parking_info',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

#自訂抓取日期
dates=['2025-08-17',
       '2025-08-18',
       '2025-08-19',
       '2025-08-21',
       '2025-08-26',
       '2025-08-27',
       '2025-08-28',
       '2025-08-29',
       '2025-08-30',
       '2025-08-31',]


try:
    for d in dates:
        with connect.cursor() as cursor:
            no="TPE0099"
            sql = f"""
            SELECT `剩餘車位`,`更新時間` FROM parking_lot
            WHERE DATE(`更新時間`) = '{d}'
            AND id = '{no}'
            """
            cursor.execute(sql)
            ex=cursor.fetchall()
            #print(ex)

            count=[]
            for i in ex:
                last=i["剩餘車位"]
                time=i["更新時間"]
                count.extend([last,time])

            #print(count)
            #print(len(count))

            timelist=count[1::2]
            spacelist=count[0::2]
            #print(timelist)
            #print(spacelist)
            #time=ex['更新時間']
            #print(time)
            df_allday=pd.DataFrame({"時間":timelist,"剩餘車位":spacelist})
            #df_allday.insert(1,"剩餘車位",spacelist)
            #print(df_allday)
            '''
            try:
                df_allday.to_excel("TPE0654.xlsx",index=False)
                print("成功寫入")
            except Exception as e:
                print("錯誤",e)
            '''
            
            plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.figure(figsize=(12, 6))
            sns.set_style("whitegrid")  # 背景加格線
            sns.lineplot(
                data=df_allday,
                x=timelist,
                y=spacelist,
                marker='o',
                linewidth=2,
                color="royalblue",
                alpha=0.8
                )

            plt.title(f"{no}-{d}", fontsize=16)
            plt.xlabel("TIME", fontsize=12)
            plt.ylabel("Empty Space", fontsize=12)
            plt.xticks(rotation=45)  # 時間標籤斜排，避免重疊
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.tight_layout()
            #plt.show()
            
            filename = f"D:/analysis project/曲線圖/{no}/{no}-{d}.png"
            plt.savefig(filename, dpi=300, bbox_inches="tight")  # 300dpi 比較清晰
            print(f"已儲存 {filename}")
            #plt.show()
            plt.close()
finally:
    connect.close()

    
