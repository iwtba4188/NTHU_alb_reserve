import sys
import json
import datetime
import time
import asyncio

from colorama import init, Fore, Style

import requests
from bs4 import BeautifulSoup

from L_util import crawling_PHPSESSID, log, get_server_time


loop = asyncio.get_event_loop()


async def post_reservation(url, headers, json):
    # response = await requests.post(url=url, headers=headers, json=json)
    time.sleep(1)
    response = await loop.run_in_executor(None, lambda: requests.post(url=url, headers=headers, json=json))

    html_data = BeautifulSoup(response.text, "html.parser")

    if response.status_code == 200 and str(html_data) == "ok":
        log(f"reserved {json} {Fore.GREEN+Style.BRIGHT}successfully{Fore.RESET+Style.RESET_ALL},"
            f"see more detail in nthualb website.")
    elif str(html_data) is None:
        log(f"reserved {json} {Fore.RED+Style.BRIGHT}FAIL{Fore.RESET+Style.RESET_ALL}."
            f"Because {Fore.RED+Style.BRIGHT}the session isn't work "
            f"(i.e. you didn't login successfully){Fore.RESET+Style.RESET_ALL}.")
    else:
        log(f"reserved {json} {Fore.RED+Style.BRIGHT}FAIL{Fore.RESET+Style.RESET_ALL}."
            f"Because {Fore.RED+Style.BRIGHT}{html_data}{Fore.RESET+Style.RESET_ALL}.")


def main():
    DEBUG = False

    init(convert=True)  # colorama init

    TODAY = (
        int(datetime.datetime.now().strftime("%Y")),
        int(datetime.datetime.now().strftime("%m")),
        int(datetime.datetime.now().strftime("%d")))

    RESERVE_TIME = datetime.datetime(year=TODAY[0], month=TODAY[1], day=TODAY[2]) \
        + datetime.timedelta(days=5 if not DEBUG else 4)

    TOMORROW_TIME = datetime.datetime(year=TODAY[0], month=TODAY[1], day=TODAY[2])\
        + datetime.timedelta(days=1)

    RESERVE_TIME = str(int(RESERVE_TIME.timestamp()))

    URL = "https://nthualb.url.tw/reservation/api/reserve_field"

    try:
        with open("headers.json") as headers_file:
            raw_header = json.load(headers_file)
            post_header = raw_header["post_header"]
            get_header = raw_header["get_header"]
    except FileNotFoundError:
        sys.stderr.write(
            "\"header.json\" not found, please add it and try again.\n")
    except Exception as err:
        sys.stderr.write(f"Unexpected Error. \nErr: {err}\n")

    try:
        with open("settings.json") as setting_file:
            setting = json.load(setting_file)
    except FileNotFoundError:
        sys.stderr.write(
            "\"setting.json\" not found, please add it and try again.\n")
    except Exception as err:
        sys.stderr.write(f"Unexpected Error. \nErr: {err}\n")

    try:
        ID = setting["id"] + '\t'
        PASSWORD = setting["password"]

        PHPSESSID = crawling_PHPSESSID(ID, PASSWORD)
        # PHPSESSID = ""

        TIME1 = int(setting["time1"])-1
        FIELD1 = int(setting["field1"])-1
        TIME2 = int(setting["time2"])-1
        FIELD2 = int(setting["field2"])-1

        post_header["cookie"] = "PHPSESSID=" + str(PHPSESSID)
        get_header["cookie"] = "PHPSESSID=" + str(PHPSESSID)
    except ValueError as err:
        sys.stderr.write(
            f"setting format is wrong, please check and try again.\nError: {err}\n")
    except Exception as err:
        sys.stderr.write(f"Unexpected Error. \nErr: {err}\n")

    log("get server time")
    SERVER_TIME = get_server_time(URL=URL, get_header=get_header)
    NEED_TO_WAIT = int(TOMORROW_TIME.timestamp()) - \
        int(SERVER_TIME.timestamp())

    tasks = []
    for info in [(TIME1, FIELD1), (TIME2, FIELD2)]:
        post_header["content-length"] = f"{42+len(str(info[0]))+len(str(info[1]))}"

        data = {
            "time": str(info[0]),
            "field": str(info[1]),
            "date": RESERVE_TIME
        }

        log(f"start reserving {data}")
        log("sending POST request")
        # raw_data = requests.post(url=URL, headers=post_header, json=data)
        for _ in range(5):
            tasks.append(loop.create_task(
                post_reservation(URL, post_header, data)))

    if not DEBUG:
        log(f"time of the server is {SERVER_TIME}")
        log(f"waiting for next day, sleep {NEED_TO_WAIT}+1 secs")
        time.sleep(NEED_TO_WAIT+1)

    loop.run_until_complete(asyncio.wait(tasks))

    log(f"{Style.BRIGHT}FIN{Style.RESET_ALL}")
    input("Input any value to exit...")


if __name__ == "__main__":
    main()
