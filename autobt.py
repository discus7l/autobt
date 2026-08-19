import subprocess
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='autobt.log', encoding='utf-8', level=logging.ERROR)

device_info_dict = {}

def quick_check():
    # Look for paired devices using bluetoothctl, terminate if none are found
    paired_check_result = subprocess.run(["bluetoothctl", "devices", "Paired"], stdout=subprocess.PIPE)

    if paired_check_result.stdout.decode().strip() == '':
        print("No paired devices found.")
        logging.error("No paired devices found.")
        exit(1)
    
    # Look for connected devices using bluetoothctl
    connected_check_result = subprocess.run(["bluetoothctl", "devices", "Connected"], stdout=subprocess.PIPE)

    if connected_check_result.stdout.decode().strip() == '':
        print("No connected devices found.")
        logging.error("No connected devices found.")
        result = "No connection"
        return result
    else:
        connected_devices = connected_check_result.stdout.decode().strip().split('\n')
        print(f"Connected devices: {connected_devices}")
        print(type(connected_devices))

        # Get device name and MAC address
        for device in connected_devices:
            device_info = device.split(' ', 2)
            if len(device_info) >= 3:
                mac_address = device_info[1]
                device_name = device_info[2]
                device_info_dict[mac_address] = device_name
                print(f"Device Name: {device_name}, MAC Address: {mac_address}")
            else:
                logging.error(f"Unexpected device info format: {device}")

    # Check wireplumb status
    print(device_info_dict)

    
    return 0

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

# Check device status
result = quick_check()
if result == 0:
    print("Device is already connected and wireplumb is set.")
    exit(0)
elif result == "No connection":
    print("Device is not connected.")


# result = connect_bt(mac_address)
# print(f'Result: {result}')

# result = set_wireplumb(device_name)
# print(f'Result: {result}')
