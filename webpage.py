import streamlit as st
import pandas as pd
import numpy as np
import csv
import sys

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

	# print(questions)
	# print(answers)
	# print(len(questions))
	# print(len(answers))
	# print(LTS(sys.argv[1:7]))

	df = pd.DataFrame({
	    '可能的問題                 ': questions, 
	    '可能的答案                 ': answers  ###用[]取答案
	})
	df

	if st.button('send A1'):
		st.write('send A2')

	if st.button('send A2'):
		st.write('send A2')

	if st.button('send A3'):
		st.write('send A3')

if __name__ == "__main__":
    main()




