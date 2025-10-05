# summarizer/urls.py
from django.urls import path
from .views import SummarizeView,AskView 

urlpatterns = [
    path('summarize/', SummarizeView.as_view(), name='summarize'),
        path('ask/', AskView.as_view(), name='ask'), # Add this line

]