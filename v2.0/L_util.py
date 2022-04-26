import time
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions


def log(log_message, time_limit=False):
    if time_limit:
        time.sleep(0.1)
    now_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"[Log: {now_time}] {log_message}")

    return


def crawling_PHPSESSID(ID, PASSWORD):
    log("open the webdriver")
    log("setting options (NTHU_OAuth_Decaptcha.crx)")
    chrome_options = ChromeOptions()
    chrome_options.add_extension("NTHU_OAuth_Decaptcha.crx")
    nthualb = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    log("set implicitly waitting time as 10 secs")
    nthualb.implicitly_wait(10)
    log("enter the website to login")
    nthualb.get("https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?client_id=nthualb&response_type=code")

    log("waiting for website done")
    WebDriverWait(nthualb, 10).until(EC.presence_of_element_located((By.ID, "id")))
    log("waiting for the extension work (5 secs)")
    time.sleep(5)
    log("get account_blank")
    account_blank = nthualb.find_element_by_id("id")
    log("send account_blank")
    account_blank.send_keys(ID + PASSWORD)

    log("get login_button")
    login_button = nthualb.find_element_by_class_name("btn-login")
    log("click login_button")
    login_button.click()

    log("enter the website to last day")
    nthualb.get("https://nthualb.url.tw/reservation/reservation?d=4")

    PHPSESSID = nthualb.get_cookie("PHPSESSID")
    print(PHPSESSID["value"])

    return PHPSESSID["value"]
