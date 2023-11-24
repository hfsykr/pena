from django.contrib import admin
from .models import Note

# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = ["user", "title"]

    def get_fields(self, request, obj=None):
        if obj is None:
            # Fields for adding Note
            return ["user", "title", "content"]
        else:
            # Fields for changing Note
            return ["user", "title", "content", "created", "updated"]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            # Readonly fields when changing Note
            return ["created", "updated"]
        else:
            return []

admin.site.register(Note, NoteAdmin)