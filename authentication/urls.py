from django.urls import path
from .views import RegisterView, MeView, LoginView, UpdateProfileView
from .views import following_list, followers_list, FollowUserView, get_user_by_id

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('me/', CurrentUserView.as_view(), name='current-user')
    path('me/', MeView.as_view(), name='me'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('me/update', UpdateProfileView.as_view(), name='update-profile'),
    path('me/following/', following_list, name='following-list'),
    path('me/followers/', followers_list, name='followers-list'),
    path('users/<int:user_id>/', get_user_by_id, name='get-user-by-id'),
]
