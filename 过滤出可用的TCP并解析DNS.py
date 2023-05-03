import os
import re
import requests
import socket
import json
from threading import Thread, Semaphore
from queue import Queue

def resolve_domain(domain):
    url = 'https://1.1.1.1/dns-query'
    headers = {
        'accept': 'application/dns-json',
    }
    params = {
        'name': domain,
        'type': 'A',
    }
    response = requests.get(url, headers=headers, params=params)
    ip = json.loads(response.text)['Answer'][0]['data']
    return ip

def test_connection(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((ip, port))
        sock.close()
        return True
    except Exception as e:
        return False

def process_file(file_name, output_dir, semaphore):
    with semaphore:
        file_path = os.path.join(dir_path, file_name)
        with open(file_path, 'r') as f:
            content = f.read()
        
        if 'proto udp' in content or 'proto tcp' not in content:  # 跳过没有TCP协议的配置文件
            print(f"{file_name} is skipped because it doesn't use TCP protocol")
            return
        
        domain = re.search(r'(?:remote\s+)([\w.-]+)', content).group(1)
        port = int(re.search(r'(?:remote\s+[\w.-]+\s+)(\d+)', content).group(1))

        ip = resolve_domain(domain)
        
        if test_connection(ip, port):
            new_content = content.replace(domain, ip)
            new_content = new_content + '\nauth-user-pass password.txt\n'  # 将 "auth-user-pass password.txt" 添加到.ovpn文件中
            new_file_path = os.path.join(output_dir, file_name)
            with open(new_file_path, 'w') as f:
                f.write(new_content)
            print(f"{file_name} is usable and saved to {new_file_path}")
        else:
            print(f"{file_name} is not usable")

dir_path = r'C:\\Users\Tony\Documents\surfshark配置'  # 替换为您的配置文件目录
output_dir = r'C:\\Users\Tony\Documents\surfshark配置\usable_configs'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

file_queue = Queue()
for file_name in os.listdir(dir_path):
    if file_name.endswith('.ovpn'):
        file_queue.put(file_name)

semaphore = Semaphore(50)

while not file_queue.empty():
    file_name = file_queue.get()
    thread = Thread(target=process_file, args=(file_name, output_dir, semaphore))
    thread.start()
