from django.test import TestCase
from django.urls import resolve, reverse
from university.views.home import HomeView

class HomePageViewViewTest(TestCase):
    def test_resolve_to_home_page_view(self):
        resolver = resolve('/')
        self.assertEqual(resolver.func.__name__, HomeView.as_view().__name__)

    # def test_appication(self):
    #     response = self.client.get(resolve('/'))
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)