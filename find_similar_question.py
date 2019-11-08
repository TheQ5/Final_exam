#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bert_serving.client import BertClient
from sklearn.metrics.pairwise import cosine_similarity
from time import strftime, localtime
import numpy as np
import pandas as pd
import string
from zhon import hanzi as zh
import re


# In[ ]:


'''
載入問題答案集，對問題進行字串的處理，包含 去除標點符號 句子前後的空白 句子問的空白 0˜9的數字 
傳入參數: csv檔案的路徑（檔案格式: 編號 問題 答案）
這裡只用到 編號 問題 二個欄位
'''

def load_questions(file):
    
    dt_q = pd.read_csv(file, encoding="utf-8")
    ori_Questions = dt_q["問題"]
    question_idx = dt_q["編號"]
    
    exclude = set(string.punctuation + zh.punctuation)
    proc_q =[]
    for sentance in ori_Questions:
        a = ''.join(ch for ch in sentance if ch not in exclude)  # 去除標點符號
        b = a.strip()  # 去除一句話的前後空白
        b = ' '.join(a.split())  # 去除字串間的空白
        b = re.sub(r'\d+', '', b)  # 去除數字
        proc_q.append(b)
    return proc_q, question_idx


# In[ ]:


class Encode(object):

    def __init__(self):
        self.bc = BertClient(port=5555, port_out=5556)
        self.topk = 3
        self.doc_vecs = []
        self.Questions = []

    def encoding(self, qry):
        tensor = self.bc.encode(qry)
        return tensor

    def query_similarity(self, tensors):
        
        return cosine_similarity(tensors)
        
    '''
    依傳入的問題回傳最相似的三筆資料
    傳入參數: 問題，型態字串
    回傳參數: cosine距離分數, 符合的問題, 問題的編號，型態list
    '''

    def model_evaluate_by_question(self, query):
        # 取得問題的embedding
        qry_vecs = self.encoding([query])

        # 將問題與問題集的embedding合成一個array
        new_query = np.append(qry_vecs, self.doc_vecs, axis=0)

        # 計算問題之間的cosine距離
        similarity = self.query_similarity(new_query)

        # 第一個是自己(距離為1)，需排除，從第二個值開始看
        distance_np = similarity[0][1:]

        # 轉成DataFrame後，依cosine距離由大到小排序，數值愈接近1 表示愈相似 (餘絃相似度 cosine similarity)
        df = pd.DataFrame(self.Questions, columns=["Question"])
        df["Score"] = distance_np
        df["q_idx"] = df.index.tolist()
        df.sort_values(by="Score", ascending=False, inplace=True)

        # 取出top 5的問題，回傳 score, question
        most_match_score = []
        most_match_question = []
        most_match_qidx = []
        for i in range(self.topk):       
            most_match_question.append(df.iloc[i, 0])
            most_match_score.append(df.iloc[i, 1])
            most_match_qidx.append(df.iloc[i, 2])

        result = [most_match_qidx, most_match_question]
        return result


# In[ ]:


'''
起始Function
傳入參數:  qry 用戶問題，型態 字串
          qa_collections 問答集，型態 csv檔，範例 "DATA/CSV/Q_of_cc-fuban_taishin_esun_ctbc_with_idx.csv"
'''

def find_similiar_questions(qry, qa_collections): 

    ec = Encode()
    
    ec.Questions, q_idx = load_questions(qa_collections)
    
    # pre-encode
    
    print('Start precessing embedding at: ', strftime("%H:%M:%S", localtime()))
    ec.doc_vecs = ec.encoding(list(ec.Questions))
    print('Finished at: ', strftime("%H:%M:%S", localtime()))
    
    question_list = ec.model_evaluate_by_question(qry)
    
    return question_list
    


# In[ ]:



# 單次呼叫，使用範例

# test = find_similiar_questions("信用卡申請", "Q_of_cc-fuban_taishin_esun_ctbc_with_idx.csv")

# print(test)


#"last update:2019/11/8"

