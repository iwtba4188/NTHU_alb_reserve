from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

import datetime
import time
import os
import sys
import json


WAITING_TIME = 0.5
ENTER_DATE = datetime.datetime.now()
TOMORROW_DATE = (ENTER_DATE + datetime.timedelta(days=1)).strftime("%Y-%m-%d")


with open("setting.json", "r") as json_file:
    datas = json.load(json_file)
    ID = datas["id"] + '\t'
    PASSWORD = datas["password"]

    PLACE1 = int(datas["place1"])
    TIME1 = int(datas["time1"])+1
    PLACE2 = int(datas["place2"])
    TIME2 = int(datas["time2"])+1

    TARGET_DATE = datas["target_date"]
    DRIVER_TYPE = datas["driver_type"]  # Chrome or Edge


def log(log_message, time_limit=False):
    if time_limit:
        time.sleep(0.1)
    now_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(f"[Log: {now_time}] {log_message}")

    return


def crawling():
    log("open the webdriver")
    if (DRIVER_TYPE == "edge"):
        log("setting options (NTHU_OAuth_Decaptcha.crx)")
        edge_options = EdgeOptions()
        edge_options.add_extension("NTHU_OAuth_Decaptcha.crx")
        nthualb = webdriver.Edge(EdgeChromiumDriverManager().install(), options=edge_options)
    elif (DRIVER_TYPE == "chrome"):
        log("setting options (NTHU_OAuth_Decaptcha.crx)")
        chrome_options = ChromeOptions()
        chrome_options.add_extension("NTHU_OAuth_Decaptcha.crx")
        nthualb = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    else:
        sys.stderr.write("Unknow driver type")
        sys.exit(1)

    log("set implicitly waitting time as 10sec")
    nthualb.implicitly_wait(10)
    log("enter the website to login")
    nthualb.get("https://oauth.ccxp.nthu.edu.tw/v1.1/authorize.php?client_id=nthualb&response_type=code")

    log("waiting for website done")
    WebDriverWait(nthualb, 10).until(EC.presence_of_element_located((By.ID, "id")))
    log("waiting for the extension work (10 secs)")
    time.sleep(10)
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

    WebDriverWait(nthualb, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[1]/tbody/tr/td[5]/div[2]")))
    log("get last_date")
    last_date = nthualb.find_element_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[1]/tbody/tr/td[5]/div[2]").text

    log("waiting for 00:00")
    count = 0
    while (datetime.datetime.now().strftime("%Y-%m-%d") != TOMORROW_DATE):
        count += 1
        if (count % 2000000 == 0):
            log("waiting for target_date")
            count = 0
    while (last_date != TARGET_DATE):
        log("target_date not found")
        log(f"sleep for {WAITING_TIME} secs then refresh")
        time.sleep(WAITING_TIME)
        log("refresh the website")
        nthualb.refresh()
        log("refresh last_date")
        last_date = nthualb.find_element_by_xpath(
            "/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[1]/tbody/tr/td[5]/div[2]").text

    log("target_date found!")

    log("select rows")
    WebDriverWait(nthualb, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[2]/tbody/tr")))
    select_table = nthualb.find_elements_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[2]/tbody/tr")
    select_table.pop()
    log("select col and select the button")
    place_button1 = select_table[TIME1].find_elements_by_tag_name("td")[PLACE1].find_element_by_tag_name("div")
    log("click the button")
    place_button1.click()

    log("wait for alert appear")
    WebDriverWait(nthualb, 10).until(EC.alert_is_present())
    log("click accept in alert")
    nthualb.switch_to.alert.accept()
    log("wait for alert appear")
    WebDriverWait(nthualb, 10).until(EC.alert_is_present())
    log("click accept in alert")
    nthualb.switch_to.alert.accept()

    log("reget the website")
    nthualb.get("https://nthualb.url.tw/reservation/reservation?d=4")
    log("select rows")
    WebDriverWait(nthualb, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[2]/tbody/tr")))
    select_table = nthualb.find_elements_by_xpath("/html/body/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[2]/tbody/tr")
    select_table.pop()
    log("select col and select the button")
    place_button2 = select_table[TIME2].find_elements_by_tag_name("td")[PLACE2].find_element_by_tag_name("div")
    log("click the button")
    place_button2.click()

    log("wait for alert appear")
    WebDriverWait(nthualb, 10).until(EC.alert_is_present())
    log("click accept in alert")
    nthualb.switch_to.alert.accept()
    log("wait for alert appear")
    WebDriverWait(nthualb, 10).until(EC.alert_is_present())
    log("click accept in alert")
    nthualb.switch_to.alert.accept()

    for i in range(0, 20):
        log("crawling success!!!!!!")

    log("Press any key to close the webdriver")
    os.system("pause")

    log("close the webdriver")
    nthualb.close()

    log("F.I.N.")
    return


if __name__ == '__main__':
    log("start running")
    crawling()
