from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse

from django.views.generic import ListView, CreateView, DetailView, UpdateView

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
        return queryset.order_by("-public_at").filter(status='public')

class AdDetailView(DetailView):
    model = Ad
    template_name = 'adds/detail.html'

class ListModeratedAdds(ListView):
    model = Ad
    context_object_name = "adds"
    template_name = "adds/list_moderated.html"
    paginate_by = 10
    paginate_orphans = 0
    ordering = '-created_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-public_at").exclude(status='public')

class DetailModeratedAdDetailView(DetailView):
    model = Ad
    template_name = 'adds/detail_moderated.html'

class AdCreateView(CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'adds/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:adds_index')

class AdUpdateView(UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'adds/update.html'

    def form_valid(self, form):
        form.instance.status = 'moderated'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:adds_index')


