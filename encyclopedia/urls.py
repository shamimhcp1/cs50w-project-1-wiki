from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_entry, name="get_entry"),
    path("random_page", views.random_page, name="random_page"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("create_page", views.create_page, name="create_page"),
]
