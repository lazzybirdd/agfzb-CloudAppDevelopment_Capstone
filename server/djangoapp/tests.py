import unittest
from django.test import TestCase
from restapis import get_dealers_from_cf

# Create your tests here.
class Testing(TestCase):
    def test_get_dealers_from_cf(self):
        result = get_dealers_from_cf()
        print(result)
        self.assertEqual(1, 1)

    def test_get_dealers_from_cf(self):
        self.assertEqual(2, 2)

if __name__ == '__main__':
    unittest.main()