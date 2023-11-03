import unittest
#from django.test import TestCase
from unittest import TestCase
from . import restapis 

# Create your tests here.
class TestRESTAPI(unittest.TestCase):

    def test_get_dealers_from_cf(self):
        result = restapis.get_dealers_from_cf({})
        self.assertEqual(len(result), 50-1)

    def test_get_dealers_from_cf(self):
        self.assertEqual(2, 2)

if __name__ == '__main__':
    unittest.main()
    #get_dealers_from_cf()    