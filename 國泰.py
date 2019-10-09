import requests
from bs4 import BeautifulSoup
import codecs

#把網址載入並整理編碼
url = requests.get(
    "https://www.cathaybk.com.tw/cathaybk/personal/credit-card/cards/intro/list/"
)
url.encoding = "utf-8"
x = BeautifulSoup(url.text, "html.parser")

#找出卡片名稱
times = 0
title = x.find_all("div",{
		"class" : "card-name"
	})
for i in title:
	titleTEXT = title[times].find("h3").text
	times += 1

#找出卡片特色 && 年費
times = 0
features = x.find_all("div",{
		"class" : "card-features"
	})
pay = x.find_all("ul",{
		"class" : "bullet-normal"
	})
# print(pay)
for j in features:
	##特色部分
	featuresTEXT = features[times].find("ul",{
			"class" : "bullet gray-medium"
		})
	featuresTEXT = str(featuresTEXT).replace("<li>", "")
	featuresTEXT = str(featuresTEXT).replace("</li>", "")
	featuresTEXT = str(featuresTEXT).replace("<ul class=\"bullet gray-medium\">", "")
	featuresTEXT = str(featuresTEXT).replace("</ul>", "")
	featuresTEXT = str(featuresTEXT).replace(" ", "")
	featuresTEXT = str(featuresTEXT).replace("\n", "")
	featuresTEXT = str(featuresTEXT).replace("None", "")
	times += 1
	print(featuresTEXT)
	##年費部分
	# payTEXT = pay[times].text
	# times += 1
	# print(payTEXT)
