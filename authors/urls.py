from django.urls import path
from .views import FollowAuthorView

urlpatterns = [
    path('<int:author_id>/follow/', FollowAuthorView.as_view(), name='follow-author'),
]
