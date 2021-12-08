from django.test import TestCase
from django.urls import resolve, reverse
from university.views.home import HomeView

# Create your tests here.

def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='Micheal', password='Temporary12$')
        response = self.client.get(reverse('manager'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'Micheal')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'back/manager_group.html')

def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('manager'))
        self.assertRedirects(response, '/mylogin')
