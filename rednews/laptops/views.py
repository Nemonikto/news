from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from rest_framework import generics

from .forms import *
from .models import *
from .utils import *
from .serializers import *


class LaptopHome(DataMixin, ListView):
    model = Laptop
    template_name = 'laptops/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self):
        return Laptop.objects.filter(is_published=True).select_related('cat')


def about(request):
    return render(request, 'laptops/about.html', {'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'laptops/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление новости")
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'laptops/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return context | c_def
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class ShowPost(DataMixin, DetailView):
    model = Laptop
    template_name = 'laptops/post.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class UpPost(LoginRequiredMixin, DataMixin, UpdateView):
    form_class = AddPostForm
    model = Laptop
    template_name = 'laptops/update.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Редактирование "+ str(context['post']))
        return context | c_def


class DeletePost(LoginRequiredMixin, DataMixin, DeleteView):
    model = Laptop
    template_name = 'laptops/delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Удаление "+ str(context['post']))
        return context | c_def


class LaptopAPIView(generics.ListAPIView):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer


class LaptopCategory(DataMixin, ListView):
    model = Laptop
    template_name = 'laptops/index.html'
    context_object_name = 'posts'
    allow_emtpy = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), 
                                        cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Laptop.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'laptops/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return context | c_def
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'laptops/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return context | c_def
    
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
