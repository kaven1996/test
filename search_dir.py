import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def list_directories(url):
    directories = []
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有链接，假设目录链接都以'/'结尾
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.endswith('/'):
                directories.append(href)

    except requests.RequestException as e:
        print(f"请求错误: {e}")
    
    return directories

def find_last_directory(url):
    directories = list_directories(url)
    if directories:
        # 假设最后一个目录在列表的最后一个位置
        return directories[-1]
    else:
        return "没有找到目录"

# 测试URL
base_url = "http://localhost/"
print("目录列表:", list_directories(base_url))
print("最后一层目录:", find_last_directory(base_url))
