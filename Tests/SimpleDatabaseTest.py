import unittest
from main import *


class MyTestCase(unittest.TestCase):
    def is_not_empty(self):
        self.assertFalse(len(stop_data_dict) == 0)


if __name__ == '__main__':
    unittest.main()
