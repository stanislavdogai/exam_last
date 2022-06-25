from django.urls import path

from webapp.views import ListAdds, AdCreateView, AdDetailView, ListModeratedAdds

app_name = 'webapp'

urlpatterns = [
    path('', ListAdds.as_view(), name='adds_index'),
    path('moderated/', ListModeratedAdds.as_view(), name='adds_index_moderated'),
    path('create/', AdCreateView.as_view(), name='adds_create'),
    path('<int:pk>/detail/', AdDetailView.as_view(), name='adds_detail')
]