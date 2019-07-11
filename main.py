# -*- coding: utf-8 -*-
import urllib.request

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from user import user
from crawler import *
SLACK_TOKEN = "xoxb-677120743489-689663400837-IA7Z92mejXsjLBgbMuRsJH4Y"
SLACK_SIGNING_SECRET = "3e18b519376ca1b60fad0e7258f77db3"

app = Flask(__name__)

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)
online_User_list = []

@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    global online_User_list
    if event_data["event"]["user"] in online_User_list:
        for i in online_User_list:
            if i.token == event_data["event"]["user"]:
                if i.getstate() == 1:
                    i.setstate(2)
    else:
        if event_data["event"]["text"] == "hi bixby!":
            temp = user(event_data["event"]["text"])
            online_User_list += temp.copy()
            if user.isExistUser(temp.token):
                user.setstate(3)
                text = "알고리즘 분류 선택" + " ".join(crawlProblem)

            else:
                text = "백준 알고리즘 아이디를 입력하세요."
                user.setstate(1)

    # channel = event_data["event"]["channel"]
    # text = event_data["event"]["text"]
    #
    # if text=="www.naver.com":
    #     keywords = _crawl_naver_keywords(text)
    #     slack_web_client.chat_postMessage(
    #         channel=channel,
    #         text=keywords
    #     )



def start_server():
    app.run('0.0.0.0', port=5000)


if __name__ == "__main__":
    start_server()