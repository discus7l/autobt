import subprocess
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='autobt.log', encoding='utf-8', level=logging.ERROR)

def quick_check():
    # Look for paired devices using bluetoothctl
    # Look for connected devices using bluetoothctl
    # Get device name and MAC address
    # Check wireplumb status
    pass

# Attempt to connect to paired device using bluetoothctl
def connect_bt(mac_address):
    try:
        subprocess.check_output(["bluetoothctl", "connect", mac_address])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error connecting to {mac_address}: {e.output.decode()}")
        return "Fail"
    return "Success"

# Set wireplumb
def set_wireplumb(device_name):
    try:
        subprocess.check_output(["wireplumb", device_name])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting wireplumb: {e.output.decode()}")
        return "Fail"
    return "Success"

mac_address = "41:42:FF:57:F9:CF" #Erazer
device_name = "Erazer" # Replace with actual device name

result = connect_bt(mac_address)
print(f'Result: {result}')

result = set_wireplumb(device_name)
print(f'Result: {result}')
