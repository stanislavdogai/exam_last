from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from accounts.views import ProfileDetailView, ProfileUpdateView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile_update')
]