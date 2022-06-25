from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import DetailView


class ProfileDetailView(DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user_obj'
    paginated_by = 2
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        profile = self.get_object().profile
        paginator = Paginator(
            profile.adds.exclude(status='delete'),
            self.paginated_by,
            self.paginate_related_orphans
        )
        page_number = self.request.GET.get('page', '1')
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['adds'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super(ProfileDetailView, self).get_context_data(**kwargs)