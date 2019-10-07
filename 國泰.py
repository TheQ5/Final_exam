import requests
from bs4 import BeautifulSoup
import codecs

#把網址載入並整理編碼
url = requests.get(
    "https://www.cathaybk.com.tw/cathaybk/personal/credit-card/cards/intro/list/"
)
url.encoding = "utf-8"
x = BeautifulSoup(url.text, "html.parser")

#找出第一頁的卡片名稱
a1 = x.find_all("tbody")

a2 = a1[0].find_all("tr")

#透過迴圈把"h3"裡的卡片名稱取出來
times = 0
for i in a2:
    a3 = a2[times].find("h3").text
    times += 1

    print(a3)