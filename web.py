import os
import requests
import urllib
from pathlib import Path
from requests_html import HTMLSession

STORAGE_DIR=os.path.join(Path.home(), "tmp")

def get_page(url):
    html_file = os.path.join(STORAGE_DIR,f'{os.path.basename(url)}.html')

    print(f'url: {url} => {html_file}')
    if os.path.exists(html_file):
        print("Use local file")
        response = urllib.request.urlopen('file://' + html_file, timeout=1)
        html = response.read()
        return html
    else:    
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }
        try:
            session = HTMLSession()
            response = session.get(url)
            with open(html_file, 'wb') as f:
                f.write(response.content)
            return response.content
        except requests.exceptions.RequestException as e:
            print(e)
