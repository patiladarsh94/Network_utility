from netmiko import ConnectHandler, file_transfer
import threading
import os
import csv
import time

###############CHANGES TO BE MADE ###########################################################
# Define the SCP source and destination file paths
username = "admin"
password = "cisco!123"
source_file = "copy ftp://calo:calo@10.207.204.10/cat3k_caa-universalk9.16.12.08.SPA.bin"
destination_file = "flash:/cat3k_caa-universalk9.16.12.08.SPA.bin\n"
file_size = "480189009"
###############CHANGES TO BE MADE ###########################################################

# Function to copy the file using SCP
def copy_file(device_ip, source, destination):
    
    # Define the device connection details
    device = {
        "device_type": "cisco_ios",
        "ip": device_ip,
        "username": username,
        "password": password,
        "session_log" : "test_log.txt"
    }

    # Connect to the device
    net_connect = ConnectHandler(**device)

    # Determine the current working directory (CWD)
    output = net_connect.send_command("dir")
    cwd = ""
    for line in output.splitlines():
        if line.startswith("Directory of"):
            cwd = line.split("Directory of")[1].strip()

    # Check if the file already exists
    output = net_connect.send_command(f"dir {destination}")
    file_exists = "Directory of" in output

    if file_exists:
        print(f"File '{destination}' already exists on device {device_ip}. Skipping...")
    else:
        # Build the SCP command
        scp_command = f"{source} {destination}"
        if cwd:
            #scp_command += f" cwd {cwd}"
            pass

        #print(f"Copying file '{source}' to '{destination}' on device {device_ip}...")
        # Copy the file using SCP
        net_connect.write_channel(net_connect.normalize_cmd(scp_command))
        net_connect.read_until_prompt_or_pattern('Destination')
        net_connect.write_channel('\n')
        
        while True:
            time.sleep(5)
            if net_connect.base_prompt in net_connect.read_channel():
                break

    # Check if the file already exists
    output = net_connect.send_command(f"dir {destination}")
    file_exists = "Directory of" in output

    if file_exists:
        print(f"File '{destination}' Copied on device {device_ip}.")
       

    # Disconnect from the device
    # net_connect.disconnect()



copy_file('10.82.141.176', source_file, destination_file)