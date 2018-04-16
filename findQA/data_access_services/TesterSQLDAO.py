from django.db import connection


class TesterSQLDAO(object):
    """
        Data access service designed to retrieve tester data
    """
    @staticmethod
    def my_custom_sql(countries=None, devices=None):
        """
            using raw sql to retrieve tester data based on countries and devices
            @type countries: None or list
            @type devices: None or list
            @rtype: list
        """
        assert countries is None or isinstance(countries, list)
        assert devices is None or isinstance(devices, list)

        base_query = """
            SELECT t.tester_id, t.first_name, t.last_name, t.country_code, count(b.bug_id) as experience
            From findQA_tester t join findQA_bug b
            on t.tester_id = b.tester_id
            join findQA_device d
            on b.device_id = d.device_id
        """

        where_clause = None
        if countries and devices:
            where_clause = """
            WHERE t.country_code in {0} and d.description in {1}
            """.format(
                '(' + ','.join(["'" + country + "'" for country in countries]) + ')',
                '(' + ','.join(["'" + device + "'" for device in devices]) + ')',
            )
        elif countries:
            where_clause = """
            WHERE t.country_code in {0}
            """.format(
                '(' + ','.join(["'" + country + "'" for country in countries]) + ')'
            )
        elif devices:
            where_clause = """
            WHERE d.description in {0}
            """.format(
                '(' + ','.join(["'" + device + "'" for device in devices]) + ')'
            )

        group_by_clause = """
            group by t.tester_id, t.first_name, t.last_name, t.country_code
            order by experience desc
        """

        if where_clause:
            query = base_query + ' ' + where_clause + ' ' + group_by_clause
        else:
            query = base_query + ' ' + group_by_clause
        print(query)

        cursor = connection.cursor()
        cursor.execute(query)
        rows = TesterSQLDAO.dictfetchall(cursor)
        print(rows)
        return rows

    @staticmethod
    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]