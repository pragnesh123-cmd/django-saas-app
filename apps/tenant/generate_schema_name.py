import string
import random


class Schema:
    def __init__(self) -> None:
        pass

    def generate_schema_name(self):
        # initializing size of string
        N = 7
        # using random.choices()
        # generating random strings
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=N))
