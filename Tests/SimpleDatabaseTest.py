import unittest
from main import *


class MyTestCase(unittest.TestCase):
    def test_is_not_empty(self):
        self.assertFalse(len(stop_data_dict) == 0)

    def test_mos_gor_trans_equals(self):
        self.maxDiff = None

        for i in TimetableFilter.ROUTES:
            for j in TimetableFilter.DAYS:
                bus = Bus(MAIN_BUS_NAME)
                l1 = set(bus.get_stops(i, j))
                l2 = set(list(bus.get_timetable(i, j)))
                self.assertEqual(l1, l2,
                                 msg=i + j +
                                 "\n\n\n" +
                                 "\n".join(map(str, l1)) +
                                 "\n\n\n" +
                                 "\n".join(map(str, l2)))


if __name__ == '__main__':
    unittest.main()
