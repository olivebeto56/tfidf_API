import unittest
from pandas.core.frame import DataFrame
from endpoints.idf.resource import IdfGenratorResource

class TestTfidf(unittest.TestCase):

    def test_get_dataset(self):

        tdfGenratorResource = IdfGenratorResource()
        ds = tdfGenratorResource.get_dataset()


        self.assertIsInstance(ds, DataFrame)
        self.assertTrue(len(ds) > 0 )
        

if __name__ == '__main__':
    unittest.main()