from django.urls import path

from . import views

urlpatterns = [
    path('', views.schichtplan_list, name='schichtplan_list'),
    path('schichtplan/<int:pk>', views.schichtplan_detail, name='schichtplan_detail')
]
