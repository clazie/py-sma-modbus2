import json
from typing import List

from pymodbus.exceptions import NotImplementedException

from Register import Register


class ResultLogger:
    def __init__(self):
        pass

    def log(self, results: List[Register]):
        for register in results:
            print(register)


class JsonLogger(ResultLogger):
    def __init__(self):
        ResultLogger.__init__(self)

    def log(self, results: List[Register]):
        raise NotImplementedException


class KeyValueLogger(ResultLogger):
    def __init__(self):
        ResultLogger.__init__(self)

    def log(self, results: List[Register]):
        for register in results:
            print(f"{register.name}={register.value}")


class TableLogger(ResultLogger):
    def __init__(self):
        ResultLogger.__init__(self)

    def log(self, results: List[Register]):
        max_len = max(len(r.name) for r in results)
        max_lenv = max(len(r.get_formattedValue()) for r in results)
        row_format = f"{{:<{max_len}}} = {{:<{max_lenv}}} ; {{}}"
        for register in results:
            print(row_format.format(register.name, register.get_formattedValue(), register.description))
