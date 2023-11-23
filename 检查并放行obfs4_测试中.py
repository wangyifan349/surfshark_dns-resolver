import re,os
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor
ufw_rule = f"sudo ufw disable"
subprocess.run(ufw_rule, shell=True)#禁止防火墙，如果不禁止，就没法测试了。不过也可能已经关闭了。

def extract_port(bridge):
    """从Tor网桥字符串中提取端口号"""
    match = re.search(r':(\d+)', bridge)
    if match:
        return int(match.group(1))
    else:
        return None

def extract_ip(bridge):
    """从Tor网桥字符串中提取IP地址"""
    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', bridge)
    if match:
        return match.group(1)
    else:
        return None

def test_bridge(bridge_ip, bridge_port):
    """测试Tor网桥是否可用"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((bridge_ip, bridge_port))
        sock.close()
        return True
    except Exception as e:
        return False

bridges = []

# 打开 bridges.txt 文件进行读取，并循环遍历每一行
with open("bridges.txt", "r") as file:
    for line in file:
        # 使用正则表达式找到所有以 "obfs4" 开头的行
        match = re.search(r"obfs4.*", line)
        if match:
            bridges.append(match.group())

# 使用 set() 函数去重，然后转换为列表
unique_bridges = list(set(bridges))

# 检测洋葱网桥可用性，并将不可用网桥移至一个新的列表末尾
available_bridges = []
unavailable_bridges = []

# 创建线程池
pool = ThreadPoolExecutor(max_workers=50)

# 定义任务函数
def check_bridge(bridge):
    bridge_ip = extract_ip(bridge)
    bridge_port = extract_port(bridge)
    if test_bridge(bridge_ip, bridge_port):
        available_bridges.append(bridge)
    else:
        unavailable_bridges.append(bridge)

# 提交任务给线程池
for bridge in unique_bridges:
    pool.submit(check_bridge, bridge)

# 等待所有任务完成
pool.shutdown(wait=True)

# 按端口号排序
sorted_available_bridges = sorted(available_bridges, key=extract_port)

# 将端口号为 443 或 80 的洋葱网桥移到列表前面
port_80_443_bridges = []
other_bridges = []

# 根据端口号分离洋葱网桥
for bridge in sorted_available_bridges:
    if ":443" in bridge or ":80" in bridge:
        port_80_443_bridges.append(bridge)
    else:
        other_bridges.append(bridge)

sorted_available_bridges = port_80_443_bridges + other_bridges

# 将可用和不可用的洋葱网桥按照分界线组合成一个新的列表
sorted_bridges = sorted_available_bridges + ['--------------'] + unavailable_bridges

# 打开 bridges.txt 文件进行写入，覆盖原有内容
with open("bridges.txt", "w") as file:
    file.write("\n".join(sorted_bridges))

# 输出找到的洋葱网桥总数，以及去重后、可用和不可用的洋葱网桥数量
print("总共找到洋葱网桥数量:", len(bridges))
print("去重后洋葱网桥数量:", len(unique_bridges))
print("可用洋葱网桥数量:", len(available_bridges))

"""这部分代码尝试获取权限情况，进行放行这些规则，并启用UFW"""

def has_root_permissions():
    # 尝试在 /root 中创建一个目录（需要 root 权限）来检查权限
    try:
        os.makedirs("/root/test_directory", exist_ok=True)
        os.rmdir("/root/test_directory")
        return True
    except PermissionError:
        return False

def add_ufw_rule(bridge_ip, bridge_port):
    # 列出已存在的规则
    existing_rules = subprocess.check_output("sudo ufw status numbered", shell=True).decode()
    # 检查规则是否已存在
    if f"allow out on wlp4s0 to {bridge_ip} port {bridge_port} proto tcp\n" in existing_rules:
        # 如果规则已存在，先删除它
        subprocess.run(f"sudo ufw delete allow out on wlp4s0 to {bridge_ip} port {bridge_port} proto tcp", shell=True)
    # 插入新规则到第一的位置
    ufw_rule = f"sudo ufw insert 1 allow out on wlp4s0 to {bridge_ip} port {bridge_port} proto tcp"
    subprocess.run(ufw_rule, shell=True)



    
ufw_rule = f"sudo ufw enable"
subprocess.run(ufw_rule, shell=True)#启用防火墙


if has_root_permissions():
    ufw_rule = f"sudo ufw enable"
    subprocess.run(ufw_rule, shell=True)#启用防火墙
    print("拥有足够的权限，尝试添加 UFW 规则：")
    for bridge in sorted_available_bridges:
        bridge_ip = extract_ip(bridge)
        bridge_port = extract_port(bridge)
        print(f"尝试添加规则允许 {bridge_ip}:{bridge_port} 的 TCP 连接")
        add_ufw_rule(bridge_ip, bridge_port)
else:
    print("没有足够的权限来添加 UFW 规则。")
ufw_rule = f"sudo ufw reload"
subprocess.run(ufw_rule, shell=True)#启用规则


print("已添加通过SOCKS5测试的Tor网桥到UFW规则（置顶）。")
