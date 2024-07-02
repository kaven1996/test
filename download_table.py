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
    
    tables = soup.find_all('table')
    
    if not tables:
        raise Exception('No tables found on the page')
    
    for table in tables:
        headers = [header.text for header in table.find_all('th')]
        rows = table.find_all('tr')
        
        data = []
        for row in rows:
            columns = row.find_all('td')
            if columns:
                data.append([column.text for column in columns])
        
        if headers and data:
            return headers, data
    
    raise Exception('All tables are empty')

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
