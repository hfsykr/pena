from django import forms

from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]

# New form for default readonly attribute
class DetailNoteForm(NoteForm):
    def __init__(self, *args, **kwargs):
       super(DetailNoteForm, self).__init__(*args, **kwargs)
       self.fields["title"].widget.attrs["readonly"] = True
       self.fields["content"].widget.attrs["readonly"] = True