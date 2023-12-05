from django.test import TestCase
from django.contrib.auth.models import User
from .models import Note
from django.test import Client
from django.urls import reverse

# Create your tests here.
class NoteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user_test", password="password user_test")
        self.note = Note.objects.create(title="Test note title", content="Test note content", user=self.user)

    def test_date_created_first_save(self):
        self.assertNotEqual(self.note.created, None)

    def test_date_updated_after_first_save(self):
        self.assertEqual(self.note.updated, None)
        self.note.title = "New test note title"
        self.note.save()
        self.assertNotEqual(self.note.updated, None)

class NoteViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.login_credentials = {
            "username": "user_test",
            "password": "password user_test",
        }

        # Create new user for login
        self.user = User.objects.create_user(**self.login_credentials)
        # Login user
        self.client.login(**self.login_credentials)

        # New not for test update & delete
        self.note = Note.objects.create(title="Test note title 1", content="Test note content 1", user=self.user)
    
    def test_view_create_note(self):
        response = self.client.post(reverse("notes:create"), data={"title": "Test note title 2", "content": "Test note content 2"})
        # Automatically redirected to note's detail/page after note's successfully created
        note_detail = self.client.get(response.url)
        self.assertContains(note_detail, "Test note title 2")

    def test_view_update_note(self):
        # Get note detail data before updated
        note_detail = self.client.get(reverse("notes:detail", args=[self.note.id]))
        # Check if note detail still not updated yet
        self.assertContains(note_detail, "Test note title 1")
        # Update the note
        response = self.client.post(reverse("notes:detail", args=[self.note.id]), data={"title": "Updated test note title 1", "content": "Updated test content 1"})
        # Automatically redirected to note's detail/page after note's successfully updated
        note_detail = self.client.get(response.url)
        # Note's title on note detail changed after update
        self.assertNotContains(note_detail, "Test note title 1")
        self.assertContains(note_detail, "Updated test note title 1")

    def test_view_delete_note(self):
        # Delete note via view
        self.client.post(reverse("notes:delete", args=[self.note.id]))
        # Try to get the deleted note data (must return "None" cause it has been deleted)
        try:
            note = Note.objects.get(pk=self.note.id)
        except Note.DoesNotExist:
            note = None
        self.assertEqual(note, None)  
    