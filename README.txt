Installation

Upgrade
python.exe -m pip install --upgrade pip

Install packages
pip install requests
pip install psutil

Generate installer
pip install -U pyinstaller 
pyinstaller --onefile --name "MISAgent" source/machine.store.py

Ref 
https://thepythoncode.com/article/get-hardware-system-information-python
https://github.com/snipe/snipe-it/tree/master