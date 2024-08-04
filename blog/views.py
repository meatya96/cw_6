from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from blog.forms import PostForm
from blog.models import Post
from blog.services import get_queryset


class PostListView(ListView):
    """ Post list edpoint """
    extra_context = {
        "title": "All posts"
    }
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return get_queryset()


class PostDetailView(DetailView):
    """ Post detail edpoint """
    model = Post
    template_name = 'blog/post_detail.html'
    success_url = reverse_lazy('blog:post_list')

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        object.increment_views()
        return object


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Post create edpoint """
    permission_required = 'blog.add_post'
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Post update edpoint """

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """ Post delete edpoint """

    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset
