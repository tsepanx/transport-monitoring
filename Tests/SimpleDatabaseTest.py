import unittest
from main import *


class MyTestCase(unittest.TestCase):
    def test_is_not_empty(self):
        self.assertFalse(len(stop_data_dict) == 0)

    


if __name__ == '__main__':
    unittest.main()
