import os
import requests
import json
from bs4 import BeautifulSoup

feature = []
Introduction = []
offer = []
attention = []

#先把土地銀行的所有卡種找出來
p = requests.get(
		"https://www.landbank.com.tw/Category/Items/銀行卡"
	)
p.encoding = "utf-8"
x = BeautifulSoup(p.text , "html.parser")

a1 = x.find("div",{
	"class" : "contect_credit_card"
	})

a2 = a1.find_all("div",{
	"class" : "credit_card_in"
	})

#輪流進到每個卡種裡拿出資訊
for url in a2:
	a3 = url.find("a").attrs["href"]

	p2 = requests.get(
			"https://www.landbank.com.tw" + a3
		)
	p2.encoding = "utf-8"
	x2 = BeautifulSoup(p2.text , "html.parser")

	# #第一步 卡片特色
	a4 = x2.find("div",{
		    	"class" : "contect_in_item"
		    })
	# print(a4)
	if a4.find("p") != None:
		a5 = a4.find("p").text
		print("我是狀況1")

	elif a4.find("ul") != None:
		a5 = a4.find("ul").text
		print("我是狀況2")

	elif a4.find("strong") != None:
		a5 = a4.find("strong").text
		print("我是狀況3")

	feature.append(a5)
print(feature)

	#第二步 卡片介紹
	# a4_2 = x2.find("div",{
	# 	    	"class" : "in_item_paddingleft"
	# 	    })
	# a5_2 = a4_2.find("p").text + a4_2.find("ul").text
	# print(a5_2)

# Location = i.find("a").text






#把資料存成檔案