import csv
import os
import sys
from findQA.models import Country
from findQA.models import Device
from findQA.models import Tester
from findQA.models import Bug
from findQA.models import Tester_Device

country_file_path = 'csv_data/country.csv'
device_file_path = 'csv_data/devices.csv'
tester_file_path = 'csv_data/testers.csv'
bug_file_path = 'csv_data/bugs.csv'
tester_device_file_path = 'csv_data/tester_device.csv'

# please do not change the import order
with open(country_file_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        country_entity = Country(name=row['name'], country_code=row['countryCode'])
        country_entity.save()

with open(device_file_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        device_entity = Device(device_id=row['deviceId'], description=row['description'])
        device_entity.save()

with open(tester_file_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        country_entity = Country.objects.get(country_code=row['country'])
        tester_entity = Tester(tester_id=row['testerId'],
                               first_name=row['firstName'],
                               last_name=row['lastName'],
                               country=country_entity,
                               lastLogin=row['lastLogin']
                               )
        tester_entity.save()

with open(bug_file_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tester_entity = Tester.objects.get(tester_id = row['testerId'])
        device_entity = Device.objects.get(device_id = row['deviceId'])
        bug_entity = Bug(bug_id=row['bugId'],
                         tester_id=tester_entity,
                         device_id=device_entity)
        bug_entity.save()

with open(tester_device_file_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tester_entity = Tester.objects.get(tester_id=row['testerId'])
        device_entity = Device.objects.get(device_id=row['deviceId'])
        tester_device_entity = Tester_Device(
            tester_id=tester_entity,
            device_id=device_entity)
        tester_device_entity.save()
