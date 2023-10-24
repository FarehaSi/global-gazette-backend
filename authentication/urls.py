from django.urls import path
from .views import RegisterView, MeView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('me/', CurrentUserView.as_view(), name='current-user')
    path('me/', MeView.as_view(), name='me'),
]
