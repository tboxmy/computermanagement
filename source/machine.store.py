from decimal import *
from getmac import get_mac_address as gma
import json
import psutil
import platform
# importing the requests library
import requests
import socket
import os, sys
from datetime import datetime
from config import get_url, get_apikey, get_token

if platform.system() == "Windows":
    import wmi

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def getMachine_addr():
    os_type = sys.platform.lower()
    dummy = None
    if "win" in os_type:
        # command = "wmic bios get serialnumber, manufacturer, version"
        # dummy = os.popen(command).read().replace("\n",",").replace("	","")
        windata = wmi.WMI()
        sysbios = windata.Win32_BIOS()[0]
        dummy = "".join([sysbios.Manufacturer, ',',sysbios.Version, ',', sysbios.Serialnumber])
    elif "linux" in os_type:
        command = """awk '{printf "%s"",",$0}' /sys/class/dmi/id/bios_version /sys/class/dmi/id/bios_vendor /sys/class/dmi/id/bios_date"""
        # command = "hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid"
        try:
            dummy = os.popen(command).read()
        except:
            dummy = "NA"
    elif "darwin" in os_type:
        command = "ioreg -l | grep IOPlatformSerialNumber"
        dummy = os.popen(command).read().replace("\n",",").replace("	","")
    return dummy

RESOURCEID = 1
DISPLAY = 1
APP_RELEASE = 'version 0.9.2'
if sys.argv[1] != None:
    RESOURCEID = sys.argv[1]
    if sys.argv[1] == '-h':
        print ('Usage: command <tag_id>')
        print ('or to silence details')
        print ('command -s <tag_id>')
        sys.exit(0)
    if sys.argv[1] == '-v':
        print (sys.argv[0], ' ', APP_RELEASE)
        sys.exit(0)
    if sys.argv[1] == '-s':
        DISPLAY = 0
        RESOURCEID = sys.argv[2]

uname = platform.uname()
sys_system = {uname.system}
sys_name = {uname.node}
sys_release = {uname.release}
sys_version = {uname.version}
sys_processor = {uname.machine}
sys_processor = {uname.processor}
ip_address = socket.gethostbyname(socket.gethostname())
mac_address = gma()
if DISPLAY == 1:
    print("="*40, "System Information", "="*40)
    print(f"System: {uname.system}")
    print('IP:',ip_address)
    print('MAC:',mac_address)
if uname.system == 'Windows':
    if sys.getwindowsversion().build >= 22000:
        sys_release = 11
# Boot Time
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
last_boot = str(bt.year) + '/' + str(bt.month) + '/' + str(bt.day) +' ' + str(bt.hour) + ':' + str(bt.minute) + ':' + str(bt.second)
if DISPLAY == 1:
    print("="*40, "Boot Time", "="*40)
    print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")
    print("Last boot:", last_boot)

# CPU info
cpufreq = psutil.cpu_freq()
cpu1 = psutil.cpu_count(logical=False)
cpu2 = psutil.cpu_count(logical=True)
cpu3 = None
cpu4 = None
cpu5 = None
cpu6 = None
cpu7 = Decimal(psutil.cpu_percent())
if cpufreq != None:
    cpu3 = Decimal(cpufreq.max)
    cpu4 = Decimal(cpufreq.min)
    cpu5 = cpufreq.current
# Memory usage
svmem = psutil.virtual_memory()
memory1 = get_size(svmem.total)
memory2 = get_size(svmem.available)
memory3 = get_size(svmem.used)
memory4 = Decimal(svmem.percent)

if DISPLAY == 1:
    print("="*40, "CPU Info", "="*40)
    # number of cores
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    # CPU usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")

# Memory Information
if DISPLAY == 1:
    print("="*40, "Memory Information", "="*40)
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    print("="*20, "SWAP", "="*20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")

# Disk Information
if DISPLAY == 1:
    print("="*40, "Disk Information", "="*40)
    print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
storages = []
for partition in partitions:    
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    if DISPLAY == 1:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    mydata = {'device': partition.device, 'mount': partition.mountpoint, 
              'filesystem': partition.fstype, 'total': get_size(partition_usage.total),
              'used': get_size(partition_usage.used), 'free': partition_usage.free, 'percentage': partition_usage.percent}
    storages.append(mydata)
storage1 = json.dumps(storages)
# get IO statistics since boot
disk_io = None
if cpufreq != None:
    disk_io = psutil.disk_io_counters()
    if DISPLAY == 1:
        print(f"Total read: {get_size(disk_io.read_bytes)}")
        print(f"Total write: {get_size(disk_io.write_bytes)}")

# Network information
if DISPLAY == 1:
    print("="*40, "Network Information", "="*40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
networking = []
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        if DISPLAY == 1:
            print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            if DISPLAY == 1:
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            mydata = { 'IP': address.address, 'netmask': address.netmask, 'broadcast': address.broadcast}
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            if DISPLAY == 1:
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
            mydata = { 'IP': address.address, 'netmask': address.netmask, 'broadcast': address.broadcast}
    networking.append(mydata)

network1 = json.dumps(networking)
# get IO statistics since boot
net_io = psutil.net_io_counters()
if DISPLAY == 1:
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

# get windows installed software
# windata = wmi.WMI()
# software = windata.Win32_Product()
# sysbios = windata.Win32_BIOS()[0]
# print(f'BIOS :{sysbios.Manufacturer}, {sysbios.Version}, - {sysbios.Serialnumber}')
# for product in software:
#     print(f"Software: {product.Name} {product.ProcessId}")
if DISPLAY == 1:
    print("Win ", getMachine_addr())
# for product in systemwin:
#     print(f"Computer: {product.version}")

# defining a params dict for the parameters to be sent to the API
HEADERS = {'x-api-key':get_apikey(), 'Accept':'application/json',
           'Authorization':'Bearer '+ get_token()}

print('resource ', RESOURCEID)
PARAMS = {'resource_id': RESOURCEID, 
          'system': sys_system,
          'name':sys_name,
          'release':sys_release,
          'version':sys_version,
          'processor': sys_processor,
          'last_boot': last_boot,
          'ip_address': ip_address,
          'mac': mac_address,
          'cpu1': cpu1,         
          'cpu2': cpu2,
          'cpu3': cpu3,
          'cpu4': cpu4,
          'cpu5': cpu5,
          'cpu6': cpu6,
          'cpu7': cpu7,
          'memory1': memory1,
          'memory2': memory2,
          'memory3': memory3,
          'memory4': memory4,
          'network1': network1,
          'storage1': storage1,
          'bios': getMachine_addr(),
          }
 
# sending get request and saving the response as response object
try:
    response = requests.post(url = get_url(), headers=HEADERS, data=PARAMS)
    # extracting data in json format
    data = response.json()
    print(data)
except:
    print('Server connection failed URL=', get_url()) 
    sys.exit(2)
# try:
#     response = requests.post(url = get_url(), headers=HEADERS, data=PARAMS)
#     data = response.json()
#     print(data);
# except NameError:
#     print("URL not defined ", get_url())
# except:
    # print('Server connection failed ', get_url()) 

