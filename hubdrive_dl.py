import re
import requests
from urllib.parse import urlparse

url = ""  # hubdrive url

crypt = "" # crypt cookie

'''
NOTE: [UNSTABLE] Needs more exception handling -_-
'''

# ==================================

def parse_info(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

def hubdrive_dl(url):
    client = requests.Session()
    client.cookies.update({'crypt': crypt})
    
    res = client.get(url)
    info_parsed = parse_info(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    
    data = { 'id': file_id }
    
    headers = {
        'x-requested-with': 'XMLHttpRequest'
    }
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except: return {'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url

    return info_parsed

# ==================================

print(hubdrive_dl(url))
