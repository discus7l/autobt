from asyncio import sleep
import subprocess
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='autobt.log', encoding='utf-8', level=logging.ERROR)

bt_connect_max_retries = 3

connected_list = []
device_info_list = []
device_info_dict = {}

# Check for paired and connected devices
def quick_check():
    # Look for paired devices using bluetoothctl
    # terminate if none are found
    # return a dictionary of device names and MAC addresses if found
    paired_check_result = subprocess.run(["bluetoothctl", "devices", "Paired"], stdout=subprocess.PIPE)

    if paired_check_result.stdout.decode().strip() == '':
        print("No paired devices found.")
        logging.error("No paired devices found.")
        exit(1)
    else:
        paired_devices = paired_check_result.stdout.decode().strip().split('\n')
        print(f"Paired devices: {paired_devices}")
        print(type(paired_devices))

        # Get device name and MAC address
        for device in paired_devices:
            device_info = device.split(' ', 2)
            if len(device_info) >= 3:
                device_name = device_info[2]
                mac_address = device_info[1]
                device_info_dict['device_name'] = device_name
                device_info_dict['mac_address'] = mac_address
                device_info_list.append(device_info_dict.copy())
            else:
                logging.error(f"Unexpected device info format: {device}")
    print(f'Device info dictionary:\n {device_info_list}') # Names and MAC addresses

    # Look for connected devices using bluetoothctl
    connected_check_result = subprocess.run(["bluetoothctl", "devices", "Connected"], stdout=subprocess.PIPE)

    if connected_check_result.stdout.decode().strip() == '':
        print("No connected devices found.")
        logging.error("No connected devices found.")
        result = "No connection"
        return result, device_info_list # Return list of paired devices
    else:
        connected_devices = connected_check_result.stdout.decode().strip().split('\n')
        print(f"Connected devices: {connected_devices}")
        print(type(connected_devices))

        # Get device name
        for device in connected_devices:
            device_info = device.split(' ', 2)
            if len(device_info) >= 3:
                connected_list.append(device_info[2])
            else:
                logging.error(f"Unexpected device info format: {device}")

    # Check wireplumb status
    print(f'Connected devices: {connected_list}') # Names only

    attachment = None
    return 0, attachment  # Return 0 if device is connected and wireplumb is set

# Attempt to connect to paired device using bluetoothctl
def connect_bt(mac_address):
    try:
        subprocess.check_output(["bluetoothctl", "connect", mac_address])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error connecting to {mac_address}: {e.output.decode()}")
        return "Fail"
    return "Success"

# Get wireplumb ID of connected device
def get_wireplumb_id(device_name):
    shell_command = [f'wpctl status | grep "{device_name}" | grep "vol"']
    wireplumb_output = subprocess.check_output(shell_command, shell=True).decode()
    print(f"Wireplumb output: \n{wireplumb_output}")

# Set wireplumb
def set_wireplumb(device_name):
    try:
        subprocess.check_output(["wireplumb", device_name])
    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting wireplumb: {e.output.decode()}")
        return "Fail"
    return "Success"

get_wireplumb_id("ERAZER  XT60PRO")
# --------------------------------------------------------------------#
# # Check device status, connect if necessary, and set wireplumb
# quick_check_result = quick_check()
# if quick_check_result[0] == 0:
#     print("Device is already connected and wireplumb is set.")
#     exit(0)
# elif quick_check_result[0] == "No connection":
#     print("Device is paired but not connected, attempting to connect.")
#     while bt_connect_max_retries > 0:
#         connect_result = connect_bt(quick_check_result[1][0]['mac_address'])  # Connect to the first paired device
#         if connect_result == "Success":
#             break
#         sleep(2)
#         bt_connect_max_retries -= 1

# if connect_result == "Success":
#     print("Device connected successfully.")
#     wireplumb_result = set_wireplumb(quick_check_result[1][0]['device_name'])  # Set wireplumb for the first paired device
#     if wireplumb_result == "Success":
#         print("Wireplumb set successfully.")
#     else:
#         print("Failed to set wireplumb.")

# if connect_result == "Fail":
#     print("Failed to connect to the device after multiple attempts.")
#     logging.error("Failed to connect to the device after multiple attempts.")
#     exit(1)

# --------------------------------------------------------------------#