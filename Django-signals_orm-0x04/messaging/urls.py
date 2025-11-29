from django.urls import path
from . import views


urlpatterns = [
    path("delete/account/<pk>/", views.delete_view, name="delete")
]
