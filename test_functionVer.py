#!/usr/bin/env python
# coding: utf-8

# In[10]:


# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 
from linebot.exceptions import (
    InvalidSignatureError
)

# 將消息模型，文字收取消息與文字寄發消息 引入
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, AudioMessage
)

# 載入設定檔

import json
secretFileContentJson=json.load(open("./line_secret_key",'r'))
server_url=secretFileContentJson.get("server_url")


# 設定Server啟用細節
app = Flask(__name__,static_url_path = "/images" , static_folder = "./images/" )

# 生成實體物件
line_bot_api = LineBotApi(secretFileContentJson.get("channel_access_token"))
handler = WebhookHandler(secretFileContentJson.get("secret_key"))

# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# In[11]:


# 載入Follow事件
from linebot.models.events import (
    FollowEvent
)

# 載入requests套件
import requests


# 告知handler，如果收到FollowEvent，則做下面的方法處理
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
        
     # 將用戶資訊存在檔案內
    with open("./users.txt", "a") as myfile:
        myfile.write(json.dumps(vars(user_profile),sort_keys=True))
        myfile.write('\r\n')
        
        
#     # 將菜單綁定在用戶身上
#     linkRichMenuId=secretFileContentJson.get("rich_menu_id")
#     linkResult=line_bot_api.link_rich_menu_to_user(secretFileContentJson["self_user_id"], linkRichMenuId)
    
#     # 回覆文字消息與圖片消息
#     line_bot_api.reply_message(
#         event.reply_token,
#         reply_message_list
#     )


# In[12]:



def PushMessage(context, user_ID):
    #推播消息
    from linebot import LineBotApi
    from linebot.models import TextSendMessage
    from linebot.exceptions import LineBotApiError

    token = "AhuuqOghydZqwlCbgOHo/JJxADgxz3begLh9bzoK7nCja4ipotAl9pnKi5YAX+1eip/O65jb+4J7kdsOcVf4lViTf/RJiKymXsctgk0gS9WhD8KeNtn1WRgICzk8I3a2oQpDWx4fXcNZfcsPA1chUgdB04t89/1O/w1cDnyilFU="

    line_bot_api = LineBotApi(token)

    # try:
    line_bot_api.push_message(user_ID, TextSendMessage(text=context))
    # except LineBotApiError as e:
    #     print("error handle")


# In[13]:


from aip import AipSpeech
import json
import time
import os
import wave
from pydub import AudioSegment
from bert_sentimentAnalysis_predict import *  ## * 很重要,pip install才可以直接import 自製的py檔要加*
from Voice2Text import *
from find_similar_question import *
from webpage import *


# In[5]:


@handler.add(MessageEvent, message=AudioMessage)
def handle_message(event):
    #取出用戶ID
    user_ID = line_bot_api.get_profile(event.source.user_id)
    user_ID = user_ID.user_id
    print(user_ID)
    #接收資料,回傳一段訊息給用戶,並將資料取回本機
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='沒事亂傳訊息，害我又要加班'))
    message_content = line_bot_api.get_message_content(event.message.id)
    with open('./audios/'+event.message.id+".aac", 'wb') as fd: ###LINE預設音檔是.aac
        for chunk in message_content.iter_content():
            fd.write(chunk)
    #####先轉檔#####
    aacPath = "./audios/"+event.message.id+".aac"
    convert_aac_to_wav(aacPath)
    
    #####這邊要加入語音轉文字#####
    wavPath = "audios"+event.message.id+".wav"
    text = voice_to_txt(wavPath)
    
    #####接著情感分析#####
    sign, content = sentimentModel().predict_and_to_pass_sign(text) ###有class的話，要class().function()才能使用　
    
    #####根據用戶心情分流#####
    if sign==0 or sign==1:
        PredictQue = find_similiar_questions(text, "qa_collections.csv") ###要記得先開伺服器###
        print(PredictQue)
    #####接到客服頁面#####    
        os.system("Streamlit run webpage.py %s"%PredictQue)
        print("完成了")
    elif sign==2:
        PushMessage(content)
    else:
        PushMessage(content)


# In[8]:


user_ID = "Ubbe1a0ecaf2b210fd618c919d1d19870"


# In[9]:


if __name__ == "__main__":
    app.run(host='0.0.0.0')


# # TO DO LIST
# 
# ## 即時取得用戶的ID 讓chatbot可以推播給任意用戶
# 
# ## 創建新的ChatBot 頻道
# 
# ## 開頭問候語、美化介面、圖文選單(help跟麥克風)
# 
# ## 包成Docker放到GCP
