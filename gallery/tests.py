from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from .models import Image
import json

# Create your tests here.
class GalleryTestCase(TestCase):
    def setUp(self):
        user_model = User.objects.create_user(username='test', password='1234', first_name='test',
                                              last_name='test', email='test@test.com')
        Image.objects.create(name='nuevo', url='No', description='testImage', type='jpg', user=user_model, is_public=True)
        Image.objects.create(name='nuevo2', url='No', description='testImage', type='jpg', user=user_model, is_public=False)

    def test_list_images_status(self):
        url = '/gallery/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_count_images_list(self):
        response = self.client.get('/gallery/')
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data), 2)

    def test_add_user(self):
        response=self.client.post('/gallery/addUser/',json.dumps({"username": "testUser", "first_name": "Test", "last_name": "User", "password": "AnyPas#5", "email": "test@test.com"}), content_type='application/json')
        current_data=json.loads(response.content)
        self.assertEqual(current_data[0]['fields']['username'],'testUser')

    def test_ver_imagen_persona(self):
        user_model = User.objects.create_user(username='test2', password='1234', first_name='test',
                                              last_name='test', email='test@test.com')
        Image.objects.create(name='nuevo', url='No', description='testImage', type='jpg', user=user_model, is_public=True)
        Image.objects.create(name='nuevo2', url='No', description='testImage', type='jpg', user=user_model, is_public=False)
        url = '/gallery/' + str(user_model.id) + '/'
        response = self.client.get(url, format='json')
        current_data = json.loads(response.content)
        self.assertEqual(len(current_data),1)
        self.assertEqual(current_data[0]['fields']['name'],'nuevo')

    def test_iniciar_Sesion(self):
        user_model = User.objects.create_user(username='test3', password='1234', first_name='test',
                                              last_name='test', email='test@test.com')
        response = self.client.post('/gallery/login/', json.dumps(
            {"username": user_model.username,"password": user_model.password}), content_type='application/json')
        current_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(current_data[0]['fields']['username'],'test3')

    def test_editar_datos_persona(self):
        user_model = User.objects.create_user(username='test4', password='1234', first_name='test',
                                              last_name='test', email='test@test.com')
        response = self.client.put('/gallery/edit/' + str(user_model.id) + '/' , json.dumps(
            {"first_name": "test4", "last_name": "test4", "email": "test4@test.com"}),
                                    content_type='application/json')
        current_data = json.loads(response.content)
        self.assertEqual(current_data[0]['fields']['first_name'], 'test4')
        self.assertEqual(current_data[0]['fields']['last_name'], 'test4')
        self.assertEqual(current_data[0]['fields']['email'], 'test4@test.com')