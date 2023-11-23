import datetime
import json
import logging
import time

import requests
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as edgeOptions
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager

init(convert=True)  # colorama init

NOW_TIME = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
DEBUG = False
logging.basicConfig(
    filename=f"{str(NOW_TIME)}.log", encoding="utf-8", level=logging.INFO
)


def log(log_message, time_limit=False):
    if time_limit:
        time.sleep(0.1)
    now_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logging.info(f"[Log: {now_time}] {log_message}")

    return


async def crawling_PHPSESSID(ID, PASSWORD):
    log("open the webdriver")
    log("setting options (NTHU_OAuth_Decaptcha.crx)")
    edge_options = edgeOptions()
    if not DEBUG:
        edge_options.add_argument("--headless")
        edge_options.add_argument("--disable-gpu")
    edge_options.add_extension("NTHU_OAuth_Decaptcha.crx")
    nthualb = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager().install()), options=edge_options
    )

    log("set implicitly waitting time as 10 secs")
    nthualb.implicitly_wait(10)
    log("enter the website to login")
    nthualb.get(
        "https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?client_id=nthualb&response_type=code"
    )

    log("waiting for website done")
    WebDriverWait(nthualb, 10).until(EC.presence_of_element_located((By.ID, "id")))
    log("waiting for the extension work (5 secs)")
    time.sleep(5)
    log("get account_blank")
    account_blank = nthualb.find_element(By.ID, "id")
    log("send account_blank")
    account_blank.send_keys(ID + "\t" + PASSWORD)

    log("get login_button")
    login_button = nthualb.find_element(By.CLASS_NAME, "btn-login")
    log("click login_button")
    login_button.click()

    log("enter the website to last day")
    try:
        nthualb.get("https://nthualb.url.tw/reservation/reservation?d=4")
    except UnexpectedAlertPresentException:
        nthualb.switch_to.alert.accept()
        nthualb.get("https://nthualb.url.tw/reservation/reservation?d=4")
    except Exception as e:
        log(f"{Fore.RED+Style.BRIGHT}未知錯誤：{e}{Fore.RESET+Style.RESET_ALL}")
        return None

    if str(nthualb.page_source).find("預約") == -1:
        log(f"{Fore.RED+Style.BRIGHT}登入失敗，請檢查登入資料是否正確。{Fore.RESET+Style.RESET_ALL}")
        return None
    else:
        log(f"{Fore.GREEN+Style.BRIGHT}登入成功。{Fore.RESET+Style.RESET_ALL}")

    PHPSESSID = nthualb.get_cookie("PHPSESSID")

    log(f"get PHPSESSION = {PHPSESSID['value']}")
    log("close driver")
    nthualb.close()

    return PHPSESSID["value"]


def get_headers():
    with open("headers.json") as headers_file:
        raw_header = json.load(headers_file)
    return raw_header


def get_server_time(session: str):
    url = "https://nthualb.url.tw/reservation/api/reserve_field"
    headers = get_headers()["get_header"]
    headers["cookie"] = f"PHPSESSID={session}"

    get_response = requests.get(url=url, headers=get_headers()["get_header"])

    raw_server_date = str(get_response.headers["date"])
    server_time = datetime.datetime.strptime(
        raw_server_date, "%a, %d %b %Y %H:%M:%S %Z"
    ) + datetime.timedelta(hours=8)
    server_time = server_time.strftime("%Y-%m-%d %H:%M:%S")

    return server_time
