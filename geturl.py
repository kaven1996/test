import requests
from bs4 import BeautifulSoup

def fetch_directory_structure(url, max_depth=3, current_depth=1):
    # 当前深度超过最大深度时停止递归
    if current_depth > max_depth:
        return {}
    
    directory = {}
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                # 过滤出有效的目录和文件链接
                if href and href.endswith('/') and not href.startswith('?') and not href.startswith('../'):
                    directory_name = href.rstrip('/')
                    sub_url = url.rstrip('/') + '/' + href
                    # 递归调用，增加当前深度
                    directory[directory_name] = fetch_directory_structure(sub_url, max_depth, current_depth + 1)
                elif href and not href.endswith('/') and not href.startswith('?') and not href.startswith('../'):
                    # 在字典中添加文件
                    directory[href] = "file"
    except requests.RequestException as e:
        print(f"Failed to access {url}: {str(e)}")
        return {}
    
    return directory

# 示例用URL，确保替换为你的实际Apache服务器地址
base_url = 'http://localhost/'
directory_structure = fetch_directory_structure(base_url, max_depth=3)
print(directory_structure)
