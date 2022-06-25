from django.urls import path

from webapp.views import ListAdds, AdCreateView, AdDetailView, ListModeratedAdds, DetailModeratedAdDetailView, \
    AdUpdateView, AdDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', ListAdds.as_view(), name='adds_index'),
    path('moderated/', ListModeratedAdds.as_view(), name='adds_index_moderated'),
    path('<int:pk>/detail/moderated/', DetailModeratedAdDetailView.as_view(), name='adds_detail_moderated'),
    path('<int:pk>/detail/', AdDetailView.as_view(), name='adds_detail'),
    path('create/', AdCreateView.as_view(), name='adds_create'),
    path('<int:pk>/update/', AdUpdateView.as_view(), name='adds_update'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='adds_delete'),
]