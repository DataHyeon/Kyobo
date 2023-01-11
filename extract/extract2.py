import os
import sys
import re
import requests
import time
import subprocess
import multiprocessing
import pyperclip
import pandas as pd
import multiprocessing
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup

try:
    from tqdm import tqdm
except ImportError:
    subprocess.run(["pip", "install", "--upgrade", "tqdm"])
    from tqdm import tqdm

try:
    from scode import is_latest_version
    if not is_latest_version():
        raise ImportError
    from scode.util import *
except ImportError:
    subprocess.run(['pip', 'install', '--upgrade', 'scode'])
    from scode.util import *

try:
    from scode.selenium import *
except ImportError:
    subprocess.run(['pip', 'install', '--upgrade', 'scode'])
    from scode.selenium import *
    

# ===============================================================================
#                               Definitions
# ===============================================================================


def kyobo(cmdt_id):
    
    text = requests.get(f'https://product.kyobobook.co.kr/detail/{cmdt_id}').text
    # soup = BeautifulSoup(text, 'html.parser')
    try:
        # div_a = soup.select_one('div[class="author"] a')
        # href = div_a['href']
        
        chrcCode = re.findall('chrcCode=(\d+)', text)[0]
        
        address_2 = f'https://www.kyobobook.co.kr/api/gw/pub/onk/author/information?chrcCode={chrcCode}'

        json_2 = requests.get(address_2).json()
        
        chr_info = json_2['data']['chrcIntcCntt']
        
    except:
        chr_info = ''
        
    
    cond_df_2 = pd.DataFrame(data = {'saleCmdtId':[cmdt_id], 'chrcIntcCntt':[chr_info]})
    
    return cond_df_2
    
def run():
    df = pd.read_csv('./kyobo2.csv')
    df_2 = pd.DataFrame()

    input_list = df['saleCmdtId']

    with multiprocessing.Pool() as p:
        for val in tqdm(p.imap_unordered(kyobo, input_list, 16), total=len(input_list)):

            df_2 = pd.concat([df_2, val]).reset_index(drop=True)

    df_2.to_csv('./kyobo3_1.csv', index=False)
    
    
    

if __name__ == '__main__':
    run()