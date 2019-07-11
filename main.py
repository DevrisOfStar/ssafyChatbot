# -*- coding: utf-8 -*-
import urllib.request

from bs4 import BeautifulSoup

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

SLACK_TOKEN = "xoxb-677120743489-689663400837-IA7Z92mejXsjLBgbMuRsJH4Y"
SLACK_SIGNING_SECRET = "3e18b519376ca1b60fad0e7258f77db3"

app = Flask(__name__)

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)


@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]

    if text=="www.naver.com":
        keywords = _crawl_naver_keywords(text)
        slack_web_client.chat_postMessage(
            channel=channel,
            text=keywords
        )



def start_server():
    app.run('0.0.0.0', port=5000)


if __name__ == "__main__":
    start_server()