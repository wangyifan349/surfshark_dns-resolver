import os
import re
import socket
from dns import resolver, exception
import shutil


# 将文件拷贝到指定目录，如果文件已存在则删除
def copy_file_with_overwrite(source_path, target_path):
    if os.path.exists(target_path):
        os.remove(target_path)
    shutil.copy(source_path, target_path)
    print(f"已拷贝文件到 {target_path}")






    
# 获取指定目录中的所有 .ovpn 文件
def get_ovpn_files(directory):
    ovpn_files = []

    items = os.listdir(directory)

    for item in items:
        item_path = os.path.join(directory, item)

        if os.path.isfile(item_path) and item.lower().endswith('.ovpn'):
            ovpn_files.append(item_path)
        elif os.path.isdir(item_path):
            ovpn_files.extend(get_ovpn_files(item_path))

    return ovpn_files

# 使用 dnspython 解析域名到 IP 地址
def resolve_to_ip_with_dnspython(domain, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            dns_resolver = resolver.Resolver()
            answer = dns_resolver.resolve(domain, "A")
            return str(answer[0].address)
        except (exception.DNSException, IndexError):
            attempts += 1
    return None

# 将域名替换为 IP 地址并返回新的配置内容
def replace_domains_with_ips(content):
    matches = re.findall(r'(?i)(?:remote|proto)\s+(\S+)\s+(\d+)', content)
    new_content = content
    for match in matches:
        domain_or_ip, port = match
        ip = resolve_to_ip_with_dnspython(domain_or_ip)
        if ip:
            new_content = new_content.replace(f"{domain_or_ip} {port}", f"{ip} {port}")
    return new_content

# 主函数
def main():
    target_directory = "/home/wangyifan/下载/openvpn"  # 请替换为您的目标目录

    if os.path.isdir(target_directory):
        ovpn_files_list = get_ovpn_files(target_directory)
        if ovpn_files_list:
            print("找到以下 .ovpn 文件：")
            for idx, ovpn_file in enumerate(ovpn_files_list, start=1):
                print(f"{idx}. {ovpn_file}")

            for ovpn_file in ovpn_files_list:
                with open(ovpn_file, 'r') as file:
                    content = file.read()
                    new_content = replace_domains_with_ips(content)
                
                # 获取协议类型
                protocol_match = re.search(r'(?i)proto\s+(\S+)', new_content)
                if protocol_match:
                    protocol = protocol_match.group(1).lower()
                    if protocol == "tcp":
                        target_protocol_directory = os.path.join(target_directory, "tcp")
                    elif protocol == "udp":
                        target_protocol_directory = os.path.join(target_directory, "udp")
                    else:
                        print(f"未知协议类型: {protocol}")
                        continue

                    # 拷贝文件到对应的协议文件夹
                    target_filename = os.path.basename(ovpn_file)
                    target_path = os.path.join(target_protocol_directory, target_filename)
                    copy_file_with_overwrite(ovpn_file, target_path)
                
                # 更新文件内容并保存
                with open(ovpn_file, 'w') as file:
                    file.write(new_content)
                
                print(f"已替换 {ovpn_file} 中的域名为 IP 地址，并拷贝到协议文件夹。")
if __name__ == "__main__":
    main()
