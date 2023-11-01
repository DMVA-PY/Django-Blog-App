from typing import Any
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# En Django, las vistas son componentes esenciales de una aplicación web que manejan las solicitudes HTTP 
# y generan respuestas para mostrar en el navegador del usuario.

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

# Django default class view for post views
class PostListView(ListView): 
    model = Post
    template_name = 'blog/home.html'
    # context_object_name es el nombre del queryset
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

# Django default class view for post views
class UserPostListView(ListView): 
    model = Post
    template_name = 'blog/user_posts.html'
    # context_object_name es el nombre del queryset
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self): 
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
# Django default class views for post listing
class PostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    model = Post 
    ordering = ['-date_posted']

# Django default class view for creating post
# LoginRequiredMixin es una clase de mezcla que se utiliza para restringir el acceso a class views solo a usuarios que hayan iniciado sesión en la app
class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/post_form.html'
    model = Post
    fields = ['title', 'content']
    ordering = ['-date_posted']

    # El autor del post sera igual al usuario registrado actualmente.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'blog/post_form.html'
    model = Post
    fields = ['title', 'content']

    # El autor del post sera igual al usuario registrado actualmente.
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Prevent other people to update another User post.
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    # Prevent other people to update another User post.
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
