"""
sends data to Openhab 1.x or any other server via a REST webservice
"""
import http.client
from typing import List
from Register import Register
from logger import ResultLogger


class OpenhabLogger(ResultLogger):
    def __init__(self, server_url="localhost", server_port=8080):
        self.server_url = server_url
        self.server_port = server_port
        ResultLogger.__init__(self)

    def log(self, results: List[Register]):
        for register in results:
            v = register.get_openhab_value()
            if v is not None:  # don't send None-Values! Only valid values
                self._send_value(register.get_openhab_name(), v)

    def _send_value(self, item, value):
        # debug
        # print("PUT", "/rest/items/" + item + "/state", str(value).encode('utf-8'))

        conn = http.client.HTTPConnection(self.server_url, self.server_port)
        conn.request("PUT", "/rest/items/" + item + "/state", str(value).encode('utf-8'))
        conn.close()
