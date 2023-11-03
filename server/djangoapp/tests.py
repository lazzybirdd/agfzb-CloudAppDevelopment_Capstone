import unittest
#from django.test import TestCase
from unittest import TestCase
from restapis import get_dealers_from_cf
from restapis import analyze_review_sentiments

#settings.configure()

# Create your tests here.
class TestRESTAPI(unittest.TestCase):

    def test_get_dealers_from_cf(self):
        result = get_dealers_from_cf({})
        self.assertEqual(len(result), 50-1)

    def test_analyze_review_sentiments(self):
        r = analyze_review_sentiments("I really really love this!")
        print(r)
        self.assertNotNull(r)
        self.assertNotNull(r["sentiment"])
        self.assertNotNull(r["sentiment"]["document"])
        self.assertNotNull(r["sentiment"]["document"]["label"])
        self.assertEqual(r["sentiment"]["document"]["label"], "positive")

if __name__ == '__main__':
    unittest.main()
    #get_dealers_from_cf()    