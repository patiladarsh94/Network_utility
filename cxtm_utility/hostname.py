import csv

csv_file = "/Users/adapatil/Desktop/input.csv"
hostnames_file = 'hostnamesV3.txt'

def extract_ip_addresses(csv_file):
    devices = []
    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            devices.append(row[0])  # Assuming the hostname is in the first column of each row
    return devices

def write_ip_addresses(devices, hostnames_file):
    with open(hostnames_file, "w") as f:
        for d in devices:
            f.write(f"SetName:#{d}\n")
            f.write("tags:device\n")
            f.write(f"deviceHostname:{d}\n")

hostnames = extract_ip_addresses(csv_file)
write_ip_addresses(hostnames, hostnames_file)
