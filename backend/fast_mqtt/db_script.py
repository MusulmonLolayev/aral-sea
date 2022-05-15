
import django
from django.conf import settings as settings
from django.utils import timezone

import os
import sys
sys.path.append('../')


os.environ['DJANGO_SETTINGS_MODULE'] = f'config.settings'
django.setup()

from  main.models import WellToolData

def convert_valid_data(msg: dict) -> dict:
    msg['t'] = msg['t'].replace('/', '-')
    msg['t'] = msg['t'].replace(',', ' ')
    msg['t'] = '20' + msg['t']

    return msg

def add_row_well_data_too(msg: dict):
    
    msg = convert_valid_data(msg)

    well_tool_data = WellToolData()
    well_tool_data.imei = msg['i']
    well_tool_data.date_time = msg['t']
    well_tool_data.degree = float(msg['d']) / 10
    well_tool_data.salinity = float(msg['r']) / 10
    well_tool_data.temperature = float(msg['q']) / 10

    well_tool_data.save()


if __name__ == "__main__":
    # test
    msg = {'i': '867857033766218', 't': '22-05-15,06:45:18+00',
           'd': '01414', 'r': '00430', 'q': '00116'}
    add_row_well_data_too(msg)
