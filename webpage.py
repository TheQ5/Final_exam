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
	content = LTS(sys.argv[1:7])
	content = content.replace('[',"").replace("]","").replace(" ","")
	content = content.split(",")
	idd = []
	questions = []
	answers = []
	for I in content[0:3]:
		# I, Q = sys.argv[1],sys.argv[] 
		idd.append(I)
	for Q in content[3:6]:
		questions.append(Q)
	for i in idd:
		answers.append(ans(i))



	df = pd.DataFrame({
	    '可能的問題                 ': questions, 
	    '可能的答案                 ': answers  ###用[]取答案
	})
	df

	if st.button('send A1'):
		PushMessage(answers[0])
		st.write(answers[0])

	if st.button('send A2'):
		PushMessage(answers[1])
		st.write(answers[1])

	if st.button('send A3'):
		PushMessage(answers[2])
		st.write(answers[2])

if __name__ == "__main__":
	main()


#"last update:2019/11/8"