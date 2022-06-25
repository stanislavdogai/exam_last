from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from webapp.forms import SearchForm, AdForm
from webapp.models import Ad


class ListAdds(ListView):
    model = Ad
    context_object_name = "adds"
    template_name = "adds/list.html"
    paginate_by = 10
    paginate_orphans = 0
    ordering = '-public_at'

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = SearchForm()
        if self.search_value:
            context['search'] = self.search_value
        return context

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(title__icontains=self.search_value) | Q(text__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by("-public_at").filter(status='public').exclude(is_deleted=True)

class AdDetailView(DetailView):
    model = Ad
    template_name = 'adds/detail.html'

class ListModeratedAdds(PermissionRequiredMixin, ListView):
    model = Ad
    context_object_name = "adds"
    template_name = "adds/list_moderated.html"
    paginate_by = 10
    paginate_orphans = 0
    ordering = '-created_at'
    permission_required = 'webapp.view_ad'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(status='public').exclude(status='delete')



class DetailModeratedAdDetailView(PermissionRequiredMixin, DetailView):
    model = Ad
    template_name = 'adds/detail_moderated.html'
    permission_required = 'webapp.view_ad'

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'adds/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:adds_index')

class AdUpdateView(PermissionRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'adds/update.html'
    permission_required = 'webapp.change_ad'

    def form_valid(self, form):
        form.instance.status = 'moderated'
        # form.instance.created_at = None
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:adds_index')

    def has_permission(self):
        return super().has_permission() or self.request.user.profile == self.get_object().author



class AdDeleteView(PermissionRequiredMixin, DeleteView):
    model = Ad
    success_url = reverse_lazy('webapp:adds_index')
    template_name = 'adds/delete.html'
    context_object_name = 'ad'
    permission_required = 'webapp.delete_ad'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        messages.success(self.request, f'Заказ № {self.object.pk} успешно удален!')
        return HttpResponseRedirect(self.get_success_url())

    def has_permission(self):
        return super().has_permission() or self.request.user.profile == self.get_object().author

