#!/usr/bin/env python
import os
import threading
import schedule
from bs4 import BeautifulSoup
import requests
import time
import json

def log(msg):
    global log_msg
    print(msg)
    now = time.strftime("%m/%d %a, %H:%M:%S | ", time.localtime())
    log_msg.append(now + msg)

def task():
    global error_times,code
    if error_times >= 3:
        log("Error times exceed 3, exit.")
        return(False)
    session_requests = requests.session()
    url = "https://app3.mingdao.edu.tw/traffic_b/action.php"

    data = {'hid1':'2',
            'txt1':'',
            'ck1':'否',
            'ck2':'是',
            'ck3':'是',
            'ck4':'否',
            'ck5':'否',
            'ck6':'否',
            'ck7':'是',
            'ck8':'否',
            'ck9':'是',
            'ck10':'否',
            'ck11':'否',
            'ck12':'否',
            'ck13':'否',
            'ck14':'否',
            'ck15':'否',
            'ck16':'否',
            'hid_caracc':'A090',
            'hid_study':'01V582',
            'okgo':'送出',
            }

    result = session_requests.post(url,data=data)
    html = BeautifulSoup(result.text, 'html.parser')
    code = html.find("p" ,style="margin:50px; text-align:center;").text.replace(" ","").replace("\n","")
    log("Website Response: " + code)
    if code != "操作成功。":
        error_times += 1
        print("Error, Retry in 5 seconds...")
        log(f"Unexpected response ({error_times})")
        time.sleep(5)
        task()
    else:
        log("Task finished.")

def run():
    global error_times,log_msg,code
    error_times = 0
    log_msg = []
    print("-----------------------------------")
    log("Start task.")
    with open('settings.json','r') as f:
        data = json.loads(f.read())
    if data["status"] == "off":
        log("AutoBUS ststus is off.")
        code = "AutoBUS ststus is off."
    else:
        task()
    with open('log.txt', 'a') as f:
        f.write(time.strftime("[ %m/%d %a ]", time.localtime()))
        f.write('\n')
        for line in log_msg:
            f.write(line)
            f.write('\n')
    print("Log saved.")
    print("-----------------------------------")
    print("")
    print("AutoBUS will run at 17:30 Thursday.")
    #Notify to Line
    token = 'lVk4U4xqG6aYVTO7NG4Rp9VhO4nDEzgInmNCFxu1jDi'
    headers = { "Authorization": "Bearer " + token }
    data = {'message': code}
    requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data)

def autorun():
    print("-----------------------------------")
    print("AutoBUS will run at 17:30 Thursday.")
    print('Total Thread:', threading.active_count())
    print("-----------------------------------")
    schedule.every().thursday.at("17:30").do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoBUS.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django."
        ) from exc
    execute_from_command_line(['main.py', 'runserver','0.0.0.0:8088', '--noreload'])

def threading_initialization():
    AutoBUS_thread = threading.Thread(
        target = autorun,
        name = 'AutoBUS'
        )
    AutoBUS_thread.start()

if __name__ == '__main__':
    threading_initialization()
    main()