# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 18:59:40 2019

@author: Hui
"""

import os.path
import sys
import json
import itchat, time
from itchat.content import *
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
itchat.auto_login(hotReload=True)                                              #此处调出微信登录二维码
CLIENT_ACCESS_TOKEN = '21a09122640240cabb6d2c05c6d380f4'
itchat.send('Hi', toUserName='filehelper')

#define ai robot                                                           #此处函数调用谷歌的 dialogflow做自动回复，需要对方id区分对象和对方语句，输出是回答
def ai_reply(nameid, message): 
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'zh-cn'  # optional, default value equal 'en'
    request.session_id = nameid
    message=message.replace('@', '')
    request.query = message
    response = request.getresponse()
    s=json.loads(response.read(), encoding='UTF-8')
    return s['result']['fulfillment']['speech']


@itchat.msg_register(itchat.content.TEXT, isGroupChat=False)
def tuling_reply(msg):
    print(msg['Text'])
    reply=ai_reply(msg['FromUserName'], msg['Text'])
    itchat.send(reply, toUserName=msg['FromUserName'])
    itchat.send(reply, toUserName='filehelper')
    print(reply)
    
@itchat.msg_register(itchat.content.TEXT,isGroupChat=True) #是否群聊信息， 群聊中功能一直不太对，没法回复对方
def get_reply(msg):
    itchat.get_chatrooms(update=True)                       #更新群信息，总是出错
    if '藕花深处' in msg['Text']:                                #此处检测作业关键词，发到我的账号并且回复，但是一直没法回复
        itchat.send(msg['Text'], toUserName='filehelper')
        print(msg['Text'])
        itchat.send('点赞', toUserName=msg['ActualNickName'])
    if msg['isAt']:
        #print(msg['IsAt'])                                           #此处检测我是否被@，True是被@
        print(msg['ActualNickName'])                                   #@我的人
        print(msg['Text'])
        reply=ai_reply(msg['ActualNickName'], msg['Text'])
        itchat.send(reply, toUserName=msg['ActualNickName'])
       

    

itchat.run()

