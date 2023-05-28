import re 
import socket
from concurrent.futures import ThreadPoolExecutor
def extract_port(bridge):# 定义函数使用正则表达式从 bridge 字符串中提取端口号
    match = re.search(r':(\d+)', bridge)
    if match:
        return int(match.group(1))
    else:
        return None
def extract_ip(bridge):# 定义函数使用正则表达式从 bridge 字符串中提取 IP 地址
    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', bridge)
    if match:
        return match.group(1)
    else:
        return None


def test_bridge(bridge_ip, bridge_port):# 定义函数测试洋葱网桥是否可用
    try:   
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# 创建一个新 socket 对象并设置超时时间为 5 秒
        sock.settimeout(5)
        sock.connect((bridge_ip, bridge_port))# 尝试连接到洋葱网桥
        sock.close()
        return True# 如果连接成功（即洋葱网桥可用），返回 True
    except Exception as e:
        return False# 如果连接失败（即洋葱网桥不可用），返回 False

bridges = [] # 初始化一个空列表来存储洋葱网桥

# 打开 bridges.txt 文件进行读取，并循环遍历每一行
with open("bridges.txt", "r") as file:
    for line in file:
        # 使用正则表达式找到所有以 "obfs4" 开头的行
        match = re.search(r"obfs4.*", line)
        if match: # 如果匹配成功
            bridges.append(match.group()) # 将匹配到的内容添加到洋葱网桥列表中

# 使用 set() 函数去重，然后转换为列表
unique_bridges = list(set(bridges))

# 检测洋葱网桥可用性，并将不可用网桥移至一个新的列表末尾
available_bridges = []
unavailable_bridges = []

# 创建线程池
pool = ThreadPoolExecutor(max_workers=50)  # 设置合适的线程数量

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
port_80_443_bridges = []  # 存储端口号为 443 或 80 的洋葱网桥
other_bridges = []  # 存储其他洋葱网桥

# 根据端口号分离洋葱网桥
for bridge in sorted_available_bridges:
    if ":443" in bridge or ":80" in bridge:
        port_80_443_bridges.append(bridge)
    else:
        other_bridges.append(bridge)

sorted_available_bridges = port_80_443_bridges + other_bridges# 将端口号为 443 或 80 的洋葱网桥放在列表前面，然后是其他洋葱网桥


# 将可用和不可用的洋葱网桥按照分界线组合成一个新的列表
sorted_bridges = sorted_available_bridges + ['--------------'] + unavailable_bridges

# 打开 bridges.txt 文件进行写入，覆盖原有内容
with open("bridges.txt", "w") as file:
    file.write("\n".join(sorted_bridges)) # 使用 "\n" 将列表中的元素连接成字符串，然后写回到文件中

# 输出找到的洋葱网桥总数，以及去重后、可用和不可用的洋葱网桥数量
print("总共找到洋葱网桥数量:", len(bridges))
print("去重后洋葱网桥数量:", len(unique_bridges))
print("可用洋葱网桥数量:", len(available_bridges))
