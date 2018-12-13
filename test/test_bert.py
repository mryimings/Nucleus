import sys
import unittest
from os.path import dirname, abspath

d = dirname(dirname(abspath(__file__)))
sys.path.append(d)
from models.bert.inference_bert import Inference

class database_test_cases(unittest.TestCase):
    def setUp(self):
        self.infe = Inference()

    def test(self):
        qas = {'question': "where is Stanford?",
               'context_list': ["Columbia University is in New York City.", "Stanford is in California.",
                                "Tongji is in Shanghai."]}
        res = self.infe.response(qas)
        self.assertTrue(len(res),9)


if __name__ == '__main__':
    unittest.main()