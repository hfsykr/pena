from django.test import TestCase
from django.test import Client
from .forms import UserRegisterForm
from django.contrib.auth.models import User

# Create your tests here.
class UserFormTests(TestCase):
    def setUp(self):
        self.credentials = {
            "username": "user",
            "email": "user@mail.com",
            "password1": "password user",
            "password2": "password user",
        }

        self.bad_passwords = {
            "password1": "password",
            "password2": "password",
        }
    
    def test_override_password2_to_password1_error(self):
        # Form will be invalid because "password" is a common password
        form = UserRegisterForm(self.bad_passwords)
        # If it is return True, then password2 error not overwritten completly to password1
        self.assertFalse("password2" in form.errors)

    def test_email_save(self):
        form = UserRegisterForm(self.credentials)
        user = form.save(commit=False)
        self.assertEqual(user.email, self.credentials["email"])

class UserViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.register_credentials = {
            "username": "user_register",
            "email": "user@register.com",
            "password1": "password user register",
            "password2": "password user register",
        }

        self.login_credentials = {
            "username": "user_login",
            "password": "password user login",
        }

        # Create new user for login without using /register/ view
        # so when test /register/ view failed, login test not failed too.
        User.objects.create_user(**self.login_credentials)
        
    def test_register(self):
        client = Client() # New instance, so session not saved in self.
        response = client.post("/register/", self.register_credentials)
        # After register, user is automatically logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login(self):
        response = self.client.post("/login/", self.login_credentials)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        response = self.client.get("/logout/")
        # False because AnonymousUser (not logged in)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
    