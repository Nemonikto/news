from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from rest_framework import generics

from .forms import *
from .models import *
from .serializers import LaptopSerializer

menu = [{'title': "О сайте", 'url_name':'about'},
        {'title': "Добавление новости", 'url_name':'add_page'},
        {'title': "Обратная связь", 'url_name':'contact'},
        {'title': "Войти", 'url_name':'login'}]


class LaptopHome(ListView):
    model = Laptop
    template_name = 'laptops/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context
    
    def get_queryset(self):
        return Laptop.objects.filter(is_published=True)


def about(request):
    return render(request, 'laptops/about.html', {'menu': menu, 'title': 'О сайте'})


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'laptops/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['menu'] = menu
        return context


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


class ShowPost(DetailView):
    model = Laptop
    template_name = 'laptops/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context


class LaptopAPIView(generics.ListAPIView):
    queryset = Laptop.objects.all()
    serializer_class = LaptopSerializer


class LaptopCategory(ListView):
    model = Laptop
    template_name = 'laptops/index.html'
    context_object_name = 'posts'
    allow_emtpy = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context

    def get_queryset(self):
        return Laptop.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
