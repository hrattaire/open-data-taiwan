# -*- coding: utf-8 -*-
import boto3
import os
from utils import (
    to_map,
    clean_null,
)
import uuid

from config import(
    apis,
    tables,
    cities,
)
import sqlalchemy
from datetime import datetime
from motc_api import ApiRequest


def update_stations(city, api='stations', engine, meta):
    # Init
    app_id = os.environ['APP_ID']
    app_key = os.environ['APP_KEY']

    # Api Call
    a = ApiRequest(app_id=app_id,
                   app_key=app_key)
    url = apis[api] + cities[city]
    request_response = a.execute(url=url)

    # Pre-process data to match table schema
    for d in request_response:
        d['station_uid'] = d['StationUID']
        d['station_id'] = d['StationID']
        d['authority_id'] = d['AuthorityID']
        d['station_name_en'] = d['StationName']['En']
        d['station_name_zh'] = d['StationName']['Zh_tw']
        d['lat'] = d['StationPosition']['PositionLat']
        d['long'] = d['StationPosition']['PositionLon']
        d['long'] = d['StationPosition']['PositionLon']
        d['station_address_en'] = d['StationAddress']['En']
        d['station_address_zh'] = d['StationAddress']['Zh_tw']
        d['bikes_capacity'] = d['BikesCapacity']
        d['src_update_time'] = d['SrcUpdateTime']
        d['update_time'] = d['UpdateTime']

    # Write into RDS

    try:
        table = meta.tables[tables[api]]
        engine.execute(table.insert(), request_response)
    except Exception as e:
        raise e


def update_availability(city, api='available'):
    # Init
    app_id = os.environ['APP_ID']
    app_key = os.environ['APP_KEY']

    # Api Call
    a = ApiRequest(app_id=app_id,
                   app_key=app_key)
    url = apis[api] + cities[city]
    request_response = a.execute(url=url)

    # Pre process before writing into RDS
    for d in request_response:
        d['id'] = uuid.uuid4().__str__()
        d['station_uid'] = d['StationUID']
        d['station_id'] = d['StationID']
        d['service_available'] = d['ServiceAvailable']
        d['available_bikes'] = d['AvailableRentBikes']
        d['available_returns'] = d['AvailableReturnBikes']
        d['src_update_time'] = d['SrcUpdateTime']
        d['update_time'] = d['UpdateTime']

    # Write into RDS
    try:
        table = meta.tables[tables[api]]
        engine.execute(table.insert(), request_response)
    except Exception as e:
        raise e
    return {'status':'200', 'body':'Data pushed to Dynamodb'}

if __name__ == '__main__':
    city = 'taipei'
