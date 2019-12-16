import unittest
from classes import *


class MyTestCase(unittest.TestCase):
    def test_db_fill(self):
        self.maxDiff = None

        path = PROJECT_PREFIX + MAIN_DB_FILENAME
        remove_if_exists(path)

        Database(BUSES_LIST).create()
        l = Database.get_filtered_rows_from_db("732", "Давыдковская улица, 10")
        print(*l)
        self.assertNotEqual(l, [])

        os.remove(path)


if __name__ == '__main__':
    unittest.main()
