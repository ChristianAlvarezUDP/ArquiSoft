import os
import json
import subprocess

bus_ip = '127.0.0.1'
bus_port = 5000

service_files = os.listdir("services")
processes = []

subprocess.Popen(["python", 'bus.py', json.dumps(service_files), bus_ip, str(bus_port)])

port = 6000
for file in service_files:
    print(file)

    process = subprocess.Popen(["python", "services/" + file, str(port), bus_ip, str(bus_port)])
    processes.append(process)

    port += 1
