python.exe -m pip install --upgrade pip
pip install pyautogui
pip install opencv-python
pip install pynput
pip install requests
pip install python-dotenv
pip install pillow
pip install pyinstaller
pip install ttkthemes

pyinstaller --onefile --noconsole --name=Warspear-AutoMarket --icon=imgs/icones/icon_ws_mkt.ico ws_interface.py
pyinstaller --onefile --name=Warspear-AutoMarket --icon=imgs/icones/icon_ws_mkt.ico ws_interface.py