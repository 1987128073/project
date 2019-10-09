import requests
url = 'http://192.168.1.45:30050/render.html?url=https://m.dianshangji.com/analyst_mtaobaodaydb/analyst.html?itemid=588706299432#itemid=588706299432'
r = requests.get(url=url)
print(r.text)