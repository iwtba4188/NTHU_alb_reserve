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
<br>This crawler using Chrome driver, so you also need to download the `Chrome Browser` :D
<br>Also, you need to install these python packages. You can just using the commands below to install them. 
```
$ pip install selenium
```
```
$ pip install webdriver_manager
```
Oh, btw, you must have the permission to pass oauth of NTHU. If you don't, I cann't help you. QQ

### While Using
You must have `revservation_of_nthualb.py`, `setting.txt` and `start.bat` in your folder. When you wants to start, just double-click `start.bat`. There is an important step to set the settings correctly.

1. The first line in `setting.txt` is your student id (or other username).
2. The second is your password (detail in title Notice).
3. Third and Fourth are two numbers of court you wants to reserve (details in title Notice).
4. The last line is the target date, when catch the date is available, it will start the next part of the code (datails in title Notice).

Below is an example of `setting.txt`.
```
./setting.txt
110999999
mypassword123
13
14
2022-03-16
```

## Notice
- If you are not trust my code, you can just write something wrong and key-in the correct one after running the script in the browser. And you can see the sourse code and discover this script will <b>NOT</b> collect your password. But it's right to be careful.
- The court number is the row/col index (start from zero) in the table. For example, `13` means that the `2nd` row and `3th` col in the table.
- You may enter the 5 days later today (because I just write to grab the last day you can reserve). And the format is `YYYY-MM-DD`. 
- You can just simply double-click the `start.bat`. Or using other methods you like.

## Requirements

### Enviroment
Please using `Windows OS`. I'm not sure this script word properly or not in other OS.

### Applications
- `Python 3.7` or above
- `Google Chrome Browser`

### Python Packages
- `selenium`
- `webdriver_manager`

## Another ~~Unimportant~~ Things
- This script just written as fun.
- Many codes are not optimization becase I am lazy. If you have greater ideas, pls let me know.
- If you see many strange grammer caused by my poor English, never in mind.
- Maybe I will using `json` instead of `txt` very soon, it seems greater. owo b
- Lines below this is very important! <b>VERY!</b>
- <b>DO NOT</b> use this script to grab the court. Otherwise, other people will disappointed like my friend. You can just see how this script working (?). And then, close it. I will appreciate you very much.
- Writing a description document is so tired. \_(:з」∠)\_

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

首先，最少會需要`python3.7`或更高的版本（因為我用了幾個f-string owo）。
<br>這個工具會用到Chrome來實現自動化運作，所以你會需要下載`Chrome Browser` :D
<br>你也需要安裝一些Python的函式庫。你可以用下面這兩個指令安裝。 
```
$ pip install selenium
```
```
$ pip install webdriver_manager
```

歐，還有，你要可以登入清大校務資訊系統。如果不行的話我也幫不了你QQ。

### 使用時
你應該會在資料夾裡面看到`revservation_of_nthualb.py`、`setting.txt`和`start.bat`。當你想要使用時，點兩下`start.bat`就好。有一些很重要的設定要正確地完成，不然會壞掉。

1. 在`setting.txt`的第一行是你的學號（或其他可以登入的帳號）。
2. 第二行是你的密碼（細節在注意事項裡面）。
3. 第三、四行是兩個你想要選的場地的號碼（細節在注意事項裡面）。
4. 最後一行是目標的日期，抓到該日期更新就會開始下一步動作（細節還是在注意事項裡面）。

下面是`setting.txt`的例子。
```
./setting.txt
110999999
mypassword123
13
14
2022-03-16
```

## 注意事項
- 如果你不相信我的code，你可以在`setting.txt`的第二行亂寫，然後執行時在瀏覽器裡面輸入正確的密碼。或是你可以看我的code證明我<b>不會</b>蒐集你的密碼。但小心一點是對ㄉ。
- 場地號碼是場地在表格的位置編號（從零開始算）。像`13`代表它在表格的`第二行`、`第三列`。
- 你只能輸入五天後的日期（因為我只有寫搶你可以搶的最後一天而已）。還有，日期格式是`YYYY-MM-DD`。 
- 你可以點兩下`start.bat`直接開始就好，或是用你喜歡的其他方法。

## 執行需求

### 應用程式
- `Python 3.7` 或更高版本
- `Google Chrome Browser`

### Python 函式庫
- `selenium`
- `webdriver_manager`

## 其它~~不重要~~的事情
- 這只是我寫好玩的。
- 很多地方沒有最佳化，因為我有點懶。如果你有更好的改進方法，你可以跟我說。
- 如果你看得懂中文，就不要去看我破破的英文。QQ
- 我可能之後會把`txt`換成`json`，感覺好像比較棒owo b。
- 下面ㄉ東西很重要！<b>非常超級無敵！</b>
- <b>不要</b>用這個工具去搶場地，不然其他人會像我朋友一樣哭哭。你可以就看看它是怎樣跑的(?)，然後就關掉它。謝你。
- 寫說明文檔好累。\_(:з」∠)\_