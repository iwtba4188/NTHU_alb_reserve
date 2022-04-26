import sys
import json
import datetime

from bs4 import BeautifulSoup
import requests

from L_util import *


TODAY = (
    int(datetime.datetime.now().strftime("%Y")),
    int(datetime.datetime.now().strftime("%m")),
    int(datetime.datetime.now().strftime("%d")))
RESERVE_TIME = datetime.datetime(year=TODAY[0], month=TODAY[1], day=TODAY[2])+datetime.timedelta(days=5)
TOMORROW_TIME = datetime.datetime(year=TODAY[0], month=TODAY[1], day=TODAY[2])+datetime.timedelta(days=1)
RESERVE_TIME = str(int(RESERVE_TIME.timestamp()))

try:
    with open("headers.json") as headers_file:
        raw_header = json.load(headers_file)
        post_header = raw_header["post_header"]
        get_header = raw_header["get_header"]
except FileNotFoundError:
    sys.stderr.write("\"header.json\" not found, please add it and try again.")
except Exception as err:
    sys.stderr.write(f"Unexpected Error. \nErr: {err}\n")

try:
    with open("settings.json") as setting_file:
        setting = json.load(setting_file)
except FileNotFoundError:
    sys.stderr.write("\"header.json\" not found, please add it and try again.\n")
except Exception as err:
    sys.stderr.write(f"Unexpected Error. \nErr: {err}\n")

try:
    ID = setting["id"] + '\t'
    PASSWORD = setting["password"]

    PHPSESSID = crawling_PHPSESSID(ID, PASSWORD)

    TIME1 = int(setting["time1"])-1
    FIELD1 = int(setting["field1"])-1
    TIME2 = int(setting["time2"])-1
    FIELD2 = int(setting["field2"])-1

    post_header["cookie"] = "PHPSESSID=" + str(PHPSESSID)
    get_header["cookie"] = "PHPSESSID=" + str(PHPSESSID)
except ValueError as err:
    sys.stderr.write(f"setting format is wrong, please check and try again.\nError: {err}\n")
except Exception as err:
    sys.stderr.write(f"Unexpected Error. \nErr: {err}\n")


url = "https://nthualb.url.tw/reservation/api/reserve_field"

log("get server time")
get_respond = requests.get(url=url, headers=get_header)
raw_server_date = str(get_respond.headers["date"])
SERVER_TIME = datetime.datetime.strptime(raw_server_date, "%a, %d %b %Y %H:%M:%S %Z") + datetime.timedelta(hours=8)
NEED_TO_WAIT = int(TOMORROW_TIME.timestamp()) - int(SERVER_TIME.timestamp())

log(f"time of the server is {SERVER_TIME}")
log(f"waiting for next day, sleep {NEED_TO_WAIT}+3 secs")
time.sleep(NEED_TO_WAIT+3)

for info in [(TIME1, FIELD1), (TIME2, FIELD2)]:
    post_header["content-length"] = f'{42+len(str(info[0]))+len(str(info[1]))}'

    data = {
        "time": str(info[0]),
        "field": str(info[1]),
        "date": RESERVE_TIME
    }

    log(f"start reserving {data}")
    log("sending POST request")
    raw_data = requests.post(url=url, headers=post_header, json=data)
    html_data = BeautifulSoup(raw_data.text, "html.parser")

    if raw_data.status_code == 200 and html_data == "ok":
        log(f"reserved {data} successfully, see more detail in nthualb website")
    else:
        log(f"reserved {data} FAIL. Because {html_data}")
