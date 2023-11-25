from django.urls import path

from . import views

urlpatterns = [
    # ex: /note/
    path("", views.index, name="index"),
    # ex: /polls/06bc031d-eb6f-496a-a65a-89b012580365
    path("note/<uuid:note_id>/", views.detail, name="note_detail")
]
