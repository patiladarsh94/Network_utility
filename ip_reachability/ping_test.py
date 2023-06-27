import os
import csv
import subprocess
import concurrent.futures

# Define a function to ping an IP address and return the reachability status
def ping_ip(ip):
    response = subprocess.run(['ping', '-c', '5', '-t', '128', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #response = subprocess.run(["ping", "-c", "3", ip], capture_output=True)
    response_str = response.stdout.decode('utf-8')
    print(response_str)
    if "0 received" in response_str:
        return ip, 'Fail'
    else:
        return ip, 'Pass'

# Open the input file
with open('input.txt', 'r') as ip_file:
    ips = [ip.strip() for ip in ip_file]

    # Use multithreading to ping all the IPs in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(ping_ip, ips)

    # Check if the output file already exists
    file_exists = os.path.isfile('output.csv')

    # Open the input and output files
    with open('input.txt', 'r') as ip_file, open('output.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        if not file_exists:
            csv_writer.writerow(['IP', 'Reachability'])

        # Write the results into csv file
        for result in results:
            csv_writer.writerow(result)
