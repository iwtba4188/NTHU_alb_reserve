import asyncio
import datetime
import threading
import time
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

import requests
from bs4 import BeautifulSoup

import utils

time_list = [
    "7:00~8:00",
    "8:00~9:00",
    "9:00~10:00",
    "10:00~11:00",
    "11:00~12:00",
    "12:00~13:00",
    "13:00~14:00",
    "14:00~15:00",
    "15:00~16:00",
    "16:00~17:00",
    "17:00~18:00",
    "18:00~19:00",
    "19:00~20:00",
    "20:00~21:00",
    "21:00~22:00",
    "22:00~23:00",
]
field_list = ["場1", "場2", "場3", "場4", "場5", "場6", "場7", "場8"]


def get_now_time():
    now_time = datetime.datetime.now()
    return now_time.strftime("%Y-%m-%d %H:%M:%S")


def get_reservation_date():
    tomorrow_time = datetime.datetime.now() + datetime.timedelta(days=5)
    return tomorrow_time.strftime("%Y-%m-%d")


def get_delta_timestamp(delta_day):
    delta_time = datetime.datetime.now() + datetime.timedelta(days=delta_day - 1)
    delta_time = delta_time.replace(hour=0, minute=0, second=0, microsecond=0)
    return str(int(delta_time.timestamp()))


def get_difference_time_to_tomorrow():
    now_time = datetime.datetime.now()
    tomorrow_time = datetime.datetime.now() + datetime.timedelta(days=1)
    tomorrow_time = tomorrow_time.replace(hour=0, minute=0, second=0, microsecond=0)
    return (tomorrow_time - now_time).seconds


def update_local_time():
    label_now_time_local.config(text=get_now_time())
    window.after(1000, update_local_time)


def update_server_time():
    if label_server_time.cget("text") != "登入後同步":
        now_server_time = datetime.datetime.strptime(
            label_server_time.cget("text"), "%Y-%m-%d %H:%M:%S"
        )
        now_server_time += datetime.timedelta(seconds=1)
        label_server_time.config(text=now_server_time.strftime("%Y-%m-%d %H:%M:%S"))
    window.after(1000, update_server_time)


def update_reservation_status():
    if (
        get_difference_time_to_tomorrow() < 10
        and label_reservation_listbox.size() != 0
        and label_server_time.cget("text") != "登入後同步"
    ):
        time.sleep(10.5)

        if label_server_time.cget("text") == "登入後同步":
            label_status.config(text="尚未登入成功，本次跨日不會進行預約", fg="white", bg="red")
        else:
            label_status.config(text="開始預約", fg="white", bg="green")
            start_reservation(immediate=False)
            label_status.config(text="預約結束", fg="white", bg="green")
    window.after(1000, update_reservation_status)


def create_reservation_tasks(status, immediate=False):
    async def post_reservation(url, headers, json_, status, index):
        # response = await requests.post(url=url, headers=headers, json=json)
        time.sleep(0.5)
        response = await loop.run_in_executor(
            None, lambda: requests.post(url=url, headers=headers, json=json_)
        )

        html_data = BeautifulSoup(response.text, "html.parser")

        if (response.status_code == 200 and str(html_data) == "ok") or status[
            index
        ] is True:
            label_reservation_listbox.delete(index)
            label_reservation_listbox.insert(
                index,
                f"[成功] {field_list[int(json_['field'])]} {time_list[int(json_['time'])]}",
            )
            status[index] = True
        else:
            status[index] = False

    URL = "https://nthualb.url.tw/reservation/api/reserve_field"
    tasks = []
    all_reservation = list(label_reservation_listbox.get(0, tk.END))
    all_reservation = [reservation.split(" ") for reservation in all_reservation]
    all_reservation = [i for i in all_reservation if len(i) == 2]  # 去掉已經處理過的預約
    post_header = utils.get_headers()["post_header"]

    if label_server_time.cget("text") == "登入後同步":
        label_status.config(text="尚未登入成功，本次預約失敗", fg="white", bg="red")
        return
    else:
        label_status.config(text="開始預約", fg="white", bg="green")
        for index, info in enumerate(all_reservation):
            field = field_list.index(info[0])
            time_ = time_list.index(info[1])
            post_header["content-length"] = f"{42+len(str(field))+len(str(time_))}"
            post_header["cookie"] = f"PHPSESSID={session}"

            data = {
                "time": str(time_),
                "field": str(field),
                "date": get_delta_timestamp(delta_day=4),
            }

            for _ in range(5):
                tasks.append(
                    loop.create_task(
                        post_reservation(URL, post_header, data, status, index)
                    )
                )

    return tasks


async def start_reservation(immediate=False):
    status = [False for _ in range(len(list(label_reservation_listbox.get(0, tk.END))))]
    tasks = create_reservation_tasks(status=status, immediate=immediate)
    if tasks is not None:
        loop.run_until_complete(asyncio.wait(tasks))
        for index, info in enumerate(list(label_reservation_listbox.get(0, tk.END))):
            # 已經更新過的預約不再更新
            if len(info.split(" ")) > 2:
                continue

            field = int(info.split(" ")[0])
            time_ = int(info.split(" ")[1])
            if not status[index]:
                label_reservation_listbox.delete(index)
                label_reservation_listbox.insert(
                    index, f"[失敗] {field_list[field]} {time_list[time_]}"
                )


def immediate_reservation():
    threading.Thread(
        target=lambda loop: loop.run_until_complete(start_reservation()),
        args=(asyncio.new_event_loop(),),
    ).start()


def button_login_click():
    if entry_id.get() == "" or entry_psw.get() == "":
        label_status.config(text="請輸入學號或密碼", fg="white", bg="red")
        return
    else:
        button_login.config(state=tk.DISABLED)
        label_status.config(text="登入中（大約需要三十秒）", fg="black", bg="yellow")
        threading.Thread(
            target=lambda loop: loop.run_until_complete(button_login_click_thread()),
            args=(asyncio.new_event_loop(),),
        ).start()


async def button_login_click_thread():
    global session
    session = await utils.crawling_PHPSESSID(entry_id.get(), entry_psw.get())
    if session is None:
        label_status.config(text="登入失敗，請確認學號及密碼後，再重試一次", fg="white", bg="red")
    else:
        label_status.config(text="登入成功", fg="white", bg="green")
        label_server_time.config(text=utils.get_server_time(session))
    button_login.config(state=tk.NORMAL)


def button_reservation_add_click():
    def button_choose_click(time, field):
        choose_time_and_field.destroy()
        if time != "" and field != "":
            label_reservation_listbox.insert(tk.END, f"{field} {time}")

    choose_time_and_field = tk.Toplevel(window)
    choose_time_and_field.title("選擇時間")
    choose_time_and_field.geometry("300x150")
    choose_time_and_field.resizable(False, False)
    choose_time_and_field.attributes("-topmost", True)
    choose_time_and_field.grab_set()

    # frame 場地
    frame_choose_field = tk.Frame(choose_time_and_field)
    frame_choose_field.pack()

    label_choose_field = tk.Label(frame_choose_field, text="選擇場地", font=("新細明體", 15))
    label_choose_field.pack()

    combobox_choose_field = ttk.Combobox(
        frame_choose_field, font=("新細明體", 15), state="readonly", values=field_list
    )
    combobox_choose_field.pack()

    # frame 時間
    frame_choose_time = tk.Frame(choose_time_and_field)
    frame_choose_time.pack()

    label_choose_time = tk.Label(frame_choose_time, text="選擇時間", font=("新細明體", 15))
    label_choose_time.pack()

    combobox_choose_time = ttk.Combobox(
        frame_choose_time, font=("新細明體", 15), state="readonly", values=time_list
    )
    combobox_choose_time.pack()

    # frame 確定
    frame_choose_button = tk.Frame(choose_time_and_field)
    frame_choose_button.pack()

    button_choose = tk.Button(
        frame_choose_button,
        text="確定",
        font=("新細明體", 15),
        command=lambda: button_choose_click(
            combobox_choose_time.get(), combobox_choose_field.get()
        ),
    )
    button_choose.pack()


def button_reservation_delete_click():
    try:
        pos = label_reservation_listbox.curselection()[0]
        label_reservation_listbox.delete(pos)
    except:
        pass


def button_reservation_clear_click():
    label_reservation_listbox.delete(0, tk.END)


def button_reservation_up_click():
    try:
        pos = label_reservation_listbox.curselection()[0]
        if pos != 0:
            text = label_reservation_listbox.get(pos)
            label_reservation_listbox.delete(pos)
            label_reservation_listbox.insert(pos - 1, text)
            label_reservation_listbox.select_set(pos - 1)
    except:
        pass


def button_reservation_down_click():
    try:
        pos = label_reservation_listbox.curselection()[0]
        if pos != 0:
            text = label_reservation_listbox.get(pos)
            label_reservation_listbox.delete(pos)
            label_reservation_listbox.insert(pos + 1, text)
            label_reservation_listbox.select_set(pos + 1)
    except:
        pass


# window config
window = tk.Tk()
window.title("清華大學羽球場地預約")
window.geometry("600x450")
window.resizable(False, False)
###############################################

# frame time config
frame_time = tk.Frame(window)
frame_time.pack(side=tk.TOP)
###############################################

# label time config
label_now_time_description = tk.Label(
    frame_time, text="現在本地時間", font=("新細明體", 20, "bold")
)
label_now_time_local = tk.Label(frame_time, font=(20))
label_server_time_description = tk.Label(
    frame_time, text="現在伺服器時間", font=("新細明體", 20, "bold")
)
label_server_time = tk.Label(frame_time, font=(20), text="登入後同步")

label_now_time_description.grid(row=0, column=0, ipadx=20)
label_now_time_local.grid(row=1, column=0, ipadx=20)
label_server_time_description.grid(row=0, column=1, ipadx=20)
label_server_time.grid(row=1, column=1, ipadx=20)
###############################################

# frame id psw login config
frame_id_psw_login = tk.Frame(window)
frame_id_psw_login.pack(side=tk.TOP, pady=20)

frame_id_psw = tk.Frame(frame_id_psw_login)
frame_id_psw.grid(row=0, column=0)

label_id = tk.Label(frame_id_psw, text="學號", font=("新細明體", 20, "bold"))
entry_id = tk.Entry(frame_id_psw, font=(20))
label_psw = tk.Label(frame_id_psw, text="密碼", font=("新細明體", 20, "bold"))
entry_psw = tk.Entry(frame_id_psw, font=(20), show="*")

label_id.grid(row=0, column=0, ipadx=20)
entry_id.grid(row=0, column=1, ipadx=20)
label_psw.grid(row=1, column=0, ipadx=20)
entry_psw.grid(row=1, column=1, ipadx=20)

frame_login = tk.Frame(frame_id_psw_login)
frame_login.grid(row=0, column=1, padx=40)

button_login = tk.Button(
    frame_login,
    text="登入",
    font=("新細明體", 15),
    padx=20,
    pady=10,
    command=button_login_click,
)
button_login.grid(row=0, column=0)
###############################################

# frame status config
frame_status = tk.Frame(window)
frame_status.pack(side=tk.TOP)

label_status = tk.Label(
    frame_status, text="尚未登入", font=("新細明體", 10), fg="white", bg="red"
)
label_status.pack()
###############################################

# frame reservation config
frame_reservation = tk.Frame(window)
frame_reservation.pack(side=tk.TOP)

frame_reservation_time = tk.Frame(frame_reservation)
frame_reservation_time.pack()

label_reservation_time = tk.Label(
    frame_reservation_time,
    text=f"跨日後將預約 {get_reservation_date()} 的場地",
    font=("新細明體", 10),
)
label_reservation_time.pack()
###############################################

# frame reservation candidate config
frame_reservation_candidate = tk.Frame(window)
frame_reservation_candidate.pack(side=tk.TOP, pady=20)

frame_reservation_listbox = tk.Frame(frame_reservation_candidate)
frame_reservation_listbox.grid(row=0, column=0)

scrollbar_reservation_listbox = tk.Scrollbar(
    frame_reservation_listbox, orient=tk.VERTICAL
)
scrollbar_reservation_listbox.pack(side=tk.RIGHT, fill=tk.Y)
label_reservation_listbox = tk.Listbox(
    frame_reservation_listbox,
    font=("新細明體", 13),
    width=35,
    selectmode=tk.SINGLE,
    yscrollcommand=scrollbar_reservation_listbox.set,
)
label_reservation_listbox.pack(expand=True, fill=tk.BOTH)
scrollbar_reservation_listbox.config(command=label_reservation_listbox.yview)

frame_reservation_control = tk.Frame(frame_reservation_candidate)
frame_reservation_control.grid(row=0, column=1, padx=20)

button_reservation_add = tk.Button(
    frame_reservation_control,
    text="新增",
    font=("新細明體", 10),
    width=10,
    pady=3,
    command=button_reservation_add_click,
)
button_reservation_add.grid(row=0, column=0, pady=5)
button_reservation_delete = tk.Button(
    frame_reservation_control,
    text="刪除",
    font=("新細明體", 10),
    width=10,
    pady=3,
    command=button_reservation_delete_click,
)
button_reservation_delete.grid(row=1, column=0, pady=5)
button_reservation_clear = tk.Button(
    frame_reservation_control,
    text="清空",
    font=("新細明體", 10),
    width=10,
    pady=3,
    command=button_reservation_clear_click,
)
button_reservation_clear.grid(row=2, column=0, pady=5)
button_reservation_up = tk.Button(
    frame_reservation_control,
    text="上移",
    font=("新細明體", 10),
    width=10,
    pady=3,
    command=button_reservation_up_click,
)
button_reservation_up.grid(row=3, column=0, pady=5)
button_reservation_down = tk.Button(
    frame_reservation_control,
    text="下移",
    font=("新細明體", 10),
    width=10,
    pady=3,
    command=button_reservation_down_click,
)
button_reservation_down.grid(row=4, column=0, pady=5)

frame_reservation_imediate = tk.Frame(frame_reservation_candidate)
frame_reservation_imediate.grid(row=0, column=2)

button_reservation_imediate = tk.Button(
    frame_reservation_imediate,
    text="立即預約\n四日後",
    font=("新細明體", 15),
    width=10,
    pady=3,
    command=immediate_reservation,
)
button_reservation_imediate.pack()
###############################################

# frame info config
frame_info = tk.Frame(window)
frame_info.pack(side=tk.TOP)

label_info = tk.Label(
    frame_info, text="By iwtba4188@GitHub", font=("新細明體", 10), fg="gray", cursor="hand2"
)
label_info.pack()
label_info.bind(
    "<Button-1>",
    lambda e: webbrowser.open("https://github.com/iwtba4188/NTHU_alb_reserve/"),
)
###############################################


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    session = None
    update_local_time()
    update_server_time()
    update_reservation_status()
    window.mainloop()
