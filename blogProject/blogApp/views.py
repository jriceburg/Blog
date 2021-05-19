from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)


# Create your views here.
@login_required
def home(request):
    context = {'posts': Post.objects.all()}
    return render(request, 'blogApp/home.html', context)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blogApp/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def about(request):
    return render(request, 'blogApp/about.html')


def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # takes two parameters: request and user object
            return redirect('blog-home')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'blogApp/sign_in.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            form.save()
            return redirect('sign_in')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'blogApp/sign_up.html', context)


def index(request):
    return render(request, 'blogApp/index.html')


def log_out(request):
    logout(request)
    return redirect('blog-index')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account Updated')
            return redirect('blog-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blogApp/profile.html', context)
