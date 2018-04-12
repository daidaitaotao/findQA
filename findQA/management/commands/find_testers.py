import logging

from django.core.management.base import BaseCommand
from findQA.ApplicationServices.TesterASerivice import TesterAService

OPTION_ALL = ['ALL']
""" option select all """


class Command(BaseCommand):
    """ command that help users to search testers by country and device """
    help = 'Find all testers who live in countries and use devices by given parameters.'

    def add_arguments(self, parser):
        # Positional argument
        parser.add_argument('-c',
                            '--country',
                            nargs='+',
                            default=OPTION_ALL,
                            help=("Country codes that you will be using to search tester, a comma-separated"
                                 "list of country code, such as -c US,JP. If you wish to search by all"
                                 "countries, use 'ALL'(by default). "
                                 "Currently supported countries are: US, GB, and JP"))
        parser.add_argument('-d',
                            '--device',
                            nargs='+',
                            default=OPTION_ALL,
                            help=("Device names that you will be using to search tester, a comma-separated"
                                 "list of device descriptions, such as -d iPhone 4,iPhone 4S. If you wish"
                                 "to search by all devices, use 'ALL'(by default). "
                                 "Currently supported devices are: 'iPhone 4', 'iPhone 4S', 'iPhone 5', 'Galaxy S3',"
                                 " 'Galaxy S4', 'Nexus 4', 'Droid Razor', 'Droid DNA', 'HTC One', and 'iPhone 3'."
                                  ))

    def handle(self, *args, **options):
        countries = options['country']
        devices = options['device']

        # assign default values
        countries_list = None
        devices_list = None

        if countries != OPTION_ALL:
            countries_list = list(set(countries[0].split(',')))

        if devices != OPTION_ALL:
            devices_list = list(set(devices[0].split(',')))

        result = TesterAService.get_testers(
            countries=countries_list,
            devices=devices_list)

        for i in result:
            print(','.join([i.first_name, i.last_name, i.country.country_code, str(i.experience)]))

        self.stdout.write(self.style.SUCCESS('Finished searching testers by given country(s) and device(s)!'))

    __LOGGER = logging.getLogger(__name__)
    """ logger for the current class """
