Installation

On Centos Linux
sudo dnf install python3-pip

Upgrade
python3.exe -m pip install --upgrade pip


Install packages
pip install requests
pip install psutil
pip install getmac

Generate installer
pip install -U pyinstaller 
pyinstaller --onefile --name "MISAgent-windows11" source/machine.store.py

Ref 
https://thepythoncode.com/article/get-hardware-system-information-python
https://github.com/snipe/snipe-it/tree/master