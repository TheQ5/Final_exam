import streamlit as st
import pandas as pd
import numpy as np
import csv
import sys
from test_functionVer import *

#接收分析後的兩個值得字串:[id, question]*3,透過ID去CSV找Answer


def LTS(s):  
    
    # initialize an empty string 
    str1 = " " 
    # return string   
    return (str1.join(s)) 

def ans(id):
	# get answer with id 
	# 開啟 CSV 檔案
	with open('qa_collections.csv', newline='', encoding = "utf-8") as csvfile:
	# 讀取 CSV 檔案內容
		rows = csv.reader(csvfile)
		for row in rows :
			if str(id) == row[0]:
				return row[2]

def main():
	st.title('課服語音輔助系統')
	st.write("Here's the input from the customers and the most possible solution from the database:")
	
	#將傳進來的資料作處理
	content = LTS(sys.argv[1:7])#list to string
	content = content.replace('[',"").replace("]","").replace(" ","")#去除多餘符號
	content = content.split(",")
	user_ID = LTS(sys.argv[7])
	user_ID = user_ID.replace('[',"").replace("]","").replace(" ","").replace("\'","")
	idd = []
	questions = []
	answers = []
	for I in content[0:3]:#取ID
		idd.append(I)
	for Q in content[3:6]:#取Q
		questions.append(Q)
	for i in idd:#取答案
		answers.append(ans(i))

	#實際資料顯示
	group = ["一", "二", "三"]
	number = 0
	answer_number = 1
	for i in group:
		st.success("第%s組Q&A"%i)
		st.write("問題:", questions[number])

		st.write("回答:", answers[number])
	
		if st.button('將第 %s 個答案推送給客戶'%answer_number):
			PushMessage(answers[number], user_ID)
			st.write("已將答案%s傳送給用戶"%answer_number)
		number += 1
		answer_number += 1


if __name__ == "__main__":
	main()


#"last update:2019/11/8"