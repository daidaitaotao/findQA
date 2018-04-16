import logging
from findQA.data_access_services.TesterDAO import TesterDAO
from findQA.data_access_services.TesterSQLDAO import TesterSQLDAO


class TesterAService(object):
    """
        Application service designed to retrieve tester data
    """

    @staticmethod
    def get_testers(countries=None, devices=None):
        """
            retrieving tester records based on given countries and devices
            @param countries: a list of country codes or None if use all countries
            @type countries: list or None
            @param devices: a list of devices' descriptions or None if use all devices
            @type devices: list or None
            @rtype: tuple
        """
        assert isinstance(countries, list) or countries is None, type(countries)
        assert isinstance(devices, list) or devices is None, type(list)
        assert countries is None or len(countries) > 0
        assert devices is None or len(devices) > 0

        if countries:
            for country in countries:
                if len(country) > 2:
                    TesterAService.__LOGGER.warning("invalid country code {0}".format(country))
                    return

        return TesterDAO.get_testers_sorted_by_bugs_count(
            countries,
            devices,
        )

    __LOGGER = logging.getLogger(__name__)
    """ logger for the current class """
