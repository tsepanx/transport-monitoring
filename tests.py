import unittest

from constants import Request
from main import YandexApiRequest


class MyTestCase(unittest.TestCase):
    def test_yandex_get_stop_info(self):
        try:
            YandexApiRequest(Request.GET_STOP_INFO, '732').run()
        except Exception as e:
            self.fail(str(e))

    def test_yandex_get_line(self):
        try:
            YandexApiRequest(Request.GET_LINE, '732').run()
        except Exception as e:
            self.fail(str(e))


if __name__ == '__main__':
    unittest.main()
