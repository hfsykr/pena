from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import user_required
from .models import Note
from django.db.models.functions import Coalesce
from .forms import NoteForm, DetailNoteForm
import requests
from .utils import html_text_to_json
from config.settings import GSS_CHECKER, LANGUAGETOOL_API_URL

def _gss_result_to_array(result):
    arr = []
    matches = result["matches"]
    for error in matches:
        err = {}

        # Context for finding the error text
        context = error["context"]
        context_text = context["text"]
        context_length = context["length"]
        context_offset = context["offset"]

        err["message"] = error["message"]
        err["offset"] = error["offset"]
        err["length"] = error["length"]
        err["text"] = context_text[context_offset:(context_offset + context_length)]
        err["replacement"] = error["replacements"][0]["value"]

        arr.append(err)
    return arr

@login_required
def index(request):
    user_id = request.user.id
    # Search parameter, default "" if parameter not provided (will return all notes)
    search = request.GET.get("search", "")
    # Get notes owned by user in session, ordered by updated date first, and created date if it is null (newly created)
    note_list = Note.objects.filter(user_id=user_id, title__contains=search).order_by(Coalesce("updated", "created").desc())
    return render(request, "index.html", {"note_list": note_list})

@login_required
@user_required
def detail(request, note_id):
    data = {
        "note_id": note_id
    }
    note = Note.objects.get(pk=note_id)
    if request.method == "POST":
        form = DetailNoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            # Checking grammar, spelling, & style error with LanguageTool API
            if GSS_CHECKER and (LANGUAGETOOL_API_URL is not None) and request.POST.get("gss-checker"):
                data_json = html_text_to_json(form.cleaned_data["content"])
                params = {"data": data_json, "language": "en-US"}
                # result = requests.post("https://api.languagetoolplus.com/v2/check", params=params)
                result = requests.post(LANGUAGETOOL_API_URL, params=params)
                data["gss_errors"] = _gss_result_to_array(result.json())
    else:
        form = DetailNoteForm(instance=note)
    return render(request, "notes/detail.html", {"form": form, "data": data, "GSS_CHECKER": GSS_CHECKER})

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
