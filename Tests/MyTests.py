import unittest

from constants import Request
from file import YandexApiRequestFile


class MyTestCase(unittest.TestCase):
    def test_yandex_get_stop_info(self):
        try:
            YandexApiRequestFile(Request.GET_STOP_INFO, '732').write_obtained_data()
        except Exception as e:
            self.fail(str(e))

    def test_yandex_get_line(self):
        try:
            YandexApiRequestFile(Request.GET_LINE, '732').write_obtained_data()
        except Exception as e:
            self.fail(str(e))


if __name__ == '__main__':
    unittest.main()
