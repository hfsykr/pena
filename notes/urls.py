from django.urls import path

from . import views

app_name = "notes"
urlpatterns = [
    # ex: /note/
    path("", views.index, name="index"),
    path("note/", views.create, name="create"),
    # ex: /polls/06bc031d-eb6f-496a-a65a-89b012580365
    path("note/<uuid:note_id>/", views.detail, name="detail")
]
