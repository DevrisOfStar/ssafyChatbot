# -*- coding: utf-8 -*-
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from copy import deepcopy
from user import *
from output import *

SLACK_TOKEN = "xoxb-677120743489-689663400837-IA7Z92mejXsjLBgbMuRsJH4Y"
SLACK_SIGNING_SECRET = "3e18b519376ca1b60fad0e7258f77db3"

app = Flask(__name__)

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)
online_User_list = []

Time_Table_List = []

@slack_events_adaptor.on("group_left")
def group_left_(event_data):
    if event_data["event"]["user"] in online_User_list:
        for i in online_User_list:
            online_User_list.remove(i)


@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    global Time_Table_List
    channel = event_data["event"]["channel"]
    if event_data["event"]["event_ts"] in Time_Table_List:
        return
    else:
        Time_Table_List.append(event_data["event"]["event_ts"])
    for i in range(len(event_data["event"]["text"])):
        if event_data["event"]["text"][i] == ">":
            text = event_data["event"]["text"][i+2:]
            break
    global online_User_list
    _text =""
    flag = 0
    for user__ in online_User_list:
        if event_data["event"]["user"] == user__.token:
            flag=1
    if flag==1:
        for i in online_User_list:
            if i.token == event_data["event"]["user"]:
                if i.getstate() == 1:
                    i.user_id = text
                    i.register(text)
                    i.setstate(2)
                    _text = "이 아이디가 맞습까??(YES / NO)"

                elif i.getstate() == 2:
                    if text == "YES":
                        i.setstate(3)
                        _text = "알고리즘 분류 선택" + " ".join(getclassifylist())
                    elif text == "NO":
                        i.setstate(1)
                        _text = "아이디를 입력해 주세요."
                    else:
                        _text = "이 아이디가 맞습까??(YES / NO)"
                elif i.getstate() == 3:
                    if text in getclassifylist():
                        problem = send_problem(text, i.token)
                        for j in range(len(problem)):
                            _text += "\n문제 번호 : "+str(problem[j].get("number"))+"\n문제 이름 : "+\
                                    str(problem[j].get("subject"))+"\n정답자 / 제출자 : "+ str(problem[j].get(
                                "cor"))+"/"+str(problem[j].get("total")) +"\n링크 : "+ \
                                    str(problem[j].get("link"))+"\n"
                        i.setstate(4)
                        _text += "\n" + "다른 문제를 원하시면 다른 문제, 분류로 돌아가고 싶으시면 분류라고 해주세요."
                        i.tempString = text
                    else:
                        _text = "정확한 종류를 입력해 주세요."

                elif i.getstate() == 4:
                    if text == "다른 문제":
                        problem = send_problem(i.tempString, i.token)
                        for j in range(len(problem)):
                            _text += "\n문제 번호 : " + str(problem[j].get("number")) + "\n문제 이름 : " + \
                                    str(problem[j].get("subject")) + "\n정답자 / 제출자 : " + str(problem[j].get(
                                "cor")) + "/" + str(problem[j].get("total")) + "\n링크 : " + \
                                    str(problem[j].get("link")) + "\n"
                    elif text == "분류":
                        i.setstate(3)
                        _text = "알고리즘 분류 선택\n" + "\n".join(getclassifylist())
                    else:
                        _text = "정확한 명령어를 입력해 주세요."
    else:
        if text == "hi bixby!":
            temp = USER(event_data["event"]["user"])
            online_User_list.append(temp)
            if temp.isExistUser(temp.token):
                temp.setstate(3)
                _text = "알고리즘 분류 선택\n" + "\n".join(getclassifylist())
            else:
                _text = "백준 알고리즘 아이디를 입력하세요."
                temp.setstate(1)
        else:
            _text = "저를 호출하시려면 hi bixby! 라고 해주세요!"
    slack_web_client.chat_postMessage(
        channel=event_data["event"]["channel"],
        text=_text
    )
    Time_Table_List.remove(event_data["event"]["event_ts"])


def start_server():
    app.run('0.0.0.0', port=5000)


if __name__ == "__main__":
    start_server()
