import json
from string import Template
from typing import List, Dict, Union
from .api import BaseApi

class Subway(BaseApi):
    URL_BASE = 'https://ptx.transportdata.tw/MOTC/' 

    DATA = {
    '_operators' : 'v2/Rail/Operator/',
    'lines': 'v2/Rail/Metro/Network/',
    'shape': 'v2/Rail/Metro/Shape/',
    'station': 'v2/Rail/Metro/Station/',
    'frequency': 'v2/Rail/Metro/Frequency/',
}
    def __init__(self, app_id, app_key, operator=None):
        super().__init__(app_id, app_key)
        self.operator = operator
    
    def list_data(self) -> str:
        return [l for l in list(self.DATA.keys()) if not l[0]=='_']
    
    def list_operators(self) -> str:
        data = self.get('_operators')
        return list(d['OperatorID'] for d in data)

    def get(self, data_key:str, operator:str=None) -> Union[List, Dict]:
        if data_key not in self.DATA:
            raise Exception(f"Field '{data_key}'' not in the list of available data")
        operator = operator or self.operator or ''
        url = self.URL_BASE + self.DATA.get(data_key) + operator
        return self.execute(url)


## Example testing code

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    OPE = 'TRTC'
    subway = Subway(os.environ['APP_ID'], os.environ['APP_KEY'], OPE)
    print(subway.list_data())
    print(subway.operator)
    print(subway.get('lines'))