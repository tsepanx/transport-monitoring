import unittest
import os
from main import *


class MyTestCase(unittest.TestCase):

    def test_mos_gor_trans_funcs_equals(self):
        self.maxDiff = None

        for i in TimetableFilter.ROUTES:
            for j in TimetableFilter.DAYS:
                bus = Bus("732")
                l1 = set(bus.get_stops(i, j))
                l2 = set(list(bus.get_timetable(i, j)))
                self.assertEqual(l1, l2,
                                 msg=i + j +
                                     "\n\n\n" +
                                     "\n".join(map(str, l1)) +
                                     "\n\n\n" +
                                     "\n".join(map(str, l2)))

    def test_db_filter(self):
        rows = main_db.get_filtered_rows_from_db("732", STOP_732_ID)
        self.assertNotEqual(rows, [])

    # @unittest.skip
    def test_fill_db(self):
        path = PROJECT_PREFIX + "test.db"
        bus = "732"

        db = SqliteDatabase(path)
        c = Database(db, [bus],
                     _filter_routes=[TimetableFilter.ROUTE_AB],
                     _filter_days=[TimetableFilter.WORKDAYS])
        l = c.get_filtered_rows_from_db(bus, STOP_732_ID)
        self.assertNotEqual([], l)
        os.remove(path)

    def test_yandex_api_crash(self):
        try:
            x = proxy.get_stop_info("https://yandex.ru/maps/213/moscow/stops/stop__9644642/")
        except Exception:
            self.fail("Can't receive data from Yandex API")


if __name__ == '__main__':
    unittest.main()
