from django.urls import path
from .views import TagListCreateView

urlpatterns = [
    # /api/v1/tags
    path('tags', TagListCreateView.as_view(), name='tag_list')
]
