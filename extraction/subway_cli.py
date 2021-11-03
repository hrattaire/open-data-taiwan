import json
import os
import click
from urllib.parse import parse_qs, urlparse
from apis.subway import Subway
from typing import List, Dict, Union, Tuple
from dotenv import load_dotenv

@click.group()
def subway():
    pass

@subway.command('list-data')
def list_data():
    app_id = os.getenv('APP_ID')
    app_key = os.getenv('APP_KEY')
    subway = Subway(app_id, app_key)
    click.echo(f"Available informations are {', '.join(subway.list_data())}")

@subway.command('list-operators')
def list_data():
    app_id = os.getenv('APP_ID')
    app_key = os.getenv('APP_KEY')
    subway = Subway(app_id, app_key)
    click.echo(f"Available opeators are {', '.join(subway.list_operators())}")

@subway.command('export-json')
@click.argument('fields', nargs=-1)
@click.option("--operator", default=None, help="Operator code", type=click.Choice(['TRTC', 'KRTC', 'NTMC', 'TMRT', 'TYMC'], case_sensitive=False))
@click.option("--directory", default=None, help="Json files directory", type=click.Path())
def subway_export(fields: Tuple, operator:str, directory:str):
    click.echo('Start exporting subway data...')
    # Instanciate subway
    app_id = os.getenv('APP_ID')
    app_key = os.getenv('APP_KEY')
    subway = Subway(app_id, app_key, operator=operator)

    # Collect data
    results = dict()
    if not fields:
        l_fields = subway.list_data()
    else:
        l_fields = list(fields)
    for l in l_fields:
        results[l] = subway.get(l,operator=operator)

    # Export in json
    os.makedirs(directory, exist_ok=True)
    for r in results:    
        path = os.path.join(directory, f"{r}_{operator}.json")
        save_json(results[r], path)
    click.echo(f'Data exported in JSON format to directory {directory}')

#cli.add_command(subway)
# cli subway --driver json --dir data/
# def extract_fields(data_path:str) -> Tuple[str, str, List]:
#     """ Extract Type of data, Operator and Fields from the path 
#         Format: Type_data/Fields
#         >>> extract_fields("Subway?fields=lines,shape,truc")
#         ('Subway', 'TRTC', ['lines', 'shape', 'truc'])
#     """
#     l_data = urlparse(data_path)
#     # Manage operators and data_type
#     data_type, operators, *_, = l_data.path.split('/') 

#     # Get list of fields
#     d_fields = parse_qs(l_data.query)
#     if not 'fields' in d_fields:
#         raise ValueError(f'No fields parameters found in the argument {data_path}') 
#     fields = d_fields['fields'][0].replace(' ','').split(',')

#     return (data_type, operators, fields)

def save_json(data:Union[List, Dict], filename:str) -> int:
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=15)
    return 0

if __name__ == "__main__":
    load_dotenv()
    subway()

    