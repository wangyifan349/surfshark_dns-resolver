import requests
import os

def dns_query(domain):
    url = "https://1.1.1.1/dns-query"
    params = {
        "name": domain,
        "type": "A",
        "ct": "application/dns-json"
    }
    headers = {
        "Accept": "application/dns-json"
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        answers = data.get("Answer", [])
        for answer in answers:
            if answer["type"] == 1:  # A record
                ip_address = answer["data"]
                return ip_address
    return None

def write_to_hosts_file(domain, ip_address):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"

    with open(hosts_path, "a") as hosts_file:
        hosts_file.write(f"{ip_address}\t{domain}\n")

def change_hosts_file_permission():
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    os.chmod(hosts_path, 0o777)  # 修改hosts文件的权限

# 示例使用
domains = [
    "baiduapi2.bestmyself.live",
    "cloundcone.bestmyself.live",
    "yyds.bestmyself.live",
    "jp-tok.prod.surfshark.com",
    "hk-hkg.prod.surfshark.com",
    "jp-tok.prod.surfshark.com",
    "surfshark.com",
    "hk-hkg.prod.surfshark.com",
    "sg-sng.prod.surfshark.com",
    "us-jfk.prod.surfshark.com",
    "de-fra.prod.surfshark.com",
    "uk-lon.prod.surfshark.com",
    "ca-tor.prod.surfshark.com",
    "au-syd.prod.surfshark.com",
    "fr-par.prod.surfshark.com",
    "it-mil.prod.surfshark.com",
    "es-mad.prod.surfshark.com",
    "nl-ams.prod.surfshark.com",
    "se-sto.prod.surfshark.com",
    "ch-zur.prod.surfshark.com",
    "no-osl.prod.surfshark.com"
]

change_hosts_file_permission()  # 修改hosts文件的权限

for domain in domains:
    ip_address = dns_query(domain)
    if ip_address:
        write_to_hosts_file(domain, ip_address)
        print(f"成功解析 {domain} 为 {ip_address}")
    else:
        print(f"无法解析 {domain}")

