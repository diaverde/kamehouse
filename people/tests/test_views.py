import json
from django.test import TestCase
from django.urls import reverse
from people.models import People

# Create your tests here.
class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        #print("setUpTestData: Run once to set up non-modified data for all class methods.")
        number_of_characters = 7
        for char_id in range(number_of_characters):
            People.objects.create(
                name=f'Character {char_id}',
            )
    
    """
    def setUp(self):
        print("setUp: Run once for every test method to set up clean data.")
        pass
    """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_seed_people_are_created(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['peopleAtHome']), 0)
        self.assertEqual(len(response.context['peopleAway']), 7)

    def test_new_person_is_created(self):
        new_character = { "nombre": "Son Gohan", "enCasa": True }
        response = self.client.post('/add', json.dumps(new_character), content_type="application/json")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['peopleAtHome']), 1)
        self.assertEqual(len(response.context['peopleAway']), 7)

    def test_person_is_updated(self):
        test_id = 4
        modified_character = { "nombre": "Son Goten", "enCasa": True }
        response = self.client.put(f'/update/{test_id}', json.dumps(modified_character), content_type="application/json")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        db_modified_char = next((char for char in response.context['peopleAtHome'] if char.id == test_id), None)
        self.assertIsNotNone(db_modified_char)
        self.assertEqual(db_modified_char.name, modified_character["nombre"])
        self.assertEqual(db_modified_char.isHere, modified_character["enCasa"])

    def test_person_is_deleted(self):
        test_id = 2
        response = self.client.delete(f'/delete/{test_id}')
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        db_modified_char = next((char for char in response.context['peopleAtHome'] if char.id == test_id), None)
        self.assertIsNone(db_modified_char)