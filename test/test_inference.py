import unittest
import os
from os.path import dirname, abspath
parent_dir = dirname(dirname(abspath(__file__)))

# the test cases for database
class database_test_cases(unittest.TestCase):
    def setUp(self):
        self.com_default = 'python {}/models/r_net/inference.py --inference-mode default'.format(parent_dir)

    def test_infer(self):
        res = os.popen(self.com_default).read()
        print(res)

if __name__ == '__main__':
    unittest.main()
