from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json 
from mac_notification import notify
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
from pathlib import Path

# 実行ファイルの基本ディレクトリを返す関数
def base_dir():
  if hasattr(sys, "_MEIPASS"):
    return Path(sys._MEIPASS)  # 実行ファイルで起動した場合

  else:
    return Path(".")  # pythonコマンドで起動した場合

# credentials.json ファイルから必要なデータを読み込む
f = open(base_dir()/'credentials.json')
data = json.load(f)

url= data["JOBCAN_URL"] 
user=data["JOBCAN_ID"] 
password=data["JOBCAN_PASSWORD"] 
f.close()

# Jobcan上の打刻を行う関数
def stamp(text):
  valid_texts = ["業務開始します", "打刻表を確認します", "業務終了します"]
  successed = "Jobcan打刻成功"
  failed = "Jobcan打刻失敗"
  # テキストが有効なものか確認
  if text in valid_texts:
      chrome_options = Options()
      # headless モードの Chrome ドライバーを作成
      chrome_options.add_argument("--headless=new")
      driver = webdriver.Chrome(options=chrome_options)

      driver.get(url)
      try:
          # ログイン情報を入力してログイン
          WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'user_email'))).send_keys(user)
          WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'user_password'))).send_keys(password)
          WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login_button'))).click()
        
      except:
          # ログインに失敗した場合
          print("Jobcanログインできなかった")
          notify("Jobcanログイン失敗", "Jobcanログインできませんでした！")
  
          return
      else:
          # テキストによって処理を分岐
          if text == valid_texts[0]:
              try:
                  # 出勤打刻
                  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'adit-button-work-start'))).click()
                  print("出勤打刻完了！")
                  notify(successed, "出勤打刻完了しました！") 
              except:
                  print("Jobcan出勤打刻できなかった")
                  notify(failed, "出勤打刻できませんでした")
                  return 

          elif text == valid_texts[1]:
              try:
                  # 打刻表確認
                  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/nav/div[2]/div/a[1]'))).click()
                  print("打刻表確認完了！")
                  notify(successed, "打刻表確認完了しました")
              except:
                print("Jobcan打刻表確認できなかった")
                notify(failed, "打刻表確認できませんでした")
                return 

          elif text == valid_texts[2]:
              try:
                  # 退勤打刻
                  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'adit-button-work-end'))).click()
                  print("退勤打刻完了！")
                  notify(successed, "退勤打刻完了しました")
              except:
                  print("Jobcan退勤打刻できなかった")
                  notify(failed, "退勤打刻完了しました")
                  return 
      finally:
          # ドライバーを終了
          driver.quit()
  else:
    # 無効なテキストの場合
    print("無効テキスト")
    notify(failed, "無効テキスト！")
    return 


