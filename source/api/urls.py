from django.urls import path

from api.views import PublicAd, CancelAd

app_name = 'api'

urlpatterns = [
    path('ad/<int:pk>/public/', PublicAd.as_view(), name='public'),
    path('ad/<int:pk>/cancel/', CancelAd.as_view(), name='cancel'),
]