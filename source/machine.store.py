from decimal import *
import json
import psutil
import platform
# importing the requests library
import requests
import socket
import sys

# api-endpoint
URL = "https://cmgimis.apps.cmg.com.my/api/machines/store"
# URL = "http://snipeitcmgi.test:90/api/machines/store"
APIKEY = "Nicholas season 2024"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiOWNkOWM3NDJlYjJjNWQxYWFmNTk4ODg4MTU2M2Q4MWFmNjRlMTRkYmJmZGU2YWVkNGYwMDYzZjQwNDIwN2I2MDYyYzcyMzBkMjgxMWFlMjciLCJpYXQiOjE3MjEwNDExMzMuODUzMjMsIm5iZiI6MTcyMTA0MTEzMy44NTMyMzQsImV4cCI6MjE5NDM0MDMzMy44Mzg0MDksInN1YiI6IjEiLCJzY29wZXMiOltdfQ.b1dDrR1o9mrMkm4XgaU7TzAqMBFsspuZm1YM3zZIremEBUUTCXRMwFOPJRFNnLPK74mTx_17RP1MSsYyL2cVHqWUWfziBsvpMdRVccwlt1USEKMJfjzpxBzXbr04mPJ8j69aXZTWc7h5YjWizgN32EPcYs9uXpSgqEFAoTqFRCHAaEwXYwfIr_J-mcc_zQjqQ_xQmSXkQpRJH6r8OhthosRyh_L7lM-nM42bja0cApznS7XJh5TKjExlLu3QUoEmoSBEDu5_S0DjvdVf4-Vw1oyFIK_nx5HPlAoUYFQzaZE-JrUcYE-0j3cErwJ-5p9NZQW3ErWC15Al2GOp3v09iLpzx63UN-6zdwjn8HNdmd-O-jK-dc8fIx1X7J_ntIL2kIHd6EJZHOO8VKuOjiBbWPQtgRv0uTTBz24nNd1f8WgXZKDqyHvHY-deylYdcdFpAivZ0tTQDqe97MIVgBO5OEiwnjr1LwGb3jfi428xfCoxrPn-mYln5bcY0Ag5rg1S4B8rRS68JeW2Dygn_u3bfqZ_KSef_BdcL79CjW1vIqLvSFPRcKqhraR_P4JBGRGkf09UfE5zthGNHVyTn641gAXoNVC2JR2buZLelVXhkJaVEzYXDgTu-xvC7ONqFtrvuoSFaWQxK_f5wn5ixxTnSQPt2cMzM6GhHSZ2It-E2po"
# TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNTIwZTdiMGRkY2VmYzhjYWFiODY3ZjM1YzVlMWUxZGFmZjY0ZTdkNjZjZGMxZTcxZGNmYjkwNjYzMTZjZmRjNDJhMWY4MzJmNTYxZWQ2ZGUiLCJpYXQiOjE3MjEwMTU3ODMuOTA4MjU1LCJuYmYiOjE3MjEwMTU3ODMuOTA4MjYsImV4cCI6MjE5NDMxNDk4My43NDE3Niwic3ViIjoiMSIsInNjb3BlcyI6W119.n8whYZV8G8YJ9r0-X58H-zmHeKXW1TcWQOdoYjce4s577mQcZuqPV19P5kpPsuS3axKjsoCv4wBIFc2HnUoDtyMZdzTC-_Kdx0YiUm2EbGze9h2Jg29Lklo21X8UpG7tMakZ2o32rnp48PaTJ9d2d7n6fQ8K59aoEF1smU9jk-PV9078HAMvp6_Y080kcIjx9qDUG_tn48GtEM9V-GCREkWEAaPnrtr7YIuGvzxeBUm5Z6NEcQXdpYysq3s_wgAIxIS2FHdXz7uEEnaMR9yL8RKrEMPCoICeFWuacn_19veZ-1y1AROHOcfkIPE8XKk45KWsCzF-MN599jBPH3m_aN9ifvlXeueqgc4vVDF_d_CD4kGfGRebzFvWTIRGhrNEun7XhNxkQMvoJsMdniMOFgMTnnAvgk1a21grrAs8-2jGlHquPABSiS92AStnVgX0j8Rpqk09jKvmEnTYXqdrSeLiwpwY-OhGRbNnUrG_GOG8phE3luU6YIWwRN_wD7tbsZRRYDw6v97tjtpx1A0AY9xWnezgUZFkhFhl9_2eilyIoHAFUqToehpllyKRfsi6mJVXTRNqNqYqFTwdBZJU8YVEH35HMRKnS_ORvGZ2WJyIbmnFJaE18_LFgC6cGPPqa7XYnzLvDY6SKzWWNiWWKzP_XezshrH6I4jrXrD_mEg" 
from datetime import datetime

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

print("="*40, "System Information", "="*40)
uname = platform.uname()
print(f"System: {uname.system}")
sys_system = {uname.system}
sys_name = {uname.node}
sys_release = {uname.release}
sys_version = {uname.version}
sys_processor = {uname.machine}
sys_processor = {uname.processor}
ip_address = socket.gethostbyname(socket.gethostname())
print('IP:',ip_address)
if uname.system == 'Windows':
    if sys.getwindowsversion().build >= 22000:
        sys_release = 11
# Boot Time
print("="*40, "Boot Time", "="*40)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

last_boot = str(bt.year) + '/' + str(bt.month) + '/' + str(bt.day) +' ' + str(bt.hour) + ':' + str(bt.minute) + ':' + str(bt.second)
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

# let's print CPU information
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
print("="*40, "Memory Information", "="*40)
# get the memory details

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
print("="*40, "Disk Information", "="*40)
print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
storages = []
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
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
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    print(f"Total write: {get_size(disk_io.write_bytes)}")

# Network information
print("="*40, "Network Information", "="*40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
networking = []
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
            mydata = { 'IP': address.address, 'netmask': address.netmask, 'broadcast': address.broadcast}
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")
            mydata = { 'IP': address.address, 'netmask': address.netmask, 'broadcast': address.broadcast}
    networking.append(mydata)
network1 = json.dumps(networking)
# get IO statistics since boot
net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

# defining a params dict for the parameters to be sent to the API
HEADERS = {'x-api-key':APIKEY, 'Accept':'application/json',
           'Authorization':'Bearer '+TOKEN}
RESOURCEID = 1
if sys.argv[0] != None:
    RESOURCEID = sys.argv[1]
print('resource ', RESOURCEID)
PARAMS = {'resource_id': RESOURCEID, 
          'system': sys_system,
          'name':sys_name,
          'release':sys_release,
          'version':sys_version,
          'processor': sys_processor,
          'last_boot': last_boot,
          'ip_address': ip_address,
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
          'storage1': storage1
          }
 
# sending get request and saving the response as response object
response = requests.post(url = URL, headers=HEADERS, data=PARAMS)
 
# extracting data in json format
data = response.json()
print(data);