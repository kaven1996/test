import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(url))
    
    return response.text

def parse_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # 这个部分根据实际的网页结构进行解析，这里假设是一个表格
    data = []
    table = soup.find('table')
    
    # 检查表格是否存在
    if not table:
        raise Exception('No table found on the page')
    
    # 提取表头
    headers = [header.text for header in table.find_all('th')]
    
    # 检查表头是否存在
    if not headers:
        raise Exception('No table headers found')
    
    # 提取表格行
    rows = table.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        if columns:
            data.append([column.text for column in columns])
    
    # 检查数据行是否存在
    if not data:
        raise Exception('No table rows found')
    
    return headers, data

def save_to_csv(headers, data, filename):
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(filename, index=False)

if __name__ == '__main__':
    url = 'https://example.com/your-table-page'  # 替换为实际的URL
    try:
        html = fetch_data(url)
        headers, data = parse_data(html)
        save_to_csv(headers, data, 'output.csv')
        print('Data saved to output.csv')
    except Exception as e:
        print('Error:', e)
