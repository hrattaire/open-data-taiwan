import base64
import hmac
import json
from hashlib import sha1
from requests import request
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime

class BaseApi():
    """
    Class aims to provide MOTC API Config + Request 
    args:
        - app_id
        - app_key
    """
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.url = ''
        self.params = dict({'format':'JSON'})
        self.response = ''
        self.headers=''
        
        
    def add_params(self, param):
        if not param == {}:
            self.params.update(param)
        
    def execute(self, url, param={}):
        self.url = url
        self.add_params(param)
        self.headers=self._get_auth_header()
        response = request('get',
                           url=self.url,
                           params=self.params,
                           headers=self.headers)
        self.response = response.content.decode('utf-8')
        self.response = json.loads(self.response)
        return self.response
    
    def _get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }
    def __repr__(self):
        return json.dumps(vars(self))