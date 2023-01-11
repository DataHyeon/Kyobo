import requests
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime
from bs4 import BeautifulSoup

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
def run():

    text = requests.get('https://product.kyobobook.co.kr/bestseller/store?').text
    soup = BeautifulSoup(text, 'html.parser')

    sel_list = soup.select('select[id="selListType"] option')
    period_list = [sel['value'] for sel in sel_list]

    column_list = ['prstRnkn','cmdtName','chrcName','ppbkRlseDate','rlseDate','inbukCntt','price','sapr','dscnRate','buyRevwNumc','buyRevwRvgr','revwEmtnKywrName','frmrRnkn','saleCmdtClstName','ymw', 'store_name', 'saleCmdtDvsnCode']

    li_store_list = soup.select('div[id="seoulStoreList"] li[class="store_item"]')
    df = pd.DataFrame()
    for li_store in li_store_list:
        store_id = li_store['data-value']
        store_name = li_store.select_one('button').text
        
        for period in period_list:
            json_ = requests.get(f'https://product.kyobobook.co.kr/api/gw/pub/pdt/best-seller/store-products?page=1&per=20&ymw={period}&codeWrth=00&strRdpCode={store_id}').json()
            
            print(f'{store_name} - {period}')
            
            con_df = pd.DataFrame(json_['data']['bestSeller'])
            con_df['store_name'] = store_name
            
            try:           
                df = pd.concat([df, con_df[column_list]]).reset_index(drop=True)
            
            except:
                continue

    df.to_csv('./kyobo.csv', index=False)


# ===============================================================================
#                            Program information
# ===============================================================================

__author__ = '임성현'
__requester__ = '요청자'
__registration_date__ = '230105'
__latest_update_date__ = '230105'
__version__ = 'v1.00'
__title__ = '교보문고'
__desc__ = '교보문고'
__changeLog__ = {
    'v1.00': ['Initial Release.'],
}

# ===============================================================================
#                                 Main Code
# ===============================================================================

if __name__ == '__main__':

    run()