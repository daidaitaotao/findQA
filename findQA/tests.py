import csv
import os
from django.test import TestCase
from findQA.models import Country
from findQA.models import Device
from findQA.models import Tester
from findQA.models import Bug
from findQA.models import Tester_Device
from findQA.ApplicationServices.TesterASerivice import TesterAService


class FindQATestCase(TestCase):
    """
        class to test <findQA.ApplicationServices.TesterASerivice.TesterAService#get_testers>
    """

    def setUp(self):
        script_path = os.path.dirname(__file__)
        country_file_path = script_path + '/../csv_data/country.csv'
        device_file_path = script_path + '/../csv_data/devices.csv'
        tester_file_path = script_path + '/../csv_data/testers.csv'
        bug_file_path = script_path + '/../csv_data/bugs.csv'
        tester_device_file_path = script_path + '/../csv_data/tester_device.csv'

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
                tester_entity = Tester.objects.get(tester_id=row['testerId'])
                device_entity = Device.objects.get(device_id=row['deviceId'])
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

    def test_all_countries_all_devices(self):
        """
           testing with all countries and devices selected
        """
        selected_testers = TesterAService.get_testers()
        all_bugs_count = Bug.objects.all().count()
        total_bugs = 0
        for tester_entity in selected_testers:
            total_bugs += tester_entity.experience

        self.assertEqual(total_bugs, all_bugs_count)

    def test_one_country_all_devices(self):
        """
            testing with one country selected
        """
        countries = ['US']
        selected_testers = TesterAService.get_testers(countries=countries)
        all_testers = Tester.objects.filter(country__country_code__in=countries).count()
        self.assertEqual(len(selected_testers), all_testers)

    def test_one_device_all_countries(self):
        """
            testing with one device selected
        """
        devices = ['Galaxy S3']
        selected_testers = TesterAService.get_testers(devices=devices)

        tester_id_list = set(i.tester_id for i in selected_testers)
        all_testers = Tester.objects.filter(bug__device_id__description__in=devices).distinct()
        self.assertEqual(len(selected_testers), len(all_testers))
        self.assertTrue(i.tester_id in tester_id_list for i in all_testers)

    def test_one_country_one_device(self):
        """
            testing with one country and one device selected
        """
        countries = ['US']
        devices = ['iPhone 4']
        selected_testers = TesterAService.get_testers(countries=countries,
                                                      devices=devices)
        for selected_tester in selected_testers:
            tester_id = selected_tester.tester_id

            expected_count = Bug.objects.filter(tester_id__tester_id=tester_id).filter(
                device_id__description__in=devices
            ).count()
            self.assertEqual(selected_tester.experience, expected_count)

    def test_unsupported_country_code(self):
        """
            testing with unsupported country code
        """
        countries = ['CH']
        selected_testers_count = TesterAService.get_testers(countries=countries).count()

        self.assertEqual(selected_testers_count, 0)

    def test_unsupported_device(self):
        """
            testing with unsupported device
        """
        devices = ['Pixel 2']
        selected_testers_count = TesterAService.get_testers(devices=devices).count()

        self.assertEqual(selected_testers_count, 0)

    def test_country_code_with_unsupported_country(self):
        """
            testing with country codes which contain unsupported country
        """
        countries = ['US', 'CH']
        selected_testers = TesterAService.get_testers(countries=countries)
        all_testers = Tester.objects.filter(country__country_code__in=countries).count()
        self.assertEqual(len(selected_testers), all_testers)

    def test_device_with_unsupported_device(self):
        """
            testing with devices which contain unsupported device
        """
        devices = ['Pixel 2', 'iPhone 4']
        selected_testers = TesterAService.get_testers(devices=devices)
        tester_id_list = set(i.tester_id for i in selected_testers)
        all_testers = Tester.objects.filter(bug__device_id__description__in=devices).distinct()
        self.assertEqual(len(selected_testers), len(all_testers))
        self.assertTrue(i.tester_id in tester_id_list for i in all_testers)




