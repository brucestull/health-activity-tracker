from django.urls import path

from . import views


app_name = 'rodbt'
urlpatterns = [
    path('', views.index, name='index'),

    path('journals/', views.JournalListView.as_view(), name='journals'),
    path('questions/', views.QuestionListView.as_view(), name='questions'),
]
