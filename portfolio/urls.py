from django.urls import path
from .views import MyProfileView, DocumentUploadView

urlpatterns = [
    # /api/v1/profile/me/
    path('me/', MyProfileView.as_view(), name='my_profile'),
    # /api/v1/portfolio/upload
    path('upload/', DocumentUploadView.as_view(), name='document_upload'),
]
