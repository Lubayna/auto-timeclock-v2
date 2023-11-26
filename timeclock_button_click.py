import tkinter as tk
from jobcan_access import stamp
from send_slack_message import send_message
import threading  

def process_button(btn, text):
    # ボタンを無効化し、処理中の表示を更新
    btn.config(state=tk.DISABLED, text=f"Processing: {text}")

    # 新しいスレッドで非同期タスクを実行
    thread = threading.Thread(target=process_task, args=(btn, text))
    thread.start()

def process_task(btn, text):
    try:
        # jobcan_access モジュールの stamp 関数を実行
        stamp(text)
        # send_slack_message モジュールの send_message 関数を実行
        send_message(text)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # タスクが完了した後、ボタンの状態と表示を元に戻す
        app.after(0, btn.config, {'state': tk.NORMAL, 'text': text})

def button_command(btn,text):
    # ボタンが実行中のスレッドを持っていないか、スレッドが終了している場合、新しいスレッドを開始
    if not hasattr(btn, '_thread') or not btn._thread.is_alive():
        btn._thread = threading.Thread(target=process_button, args=(btn, text))
        btn._thread.start()

# Tkinterを使ってアプリの初期化
app = tk.Tk()
app.title("自動打刻アプリ")

# ボタンと対応するコマンドを作成し、表示
texts = ["業務開始します", "打刻表を確認します", "業務終了します"]
button1 = tk.Button(app, text=texts[0], command=lambda: button_command(button1, texts[0]))
button2 = tk.Button(app, text=texts[1], command=lambda: button_command(button2, texts[1]))
button3 = tk.Button(app, text=texts[2], command=lambda: button_command(button3, texts[2]))
button1.pack()
button2.pack()
button3.pack()

# アプリのメインループを開始
app.mainloop()
