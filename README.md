# NTHU_alb_reserve
## Environment
- OS: Windows 11
- Python version: 3.11.1
- Packages version: see `requirements.txt` for more details

## Getting Start
### 在有 Python 環境的電腦運行
將整個檔案下載下來後，執行
```sh
py -m venv venv
.\venv\Scripts\activate
py -m pip install -r requirements.txt
.\src\main.py
```
即可正常運行。

### 打包成 `exe` 執行檔
```sh
py -m venv venv
.\venv\Scripts\activate
py -m pip install -r requirements.txt
py -m pip install  pyinstaller

pyinstaller -F .\src\main.py
```
打包完成後，將 `settings.json` 及 `NTHU_OAuth_Decaptcha.crx` 放入 `exe` 執行檔同一層目錄。

## Thanks
- Chrome extension [NTHU OAuth Decaptcha](https://github.com/justin0u0/NTHU-OAuth-Decaptcha) by [Justin0u0](https://github.com/justin0u0).

## License
[MIT](https://choosealicense.com/licenses/mit/)