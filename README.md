# Reservation_of_NTHUalb

## Introduction
This is a tiny python script to auto reserve the court of the ALB in NTHU.
<br>(This script only for education.)
### Why Does This Script Born?
Because somebody said that he cannot reserve the court at alb every time, because other people using script to fight the court QAQ. So, he wants a script to balance the unbalance on his mind (?).

## Description

### Before Use
Before using this "tiny" script, please install some applications to make sure this script will work properly.

First, at least `Python 3.7` or above is required (because I used the f-string to format the string owo).
<br>This crawler using `Chrome Driver` or `Edge Driver`. Remember to install the correspond browser.
<br>Also, you need to install these python packages. You can just using the commands below to install them.
```
$ pip install selenium
$ pip install webdriver_manager
```
Oh, btw, you must have the permission to pass oauth of NTHU. If you don't, I cann't help you. QQ

### While Using
You must have `revservation_of_nthualb.py`, `setting.json`, `NTHU_OAuth_Decaptcha.crx` and `start.bat` in your folder. When you wants to start, just double-click `start.bat`. And then, what you need to do is just fill all contents in `setting.json` following each tag name.

Below is an example of `setting.json`.
``` json
./setting.json

{
    "id": "110999999",
    "password": "yourpassword",
    "place1": "1",
    "time1": "3",
    "place2": "1",
    "time2": "4",
    "target_date": "2022-05-20",
    "driver_type": "edge"
}
```

## Notice
- The court number is the row/col index (start from zero) in the table. For example, `"place1": "1", "time1": "3"` means that the `2nd` row and `4th` col in the table.
- You may enter the 5 days later today (you need this script only to reserve 5 days later). And the format is `YYYY-MM-DD`.

## Requirements

### Enviroment
Please using `Windows OS`. I'm not sure this script world properly or not in other OS.

### Applications
- `Python 3.7` or above
- `Google Chrome Browser` or `Edge Browser`

### Python Packages
- `selenium`
- `webdriver_manager`

## Another ~~Unimportant~~ Things
- This script just written as fun.
- If you see many strange grammer caused by my poor English, never in mind.
- Lines below this is very important! <b>VERY!</b>
- <b>DO NOT</b> use this script to grab the court. Otherwise, other people will disappointed like my friend. You can just see how this script working (?). And then, close it. I will appreciate you very much.
- Writing a description document is so tired. \_(:з」∠)\_

## Thanks
- Chrome extension [NTHU OAuth Decaptcha](https://github.com/justin0u0/NTHU-OAuth-Decaptcha) by [Justin0u0](https://github.com/justin0u0).

---
# Reservation_of_NTHUalb

## 簡介
這是一個小小小的python腳本，可以用來預約清大校體的場地。
<br>（這個腳本只用於教育研究）
### 為什麼有這個酷東西
有人說他每次都搶不到校體的場地，因為其他人都用程式去搶QAQ。
所以他也想要有一個來彌補他弱小的心靈(?)。

## 說明

### 開始之前
在開始用這個小東西之前，請先安裝一些程式來確保它會正常運行。

首先，最少會需要 `python3.7` 或更高的版本（因為我用了幾個f-string owo）。
<br>這個工具使用 `Chrome Driver` 或 `Edge Driver`。記得安裝相對應的瀏覽器。
<br>你也需要安裝一些Python的函式庫。你可以用下面這兩個指令安裝。 
```
$ pip install selenium
$ pip install webdriver_manager
```

歐，還有，你要可以登入清大校務資訊系統。如果不行的話我也幫不了你QQ。

### 使用時
你應該會在資料夾裡面看到 `revservation_of_nthualb.py` 、 `setting.json` 、 `NTHU_OAuth_Decaptcha.crx` 和 `start.bat` 。當你想要使用時，點兩下 `start.bat` 就好。接著你只要依照 `setting.json` 裡面的標籤名稱填寫就好。

下面是 `setting.json` 的例子。
``` json
./setting.json

{
    "id": "110999999",
    "password": "yourpassword",
    "place1": "1",
    "time1": "3",
    "place2": "1",
    "time2": "4",
    "target_date": "2022-05-20",
    "driver_type": "edge"
}
```

## 注意事項
- 場地號碼是場地在表格的位置編號（從零開始算）。像 `"place1": "1", "time1": "3"` 代表它在表格的 `第二行` 、 `第四列` 。
- 你只能輸入五天後的日期（你只會在預約五天後的場會用到這個腳本）。然後日期格式是 `YYYY-MM-DD` 。 

## 執行需求

### 環境
請使用 `Windows系統` ，我不確定其他的OS能不能用。

### 應用程式
- `Python 3.7` 或更高版本
- `Google Chrome Browser` 或 `Edge Browser`

### Python 函式庫
- `selenium`
- `webdriver_manager`

## 其它~~不重要~~的事情
- 這只是我寫好玩的。
- 如果你看得懂中文，就不要去看我破破的英文。QQ
- 下面ㄉ東西很重要！<b>非常超級無敵！</b>
- <b>不要</b>用這個工具去搶場地，不然其他人會像我朋友一樣哭哭。你可以就看看它是怎樣跑的(?)，然後就關掉它。謝你。
- 寫說明文檔好累。\_(:з」∠)\_

## 感謝
- Chrome 擴充延伸模組 [NTHU OAuth Decaptcha](https://github.com/justin0u0/NTHU-OAuth-Decaptcha) by [Justin0u0](https://github.com/justin0u0).