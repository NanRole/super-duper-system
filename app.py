from flask import Flask, render_template
import pandas as pd
from bs4 import BeautifulSoup
import requests
import io

app = Flask(__name__)

# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context # 報錯請加這兩行，不驗證SSL證書
@app.route('/')
def index():
    html = requests.get('https://data.gov.tw/dataset/34811')
    soup = BeautifulSoup(html.text, 'html.parser')
    # 找出所有 <a> 且有 title 屬性的
    links = soup.find_all('a', attrs={'title': True})
    csv_link = ''
    for a in links:
        if 'CSV' in a['title']: # 關鍵字找尋
            csv_link = a['href']
            break
    html = requests.get(csv_link)
    df = pd.read_csv(io.StringIO(html.text))
    latest = df.loc[0]['monitordate']
    x = []
    y = []
    for i in range(len(df)):
        row = df.loc[i]
        if row['monitordate'] == latest:
            x.append(f"{row['itemengname']}({row['itemunit']})")
            if row['concentration'] != 'x':
                y.append(float(row['concentration']))
            else:
                y.append(0)
    return render_template('index.html', title=latest, x=x, y=y)

app.run('0.0.0.0', debug=True)