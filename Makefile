# "run" ターゲット: Python スクリプトを実行する
run:
	python timeclock_button_click.py

# "build" ターゲット: PyInstaller を使用して実行ファイルをビルドする
build: clean
	pyinstaller timeclock_button_click.py --onefile --add-data "credentials.json:."

# "init" ターゲット: 必要な依存関係をインストールする
init:
	brew install python-tk@3.11
	pip install -r required-modules.txt

# "automator" ターゲット: まだ実装されていない旨を表示、まだ完成していない
# automator:
# 	echo "not yet implemented"

# "clean" ターゲット: ビルド関連のファイルやディレクトリを削除する
clean:
	rm -Rf build dist __pycache__ timeclock_button_click.spec
