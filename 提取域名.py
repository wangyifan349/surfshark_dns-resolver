import re

def extract_and_sort_domains(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        # 使用正则表达式匹配域名的模式
        pattern = r'\b[A-Za-z0-9.-]+\.(?:com|net|org|edu|gov|mil|int|cn|co|uk|de|fr|jp|au|ru|br|it|nl|es|ca|eu|kr|se|ch|no|at|me|us)\b'

        # 使用findall函数找到所有匹配的域名
        domain_names = re.findall(pattern, text)

        # 去重并按照"a"在前、"z"在后的升序排列
        unique_domains = sorted(set(domain_names), key=lambda x: (x.startswith('a'), x.endswith('z')))

        return unique_domains

# 指定文件路径
file_path = 'config.json'

# 提取、去重并排序域名
sorted_domains = extract_and_sort_domains(file_path)

# 打印去重并排序后的域名
for domain in sorted_domains:
    print(domain)
