from django.urls import path

from . import views

app_name = "notes"
urlpatterns = [
    # ex: /note/new/
    path("new/", views.create, name="create"),
    # ex: /note/06bc031d-eb6f-496a-a65a-89b012580365/
    path("<uuid:note_id>/", views.detail, name="detail"),
    # ex: /note/delete/06bc031d-eb6f-496a-a65a-89b012580365/
    # you can use "?ref=" for referral to where the note was deleted
    # ex: /note/delete/06bc031d-eb6f-496a-a65a-89b012580365/?ref=/
    path("delete/<uuid:note_id>/", views.delete, name="delete"),
]
