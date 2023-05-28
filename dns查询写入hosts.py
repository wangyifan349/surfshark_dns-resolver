import requests
import os
import platform
import concurrent.futures
print("请确保hosts可以被修改，拥有修改的权限")
print("这部分代码利用hosts修改了DNS污染问题，防止DNS污染。")
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

def get_hosts_path():#根据系统类型，返回hosts的位置。
    system = platform.system()
    if system == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    elif system == "Linux" or system == "Darwin":
        return "/etc/hosts"
    else:
        raise Exception("Unsupported operating system")

def write_to_hosts_file(domain, ip_address):
    hosts_path = get_hosts_path()

    with open(hosts_path, "a") as hosts_file:
        hosts_file.write(f"{ip_address}\t{domain}\n")

def change_hosts_file_permission():
    hosts_path = get_hosts_path()
    os.chmod(hosts_path, 0o777)  # 修改hosts文件的权限，Windows下请确保那个文件可以被修改哦。

def resolve_domain(domain):
    ip_address = dns_query(domain)
    if ip_address:
        write_to_hosts_file(domain, ip_address)
        print(f"成功解析 {domain} 为 {ip_address}")
    else:
        print(f"无法解析 {domain}")

# 示例使用
domains = [
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
    "no-osl.prod.surfshark.com",
    "kr-seo.prod.surfshark.com",
    "my-kul.prod.surfshark.com",
    "kh-pnh.prod.surfshark.com",
    "my.surfshark.com"
]


unique_domains = set(domains)
unique_domains = list(unique_domains)
domains=unique_domains    #去重
change_hosts_file_permission()  # 修改hosts文件的权限

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = []  # 存储任务结果的列表
    for domain in domains:
        task = executor.submit(resolve_domain, domain)  # 提交任务给线程池执行
        results.append(task)  # 将任务对象添加到结果列表中

for result in concurrent.futures.as_completed(results):# 获取查询结果
    try:
        result.result()  # 等待任务完成并获取结果
    except Exception as e:
        print(f"查询出错：{str(e)}")

print("全部查询完毕，并写入hosts文件中了")
