from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import user_required
from .models import Note
from django.db.models.functions import Coalesce
from .forms import NoteForm

# Create your views here.
@login_required
def index(request):
    user_id = request.user.id
    # Get notes owned by user in session, ordered by updated date first, and created date if it is null (newly created)
    note_list = Note.objects.filter(user_id=user_id).order_by(Coalesce("updated", "created").desc())
    return render(request, "notes/index.html", {"note_list": note_list})

@login_required
@user_required
def detail(request, note_id):
    return HttpResponse("You're looking at note %s." % note_id)

@login_required
def create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect("notes:detail", note_id=note.id)
    else:
        form = NoteForm()
    return render(request, "notes/create.html", {"form": form})
