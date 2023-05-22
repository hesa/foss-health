import os
import requests
import urllib
from pathlib import Path
from requests_html import HTMLSession

from naive_foss_health.exception import NfhcException
from naive_foss_health.error import NETWORK_FAILURE
import logging

STORAGE_DIR=os.path.join(Path.home(), ".cache/nfhc")

def get_page(url):

    org = url.split("/")[3]
    repo = url.split("/")[4]

    repo_store = os.path.join(os.path.join(STORAGE_DIR, org), repo)

    if not os.path.exists(repo_store):
        os.makedirs(repo_store)
    
    html_file = os.path.join(repo_store, f'{os.path.basename(url)}.html')

    logging.debug(f'url: {url} => {html_file}')
    if os.path.exists(html_file):
        logging.info(f'Use local file for {url}: {html_file}')
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
            raise NfhcException(NETWORK_FAILURE, f'Could not download: {html_page}\nOriginal exception: {e}')
