# Post Machine data

## Installation

On Centos Linux
sudo dnf install python3-pip

Upgrade
python3.exe -m pip install --upgrade pip

Install packages
pip install requests
pip install psutil
pip install getmac
pip install wmi

Rename config.py-example to config.py and update the variable values.

## Generate installer

pip install -U pyinstaller
pyinstaller --onefile --name "MISAgent-windows11" source/machine.store.py source/config.py

## Execute

Collect and submit data to server

```
MISAgent-windows11.exe &lt;asset tag>
```

How to run the command

```
MISAgent-windows11.exe -h
```

Check the version of agent

```
MISAgent-windows11.exe -v
```

## References

https://thepythoncode.com/article/get-hardware-system-information-python

## Related projects

- [Snipe-IT](https://github.com/snipe/snipe-it)

## Credits

- [Tboxmy](https://github.com/tboxmy)
