from django.contrib import admin
from .models import Note

# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = ["user", "clean_title"]

    def clean_title(self, obj):
        return obj.title if obj.title != "" else "untitled"
    
    clean_title.short_description = "title"
    clean_title.admin_order_field  = "title"

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