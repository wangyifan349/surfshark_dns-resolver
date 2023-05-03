import re
import socket

def extract_port(bridge):
    match = re.search(r':(\d+)', bridge)#提取端口号的规则
    if match:
        return int(match.group(1))
    else:
        return None

def extract_ip(bridge):
    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', bridge)#提取ip4地址的规则
    if match:
        return match.group(1)
    else:
        return None

def test_bridge(bridge_ip, bridge_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置连接超时时间
        sock.settimeout(5)
        # 连接网桥
        sock.connect((bridge_ip, bridge_port))
        sock.close()
        # 返回True，表示网桥可用
        return True
    except Exception as e:
        # 连接失败，返回False
        return False

bridges = [] # 初始化一个列表来存储洋葱网桥
with open("bridges.txt", "r") as file: # 打开文件
    for line in file: # 遍历每一行
        match = re.search(r"obfs4.*", line) # 使用正则表达式找到所有以"obfs4"开头的行
        if match: # 如果匹配成功
            bridges.append(match.group()) # 将匹配到的内容添加到列表中

unique_bridges = list(set(bridges)) # 使用set()函数去重，然后转换为列表

# 检测网桥可用性，并将不可用网桥移至列表末尾
available_bridges = []
unavailable_bridges = []

for bridge in unique_bridges:
    bridge_ip = extract_ip(bridge)
    bridge_port = extract_port(bridge)
    if test_bridge(bridge_ip, bridge_port):
        available_bridges.append(bridge)
    else:
        unavailable_bridges.append(bridge)

# 按端口号排序
sorted_available_bridges = sorted(available_bridges, key=extract_port)
# 将端口号为443或80的桥移到列表前面
sorted_available_bridges = [bridge for bridge in sorted_available_bridges if ':443' in bridge or ':80' in bridge] + \
                           [bridge for bridge in sorted_available_bridges if ':443' not in bridge and ':80' not in bridge]

sorted_bridges = sorted_available_bridges + ['--------------'] + unavailable_bridges

with open("bridges.txt", "w") as file: # 打开文件以覆盖写入模式
    file.write("\n".join(sorted_bridges)) # 使用"\n"将列表中的元素连接成字符串，然后写回到文件中

print("总共找到洋葱网桥数量:", len(bridges)) # 输出找到的洋葱网桥总数
print("去重后洋葱网桥数量:", len(unique_bridges)) # 输出去重后的洋葱网桥数量
print("可用洋葱网桥数量:", len(available_bridges)) # 输出可用的洋葱网桥数量
