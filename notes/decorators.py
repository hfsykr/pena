from functools import wraps
from .models import Note
from django.shortcuts import redirect

def user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        note_id = kwargs["note_id"]
        try:
            note = Note.objects.get(pk=note_id)
            if request.user.id != note.user_id:
                return redirect("/")
        except Note.DoesNotExist:
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper