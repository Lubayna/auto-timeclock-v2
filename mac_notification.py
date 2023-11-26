import subprocess

# macOS の通知を表示する関数
def notify(title, message):
  # osascript コマンドを使用して macOS の通知を表示
  # 'display notification' は macOS の AppleScript で通知を表示するためのコマンド
  subprocess.Popen(f'osascript -e \'display notification "{message}" with title "{title}"\'', shell=True)
