# -*- coding: utf-8 -*-

import urllib.request

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from user import user
from crawler import *
from output import *
SLACK_TOKEN = "xoxb-677120743489-689663400837-IA7Z92mejXsjLBgbMuRsJH4Y"
SLACK_SIGNING_SECRET = "3e18b519376ca1b60fad0e7258f77db3"

app = Flask(__name__)

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)
online_User_list = []
@slack_events_adaptor.on("group_joined")
def group_joined_(event_data):
    if event_data["event"]["user"] in online_User_list:
        for i in online_User_list:
            online_User_list.remove(i)


@slack_events_adaptor.on("group_left")
def group_left_(event_data):
    if event_data["event"]["user"] in online_User_list:
        for i in online_User_list:
            online_User_list.remove(i)


@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]
    global online_User_list
    _text =""
    if event_data["event"]["user"] in online_User_list:
        for i in online_User_list:
            if i.token == event_data["event"]["user"]:
                if i.getstate() == 1:
                    i.setstate(2)
                    _text = "이 아이디가 맞습까??(YES / NO)"

                elif i.getstate() == 2:
                    if event_data["event"]["text"] == "YES":
                        i.getstate = 3
                        _text = "알고리즘 분류 선택" + " ".join(crawlProblem())
                    elif event_data["event"]["text"] == "NO":
                        i.getstate = 1

                elif i.getstate() == 3:
                    _text = " ".join(send_problem(event_data["event"]["text"],i.token))
                    i.setstate(4)
                    _text += "\n" + "다른 문제를 원하시면 다른 문제, 분류로 돌아가고 싶으시면 분류라고 해주세요."

                elif i.getstate() == 4:
                    if event_data["event"]["text"] == "다른 문제":
                        _text = " ".join(send_problem(event_data["event"]["text"], i.token))
                    elif event_data["event"]["text"] == "분류":
                        i.getstate(3)
                        _text = "알고리즘 분류 선택" + " ".join(crawlProblem())
    else:
        if event_data["event"]["text"] == "hi bixby!":
            temp = user(event_data["event"]["user"])
            online_User_list += temp.copy()
            if user.isExistUser(temp.token):
                user.setstate(3)
                _text = "알고리즘 분류 선택" + " ".join(crawlProblem)
            else:
                _text = "백준 알고리즘 아이디를 입력하세요."
                user.setid()
                user.setstate(1)
        else:
            _text = "저를 호출하시려면 hi bixby! 라고 해주세요!"
    # channel = event_data["event"]["channel"]
    # text = event_data["event"]["text"]
    #
    # if text=="www.naver.com":
    # keywords = _crawl_naver_keywords(text)
    slack_web_client.chat_postMessage(
        channel=event_data["event"]["channel"],
        text=_text
    )


def start_server():
    app.run('0.0.0.0', port=5000)


if __name__ == "__main__":
    start_server()
