from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

import ssl
ssl._create_default_https_context = ssl._create_unverified_context # 報錯請加這兩行，不驗證SSL證書
import datetime

@app.route('/')
def index():
    tables = pd.read_html('https://donate.ndhu.edu.tw/p/404-1195-239300.php?Lang=zh-tw')
    table = tables[0]
    datas = table[:-2].groupby('日期').sum()
    print(datas)
    year = datetime.date.today().year
    last = table.iloc[-1]
    month = last['#'][2:-2]
    yearmonth = f'{year}年{month}'
    x = list(datas.index)
    y = list(datas['捐贈金額'])
    return render_template('index.html', title=yearmonth, x=x, y=y)

app.run('0.0.0.0', debug=True)
