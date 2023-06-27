from netmiko import ConnectHandler
import threading
import os
import csv
import re
import time

###############CHANGES TO BE MADE ###########################################################
# Define the SCP source and destination file paths
username = "admin"
password = "cisco!123"
version_regex = 'Cisco IOS XE Software, Version ([\d\.]+[a-z]+)'
###############CHANGES TO BE MADE ###########################################################

# Function to copy the file using SCP
def dav(device_ip):
    try:
        # Define the device connection details
        device = {
            "device_type": "cisco_ios",
            "ip": device_ip,
            "username": username,
            "password": password,
        }

        # Connect to the device
        status = "Fail"
        net_connect = ConnectHandler(**device)

        # Determine the current working directory (CWD)
        output = net_connect.send_command("show ver")
        if output:
            status = "Pass"
            lines = str(output).splitlines()
            for line in lines:
                cline = str(line).strip()
                matches = re.match(version_regex, cline)
                if matches:
                    version = matches.group(1)
        else:
            # Copy the file using SCP
            print(f"Could not fetch the show version output on device {device_ip}.")
        
        return device_ip, status, version

        # Disconnect from the device
        # net_connect.disconnect()
    except Exception as e:
        print(f"An error occurred for device {device_ip}: {str(e)}")
        return device_ip, str(e), "Fail"

# Read the device IPs from the file
with open("device.txt", "r") as file:
    device_ips = [line.strip() for line in file.readlines()]

# Create a list to store the results
results = []

# Create a list of threads
threads = []
for ip in device_ips:
    thread = threading.Thread(target=lambda: results.append(dav(ip)))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

 # Check if the output file already exists
file_exists = os.path.isfile('copy_output.csv')

# Open the input and output files
with open('copy_output.csv', 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    if not file_exists:
        csv_writer.writerow(['IP', 'Status', 'Version'])
    
    # Write the results into csv file
    print(results)
    for result in results:
        csv_writer.writerow(result)
    print("All threads completed.")
