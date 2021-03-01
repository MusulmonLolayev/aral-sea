from django.shortcuts import render
from django.http import HttpResponse

from pathlib import Path
import os

from .models import Farm, District, Well


def load(request):
    """from openpyxl import load_workbook

    BASE_DIR = Path(__file__).resolve().parent

    path = os.path.join(BASE_DIR, 'observed_wells.xlsx')
    workbook = load_workbook(filename=path)
    sheet = workbook.active

    err_count = 0

    districts = District.objects.all()

    farms = []

    for i in range(2, 3658):
        district = str(sheet['D' + str(i)].value).strip()
        farm_name = str(sheet['E' + str(i)].value).strip()

        found_farm = None
        for item in farms:
            if farm_name.lower() == item.name.lower():
                found_farm = item
                break
        
        if found_farm is None:
            found_farm = Farm()
            found_farm.name = farm_name
            
            for dist in districts:
                if dist.name.lower() == district.lower():
                    found_farm.district = dist
                    break
            
            found_farm.save()
            farms.append(found_farm)

        well = Well()

        well.number = str(sheet['c' + str(i)].value).strip()
        well.farm = found_farm
        well.x = float(str(sheet['f' + str(i)].value).strip().replace(',', '.'))
        well.y = float(str(sheet['g' + str(i)].value).strip().replace(',', '.'))
        val = str(sheet['h' + str(i)].value).strip()
        if val != '' and not (val is None):
            well.built_year = int(val)
        val = str(sheet['i' + str(i)].value).strip().replace(',', '.')
        if val != '' and not (val is None):
            well.depth = float(val)
        val = str(sheet['j' + str(i)].value).strip().replace(',', '.')
        if val != '' and not (val is None):
            well.diameter = float(val)
        if str(sheet['k' + str(i)].value).strip() == "полиэтилен":
            well.material = True
        else:
            well.material = False
        val = str(sheet['l' + str(i)].value).strip().replace(',', '.')
        if val != '' and not (val is None):
            well.area = float(val)
        val = str(sheet['m' + str(i)].value).strip().replace(',', '.')
        if val != '':
            well.label = float(val)

        print(i)
        well.save()
        
    print(err_count)"""

    return HttpResponse("Salom")
