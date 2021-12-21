import unittest
from pandas.core.frame import DataFrame
from endpoints.tfidf.resource import TfidfResource

class TestTfidf(unittest.TestCase):

    def test_get_tf(self):

        tfidfResource = TfidfResource()
        text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        
        tf = tfidfResource.get_tf(text)

        self.assertEqual(len(tf), 68)

    def test_get_text_url(self):

        url = 'https://www.google.com/'
        tfidfResource = TfidfResource()
        text = tfidfResource.get_text_url(url)

        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 0 )


    @unittest.skip("Skip if the file does not exist yet")
    def test_get_idf_stored(self):

        tfidfResource = TfidfResource()
        idf = tfidfResource.get_idf_stored()

        self.assertIsInstance(idf, DataFrame)
        self.assertTrue(len(idf) > 0 )

if __name__ == '__main__':
    unittest.main()