#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 20:41:42 2019

@author: hugues
"""
import os
from typing import List
from api import BaseApi

class Motc(BaseApi):
    URL_BASE = 'https://ptx.transportdata.tw/MOTC/' 
    CATEGORY = {
        'subway':'v2/Rail/Metro/'
    }
    
    FIELDS = {
        'lines':'Network/',
        'shape': 'Shape/',
        'station': 'Station/',
        'frequency': 'Frequency/',
    }

    OPTIONS = {
        'subway': {
            'operator': {
                'trtc': 'TRTC'}
        }
    }


    def __init__(self, app_id:str, app_key:str, category:str):
        super().__init__(app_id, app_key)
        self.category = category
    
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value:str):
        value = value.lower()
        if value not in self.CATEGORY:
            raise ValueError(f"category must be in the following list [{', '.join(self.CATEGORY.keys())}]")
        self._category = value

    @category.getter
    def category(self):
        return self._category

    @property
    def operator(self):
        return self._operator
    
    @operator.getter
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value:str) -> None:
        if not value:
            if len(self.OPERATOR[self.category]) == 1:
                value = list(self.OPERATOR[self.category].keys())[0]
            else:
                raise ValueError("Please specify the operator for the category {self.category}")
        
        if value not in self.OPERATOR[self.category]:
            raise KeyError("Operator {operator} not valid for the category {self.category}")
        self._operator = value

    def get(self, field: str, operator=None):
        self.operator = operator
        operator_url = self.OPERATOR[self.category][self.operator]
        category_url = self.CATEGORY[self.category]
        field_url = self.FIELDS[field]
        url = os.path.join(self.URL_BASE, category_url, field_url, operator_url)
        print(url)
        return self.execute(url)

if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    load_dotenv()
    subway = Motc(os.environ['APP_ID'], os.environ['APP_KEY'], 'subway')
    print(subway.get('shape'))


    