from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from blog.models import Post
from main.forms import NewsLetterForm, ClientForm
from main.models import NewsLetter, Client, SendAttemp


class NewsLetterListView(LoginRequiredMixin, ListView):
    """ NewsLetter list edpoint """
    model = NewsLetter
    template_name = 'main/newsletter_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_newsletters'] = NewsLetter.objects.count()
        context['active_newsletters'] = NewsLetter.objects.filter(status='created').count()
        context['unique_clients'] = Client.objects.distinct().count()
        all_posts = list(Post.objects.filter(is_published=True))
        context['random_posts'] = sample(all_posts, min(len(all_posts), 3))
        return context

    def get_queryset(self):
        user = self.request.user
        newsletters = NewsLetter.objects.filter(user=user)
        return NewsLetter.objects.filter(user=user)


class NewsLetterDetailView(LoginRequiredMixin, DetailView):
    """ NewsLetter detail edpoint """

    model = NewsLetter
    template_name = 'main/newsletter_detail.html'
    success_url = reverse_lazy('main:newsletter_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['send_attempts'] = self.object.send_attempts.all()
        return context


class NewsLetterCreateView(CreateView):
    """ NewsLetter create edpoint """

    model = NewsLetter
    form_class = NewsLetterForm
    template_name = 'main/newsletter_form.html'
    success_url = reverse_lazy('main:newsletter_list')

    def form_valid(self, form):
        # Устанавливаем текущего пользователя как автора рассылки
        form.instance.user = self.request.user
        # Вызываем родительский метод для сохранения данных формы
        return super().form_valid(form)


class NewsLetterUpdateView(LoginRequiredMixin, UpdateView):
    """ NewsLetter update edpoint """

    model = NewsLetter
    form_class = NewsLetterForm
    template_name = 'main/newsletter_form.html'
    success_url = reverse_lazy('main:newsletter_list')


class NewsLetterDeleteView(LoginRequiredMixin, DeleteView):
    """ NewsLetter delete edpoint """

    model = NewsLetter
    template_name = 'main/newsletter_delete.html'
    success_url = reverse_lazy('main:newsletter_list')


class ClientListView(ListView):
    """ Client list edpoint """
    model = Client
    template_name = 'client_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            queryset = Client.objects.all()
        else:
            queryset = Client.objects.filter(user=user)
        queryset = Client.objects.all()

        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    """ Client detail edpoint """

    model = Client
    template_name = 'main/client_detail.html'
    success_url = reverse_lazy('main:client_list')

class ClientCreateView(LoginRequiredMixin, CreateView):
    """ Client create edpoint """

    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    success_url = reverse_lazy('main:client_list')

    def get_success_url(self):
        return reverse_lazy('users:register_success')

    def form_valid(self, form):
        client = form.save(commit=False)
        client.user = self.request.user
        client.save()
        return super(ClientCreateView, self).form_valid(form)

# Надо дописать тут permissions
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """ Client update edpoint """

    model = Client
    form_class = ClientForm
    template_name = 'main/client_form.html'
    success_url = reverse_lazy('main:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """ Client delete edpoint """

    model = Client
    template_name = 'client_form.html'
    success_url = reverse_lazy('main:client_list')

class SendAttempListView(ListView):
    """ SendAttemps list edpoint """

    model = SendAttemp
    template_name = 'sendattemp_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletter'] = "Попытки рассылки"
        context['log_list'] = SendAttemp.objects.all()
        return context

