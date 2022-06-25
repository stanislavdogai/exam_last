from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import DetailView, UpdateView

from accounts.forms import ProfileForm
from accounts.models import Profile


class ProfileDetailView(PermissionRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user_obj'
    paginated_by = 2
    paginate_related_orphans = 0
    permission_required = 'webapp.view_profile'

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

    def get_object(self, queryset=None):
        return self.request.user

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object()

class ProfileUpdateView(PermissionRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile_change.html'
    form_class = ProfileForm
    context_object_name = 'user_obj'
    permission_required = 'webapp.change_profile'

    def get_object(self, queryset=None):
        return self.request.user

    def has_permission(self):
        return super().has_permission() or self.request.user == self.get_object()