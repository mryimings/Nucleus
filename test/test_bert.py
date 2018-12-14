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
        feed_dict = {"question": "Where is New York City", "context_list": [
            '2 million residents born outside the United States, the largest foreign-born population of any city in the world.  In 2017, the New York metropolitan area produced a gross metropolitan product (GMP) of US$1.73 trillion. If greater New York City were a sovereign state, it would have the 12th highest GDP in the world.New York City traces its origins to a trading post founded by colonists from the Dutch Republic in 1624 on Lower Manhattan; the post was named New Amsterdam in 1626. The city and its surroundings came under English control in 1664 and were renamed New York after King Charles II of England granted the lands to his brother, the Duke of York. New York served as the capital of the United States from 1785 until 1790.'

        ]}
        res = self.infe.response(feed_dict)
        print(res)
        self.assertTrue(len(res),3)


if __name__ == '__main__':
    unittest.main()