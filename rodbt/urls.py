from django.urls import path

from . import views


app_name = 'rodbt'
urlpatterns = [
    path('', views.index, name='index'),

    path('journals/', views.JournalListView.as_view(), name='journals'),
    path('journals/create/', views.JournalCreateView.as_view(), name='journal-create'),
    path('journals/<int:pk>/', views.JournalDetailView.as_view(), name='journal-detail'),

    path('questions/', views.QuestionListView.as_view(), name='questions'),
]
