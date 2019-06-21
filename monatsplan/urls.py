from django.urls import path
from django.views.generic import TemplateView
from .views import MonatsplanView

urlpatterns = [
    path('today/', MonatsplanView.as_view()),
]
