# -*- coding: utf-8 -*-

from linepy import *
from akad.ttypes import Message
from akad.ttypes import ContentType as Type
from liff.ttypes import LiffChatContext, LiffContext, LiffSquareChatContext, LiffNoneContext, LiffViewRequest
from datetime import datetime, timedelta
from time import sleep
from bs4 import BeautifulSoup
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse, traceback

mac  = "DESKTOPMAC\t5.8.0\tFGM-BOTS-SERVICE\t11.2.5"
win  = "DESKTOPWIN\t5.8.0\tFGM-BOTS-SERVICE\t11.2.5"
chrm = "CHROMEOS\t2.1.5\tFGM-BOTS-SERVICE\t11.2.5"
ipd  = "IOSIPAD\t8.11.0\tFGM-BOTS-SERVICE\t11.2.5"

client = LINE("AUTHTOKEN", appName=mac)
client.log("Auth Token : " + str(client.authToken))
channelToken = client.getChannelResult()
client.log("Channel Token : " + str(channelToken))
clientMid = client.profile.mid
clientStart = time.time()
clientPoll = OEPoll(client)
responlimit = []
responlimit1 = []
responlimit2 = []
responlimit3 = []
responlimit4 = []
responlimit5 = []
responlimit6 = []

def restartBot():
    print ("[ INFO ] BOT RESETTED")
    python = sys.executable
    os.execl(python, python, *sys.argv)

def autoRestart():
    while True:
        try:
            time.sleep(21600)
            restartBot()
        except:
            pass
thread21 = threading.Thread(target=autoRestart)
thread21.daemon = True
thread21.start()

def delreslimit():
    while True:
        try:
            time.sleep(2)
            del responlimit[:]
            del responlimit1[:]
            del responlimit2[:]
            del responlimit3[:]
            del responlimit4[:]
            del responlimit5[:]
            del responlimit6[:]
        except:
            pass
thread211 = threading.Thread(target=delreslimit)
thread211.daemon = True
thread211.start()

def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))

def timeChange(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours,24)
    weeks, days = divmod(days,7)
    months, weeks = divmod(weeks,4)
    text = ""
    if months != 0: text += "%02d Bulan" % (months)
    if weeks != 0: text += " %02d Minggu" % (weeks)
    if days != 0: text += " %02d Hari" % (days)
    if hours !=  0: text +=  " %02d Jam" % (hours)
    if mins != 0: text += " %02d Menit" % (mins)
    if secs != 0: text += " %02d Detik" % (secs)
    if text[0] == " ":
        text = text[1:]
    return text

def command(text):
    pesan = text.lower()
    if settings["setKey"] == True:
        if pesan.startswith(settings["keyCommand"]):
            cmd = pesan.replace(settings["keyCommand"],"")
        else:
            cmd = "Undefined command"
    else:
        cmd = text.lower()
    return cmd
#==========================
def testFlex():
    data = {
        "type": "flex",
        "altText": "Flex Message",
        "contents": {
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Header",
                        "align": "center"
                    }
                ]
            },
            "styles": {
                "header": {
                    "backgroundColor": "#0EF2D6"
                }
            }
        }
    }
    return data


def sendLiff(to, data):
    xyz = LiffChatContext(to)
    xyzz = LiffContext(chat=xyz)
    view = LiffViewRequest('1602687308-GXq4Vvk9', xyzz)
    token = client.liff.issueLiffView(view)
    url = 'https://api.line.me/message/v3/share'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % token.accessToken
    }
    data = {"messages":[data]}
    requests.post(url, headers=headers, data=json.dumps(data))

def clientBot(op):
    if op.type == 0:
        return
    if op.type == 26 and op.message._from not in responlimit:
            msg = op.message
            cmd = str(msg.text.lower())
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                if msg.toType == 0:
                    if sender != client.profile.mid:
                        to = sender
                    else:
                        to = receiver
                elif msg.toType == 1:
                    to = receiver
                elif msg.toType == 2:
                    to = receiver
            if msg.contentType == 0:
                if cmd is None:
                    return
                elif cmd == 'flex':
                    data = testFlex()
                    sendLiff(to, data)
            responlimit.append(sender)

def run():
    while True:
        ops = clientPoll.singleTrace(count=50)
        if ops != None:
            for op in ops:
                try:
                    clientBot(op)
                except Exception as error:
                    logError(error)
                clientPoll.setRevision(op.revision)

if __name__ == "__main__":
    run()