from django.test import TestCase
from people.models import People

# Create your tests here.
class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        People.objects.create(name = "Mutenroshi")
    
    """
    def setUp(self):
        print("setUp: Run once for every test method to set up clean data.")
        pass
    """

    def test_not_here_as_default(self):
        person = People.objects.get(id = 1)
        initial_isHere = person.isHere
        self.assertFalse(initial_isHere)
