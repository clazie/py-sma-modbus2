"""
sends data to InfluxDB 1.x
"""

from typing import List
from Register import Register
from logger import ResultLogger
from influxdb import InfluxDBClient
# import json


class InfluxDBLogger(ResultLogger):
    def __init__(self, server_url="localhost", server_port=8086, user='admin', password='admin', database='openhab'):
        self.server_url = server_url
        self.server_port = server_port
        self.user = user
        self.password = password
        self.database = database
        ResultLogger.__init__(self)

    def log(self, results: List[Register]):
        j = []

        for register in results:
            j += register.get_JSON("PV")  # with multiple inverters change the name or add tags!

        # print(json.dumps(j, indent=4))

        client = InfluxDBClient(self.server_url, self.server_port, self.user, self.password, self.database)
        client.write_points(j)
