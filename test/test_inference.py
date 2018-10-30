import unittest
import sys
from os.path import dirname, abspath
sys.path.insert(0, '../models/r_net')
from r_net import inference
parent_dir = dirname(abspath(__file__))

# the test cases for database
class database_test_cases(unittest.TestCase):
    def setUp(self):
        self.com_default = 1




if __name__ == '__main__':
    unittest.main()
