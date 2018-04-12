import datetime
import logging

from findQA.models import Country
from findQA.models import Device
from findQA.models import Tester
from findQA.models import Bug
from findQA.models import Tester_Device
from django.db.models import Q
from django.db.models import Count


class TesterDAO(object):
    """
        Data access service designed to retrieve tester data
    """

    @staticmethod
    def get_testers_sorted_by_bugs_count(
            countries=None,
            devices=None):
        """
            retrieving tester objects based on given countries and devices

            @param countries: a list of country codes or None if use all countries
            @type countries: list or None
            @param devices: a list of devices' descriptions or None if use all devices
            @type devices: list
            @rtype: tuple

            @precondition: len(countries) > 0
            @precondition: len(devices) > 0
        """
        assert isinstance(countries, list) or countries is None, type(countries)
        assert isinstance(devices, list) or devices is None, type(list)
        assert countries is None or len(countries) > 0
        assert devices is None or len(devices) > 0

        result = Tester.objects
        if countries:
            result = result.filter(
            country__country_code__in=countries)

        if devices:
            result = result.filter(tester_device__device_id__description__in=devices).annotate(
                experience=Count('bug', filter=Q(bug__device_id__description__in=devices))).order_by(
                '-experience')
        else:
            result = result.annotate(
                experience=Count('bug')).order_by('-experience')

        return result

    __LOGGER = logging.getLogger(__name__)
    """ logger for the current class """
