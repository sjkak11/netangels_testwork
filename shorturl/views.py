from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from shorturl import models as shorturl_models


class ShortUrlCreateView(CreateView):
    model = shorturl_models.ConvertedUrl
    fields = ['original_url']

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = self.model.objects.all()[:20]
        return super().get_context_data(**kwargs)


class ShortUrlDetailView(DetailView):
    model = shorturl_models.ConvertedUrl


class ShortUrlListView(ListView):
    model = shorturl_models.ConvertedUrl
    paginate_by = 10


class ShortUrlDeleteView(DeleteView):
    model = shorturl_models.ConvertedUrl
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def redirect_view(request, pk):
    short_cut = get_object_or_404(shorturl_models.ConvertedUrl, pk=pk)
    short_cut.update_redirect_count()
    return redirect(short_cut.original_url)
