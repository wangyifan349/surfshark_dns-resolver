import requests
import os
import platform
import concurrent.futures

print("请确保hosts可以被修改，拥有修改的权限")
print("这部分代码利用hosts修改了DNS污染问题，防止DNS污染。")

def load_hosts_file():
    hosts_path = get_hosts_path()  # 获取hosts文件的路径
    # 创建一个空字典来存储hosts条目
    hosts_dict = {}
    with open(hosts_path, "r") as hosts_file:
        for line in hosts_file:  # 遍历文件中的每一行
            line = line.strip()  # 去除行首和行尾的空格
            if not line or line.startswith("#"):  # 忽略空行和注释（以"#"开头的行）
                continue
            parts = line.split()  # 根据空格将行分割成多个部分
            if len(parts) >= 2:  # 检查行是否至少有两个部分
                ip, domain = parts[:2]  # 提取行中的IP地址和域名
                hosts_dict[domain] = ip  # 将域名和IP地址添加到hosts字典中
    return hosts_dict  # 返回填充后的hosts字典

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
            if answer["type"] == 1:  # A记录类型
                ip_address = answer["data"]
                return ip_address
    return None

def get_hosts_path():  # 根据系统类型，返回hosts的位置。
    system = platform.system()
    if system == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    elif system == "Linux" or system == "Darwin":
        return "/etc/hosts"
    else:
        raise Exception("不支持的操作系统")

def write_to_hosts_file(hosts_dict):
    hosts_path = get_hosts_path()
    with open(hosts_path, "w") as hosts_file:
        for domain, ip in hosts_dict.items():
            hosts_file.write(f"{ip}\t{domain}\n")

def change_hosts_file_permission():
    hosts_path = get_hosts_path()
    os.chmod(hosts_path, 0o777)  # 修改hosts文件的权限，Windows下请确保该文件可以被修改

def resolve_domain(domain, hosts_dict):
    ip_address = dns_query(domain)
    if ip_address and (domain not in hosts_dict or hosts_dict[domain] != ip_address):
        hosts_dict[domain] = ip_address  # 更新字典中的条目
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
    "ux.surfshark.com",
    "in.appcenter.ms",
    "cdn.ss-cdn.com",
    "download.surfshark.com",
    "in.appcenter.ms"
]

unique_domains = set(domains)
unique_domains = list(unique_domains)
domains = unique_domains  # 去重
change_hosts_file_permission()  # 修改hosts文件的权限
hosts_dict = load_hosts_file()  # 加载hosts文件到字典

retry_limit = 3  # 最大重试次数

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = []  # 存储任务结果的列表
    for domain in domains:
        retry_count = 0
        while retry_count < retry_limit:
            task = executor.submit(resolve_domain, domain, hosts_dict)  # 提交任务给线程池执行
            results.append(task)  # 将任务对象添加到结果列表中
            retry_count += 1

for result in concurrent.futures.as_completed(results):  # 获取查询结果
    try:
        result.result()  # 等待任务完成并获取结果
    except Exception as e:
        print(f"查询出错：{str(e)}")

write_to_hosts_file(hosts_dict)  # 使用新的字典内容覆盖hosts文件
print("全部查询完毕，并写入hosts文件中了")
