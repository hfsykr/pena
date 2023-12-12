from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import user_required
from .models import Note
from django.db.models.functions import Coalesce
from .forms import NoteForm, DetailNoteForm

# Create your views here.
@login_required
def index(request):
    user_id = request.user.id
    # Search parameter, default "" if parameter not provided (will return all notes).
    search = request.GET.get("search", "")
    # Get notes owned by user in session, ordered by updated date first, and created date if it is null (newly created)
    note_list = Note.objects.filter(user_id=user_id, title__contains=search).order_by(Coalesce("updated", "created").desc())
    return render(request, "index.html", {"note_list": note_list})

@login_required
@user_required
def detail(request, note_id):
    note = Note.objects.get(pk=note_id)
    if request.method == "POST":
        form = DetailNoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            return redirect("notes:detail", note_id=note.id)
    else:
        form = DetailNoteForm(instance=note)
    return render(request, "notes/detail.html", {"form": form, "note_id": note_id})

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

@login_required
@user_required
def delete(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    ref = request.GET.get("ref", "/")
    return redirect(ref)
