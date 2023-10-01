from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.db.models import Prefetch
from .views import AuthorsListView, CreateAuthorView
from .models import Author, Book
from .forms import CreateAuthorForm


class TestAuthorsList(TestCase):
    def setUp(self):
        self.actual_path = reverse('authors-list') 
        self.client = Client()
        self.response = self.client.get(self.actual_path)

        self.author_1 = Author.objects.create(
            first_name = 'Denise',
            last_name = 'Adam',
            birth_date = '1986-10-20',
            description = ''
        ) 
        
        self.author_2 = Author.objects.create(
            first_name = 'Elizabeth',
            last_name = 'Adams',
            birth_date = '1980-2-15',
            description = ''
        ) 

    def test_authors_list_url(self):
        self.assertEqual(resolve(self.actual_path).func.view_class, AuthorsListView)

    def test_authors_list_get_request(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'core/authors_list.html')
        self.assertIn('authors_data', self.response.context)


class TestCreateAuthor(TestCase):
    def setUp(self):
        self.actual_path = reverse('create-author')
        self.client = Client()
        self.response = self.client.get(self.actual_path)

    def test_create_author_url(self):
        self.assertEqual(resolve(self.actual_path).func.view_class, CreateAuthorView)
        
    def test_create_author_get_request(self):
        form = self.response.context.get('form')
        
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'core/author_form.html')
        self.assertIsInstance(form, CreateAuthorForm)

    def test_create_author_post_request_with_valid_form(self):pass


class TestUpdateAuthor(TestCase):
    def test_update_author_get_request(self):pass

    def test_update_author_get_request(self):pass


class TestDeleteAuthor(TestCase): pass


    
        
        
