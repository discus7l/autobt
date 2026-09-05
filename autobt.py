#!/usr/bin/env python3

import time
import re
import subprocess
import logging
import configparser

from subprocess import Popen, PIPE, TimeoutExpired
from logging.handlers import RotatingFileHandler

# Set up logging
handler = RotatingFileHandler(
    '/mnt/mmc/MUOS/application/autobt.log',
    encoding='utf-8',
    maxBytes=1024*1024,
    backupCount=1
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Read configuration from autobt_conf.ini
config = configparser.ConfigParser()
config.read('/mnt/mmc/MUOS/application/autobt_conf.ini')
bt_connect_max_retries = int(config.get('DEFAULT', 'bt_connect_max_retries'))
wpctl_set_max_retries = int(config.get('DEFAULT', 'wpctl_set_max_retries'))
boot_delay = int(config.get('DEFAULT', 'boot_delay'))
volume = str(config.get('DEFAULT', 'volume'))

connected_list = []
device_info_list = []
device_info_dict = {}

# Check if bluetoothctl is frozen
def freeze_check():
    counter = 0
    while counter < 3:
        proc = Popen(
            ["bluetoothctl", "show"],
            stdout=PIPE,
            stderr=PIPE,
            text=True
        )

        try:
            outs, errs = proc.communicate(timeout=2)
            return 0
        except TimeoutExpired:
            counter += 1
            logger.error("bluetoothctl is frozen, killing the process and retrying.")
            proc.kill()
            outs, errs = proc.communicate()
        return 1

# Check for paired and connected devices
def quick_check(bt_connect_max_retries):
    # Look for paired devices using bluetoothctl
    # terminate if none are found
    # return a dictionary of device names and MAC addresses if found
    while bt_connect_max_retries > 0:
        try:
            paired_check_result = subprocess.run(["bluetoothctl", "devices", "Paired"], stdout=subprocess.PIPE)
            logger.info('Successfully executed paired devices check.')
            break
        except:
            logger.error("Error checking paired devices, retrying...")
            bt_connect_max_retries -= 1
            time.sleep(1)

    if paired_check_result.stdout.decode().strip() == '':
        print("No paired devices found.")
        logger.error("No paired devices found.")
        exit(1)
    else:
        paired_devices = paired_check_result.stdout.decode().strip().split('\n')
        logger.info(f"Paired devices: {paired_devices}")

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
                logger.error(f"Unexpected device info format: {device}")
    logger.info(f'Device info dictionary:\n {device_info_list}') # Names and MAC addresses

    # Look for connected devices using bluetoothctl
    connected_check_result = subprocess.run(["bluetoothctl", "devices", "Connected"], stdout=subprocess.PIPE)

    if connected_check_result.stdout.decode().strip() == '':
        logger.error("No connected devices found.")
        result = "No connection"
        return result, device_info_list # Return list of paired devices
    else:
        connected_devices = connected_check_result.stdout.decode().strip().split('\n')
        logger.info(f"Connected devices: {connected_devices}")

        # Get device name
        for device in connected_devices:
            device_info = device.split(' ', 2)
            if len(device_info) >= 3:
                connected_list.append(device_info[2])
            else:
                logger.error(f"Unexpected device info format: {device}")

    # Check wireplumb status
    logger.info(f'Connected devices: {connected_list}') # Names only
    shell_command = [f'wpctl status | grep \*']
    try:
        wireplumb_output = subprocess.check_output(shell_command, shell=True).decode()
    except subprocess.CalledProcessError as e:
        logger.error(f"Error checking wireplumb status: {e.output.decode()}")
        return "Fail", None

    for i in connected_list:
        if i in wireplumb_output:
            logger.info(f"Device {i} is connected and wireplumb is set.")
            return 0, None
    return "Wireplumb not set", connected_list

# Attempt to connect to paired device using bluetoothctl
def connect_bt(mac_address):
    try:
        subprocess.check_output(["bluetoothctl", "connect", mac_address])
    except subprocess.CalledProcessError as e:
        logger.error(f"Error connecting to {mac_address}: {e.output.decode()}")
        return "Fail"
    return "Success"

# Get wireplumb ID of connected device
def get_wireplumb_id(device_name):
    shell_command = [f'wpctl status | grep "{device_name}" | grep "vol"']
    try:
        wireplumb_output = subprocess.check_output(shell_command, shell=True).decode()
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting wireplumb ID for {device_name}: {e.output.decode()}")
        return "Fail"
    logger.info(f"Wireplumb output: \n{wireplumb_output}")
    match = re.search(r'(\d+)', wireplumb_output)
    id = match.group(1)
    return "Success", id

# Set wireplumb, set volume, write the ID to /run/muos/audio/nid_internal, and un-mute
def set_wireplumb(id, volume):

    try:
        subprocess.check_output(["wpctl", "set-volume", id, volume])
    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting volume: {e.output.decode()}")
        return "Fail"

    time.sleep(1)  # Wait for volume to be set before setting default

    try:
        subprocess.check_output(["wpctl", "set-default", id])
    except subprocess.CalledProcessError as e:
        logger.error(f"Error setting wireplumb: {e.output.decode()}")
        return "Fail"
   
    # shell_command = [f'echo "{id}" > "/run/muos/audio/nid_internal"']
    # try:
    #     subprocess.check_output(shell_command, shell=True)
    # except subprocess.CalledProcessError as e:
    #     logger.error(f"Error writing wireplumb ID to file: {e.output.decode()}")
    #     return "Fail"

    # shell_command = [f'wpctl set-mute {id} 0']
    # try:
    #     subprocess.check_output(shell_command, shell=True)
    # except subprocess.CalledProcessError as e:
    #     logger.error(f"Error setting mute status: {e.output.decode()}")
    #     return "Fail"
    return "Success"


# --------------------------------------------------------------------#
# Check device status, connect if necessary, and set wireplumb
logger.info("Starting autobt script.")
time.sleep(boot_delay)  # Wait for system to initialize

# Check if bluetoothctl is frozen
freeze_check_result = freeze_check()
if freeze_check_result == 1:
    logger.error("bluetoothctl is frozen, exiting script.")
    exit(1)

quick_check_result = quick_check(bt_connect_max_retries)
if quick_check_result[0] == 0:
    logger.info("Device is already connected and wireplumb is set.")
    exit(0)

elif quick_check_result[0] == "No connection":
    logger.info("Device is paired but not connected, attempting to connect.")
    while bt_connect_max_retries > 0:
        for device in quick_check_result[1]:
            connect_result = connect_bt(device['mac_address'])  # Connect to each paired device
            if connect_result == "Success":
                connected_device_name = device['device_name']
                logger.info(f"Connected to device {connected_device_name}.")
                break
        if connect_result == "Success":
            break
        time.sleep(2)
        bt_connect_max_retries -= 1

elif quick_check_result[0] == "Wireplumb not set":
    logger.info("Device is connected but wireplumb is not set, attempting to set wireplumb.")
    while wpctl_set_max_retries > 0:
        for device in quick_check_result[1]:
            get_wireplumb_id_result = get_wireplumb_id(device)
            if get_wireplumb_id_result[0] == "Success":
                break
        if get_wireplumb_id_result[0] == "Success":
            break
        time.sleep(1)
        wpctl_set_max_retries -= 1
    set_wireplumb_result = set_wireplumb(get_wireplumb_id_result[1], volume)
    if set_wireplumb_result == "Success":
        logger.info(f"Wireplumb set successfully for device {device}.")
        exit(0)
    else:
        logger.error("Failed to set wireplumb.")
        exit(1)

if connect_result == "Success":
    logger.info("Device connected successfully, getting wireplumb ID.")

    while wpctl_set_max_retries > 0:
        get_wireplumb_id_result = get_wireplumb_id(connected_device_name)
        if get_wireplumb_id_result[0] == "Success":
            break
        time.sleep(1)
        wpctl_set_max_retries -= 1

    set_wireplumb_result = set_wireplumb(get_wireplumb_id_result[1], volume)
    if set_wireplumb_result == "Success":
        logger.info("Wireplumb set successfully.")
        exit(0)
    else:
        logger.error("Failed to set wireplumb.")
        exit(1)

if connect_result == "Fail":
    logger.error("Failed to connect to the device after multiple attempts.")
    exit(1)

# --------------------------------------------------------------------#