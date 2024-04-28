from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main import models


@login_required(login_url='dashboard:log_in')
def index(request):
    contacts = models.Contact.objects.filter(is_show=False).count()
    users = User.objects.count()
    post = models.Post.objects.count()
    context = {
        'contacts':contacts,
        'users':users,
        'post':post
    }
    return render(request, 'dashboard/index.html', context)

def base(request):
    categories = models.Category.objects.all()
    return render(request, 'dashboard/base.html', {'categories':categories})

# Kategoriya
@login_required(login_url='dashboard:log_in')
def create_category(request):
    if request.method == "POST":
        name = request.POST['name']
        models.Category.objects.create(name=name)
    return render(request, 'dashboard/category/create.html')


@login_required(login_url='dashboard:log_in')
def list_category(request):
    category = models.Category.objects.all()
    context = {
        'category':category,
        }

    return render(request, 'dashboard/category/list.html', context)


@login_required(login_url='dashboard:log_in')
def update_category(request, id):
    category = models.Category.objects.get(id=id)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.save()
        return redirect('dashboard:list_category')
    return render(request, 'dashboard:update_category', {'category':category})


@login_required(login_url='dashboard:log_in')
def delete_category(request, id):
    models.Category.objects.get(id=id).delete()
    return redirect('dashboard:list_category')


@login_required(login_url='dashboard:log_in')
def detail_category(request):
    category = models.Category.objects.all()
    post = models.Post.objects.filter(category=category)
    context = {
        'category':category,
        'post':post,
    }

    return render(request, 'dashboard/category/detail.html', context)


# Post
@login_required(login_url='dashboard:log_in')
def create_post(request):
    categories = models.Category.objects.all()
    authors = models.User.objects.all()
    context = {
            'categories': categories,
            'authors':authors
            }
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        date = request.POST['date']
        if 'banner_img' in request.FILES:
            banner_img = request.FILES['banner_img']
            models.Post.objects.create(
                title=title,
                body=body,
                date=date,
                banner_img=banner_img,
            )
        else:
            models.Post.objects.create(
                title=title,
                body=body,
                date=date,
            )
        print(request.POST)
    return render(request, 'dashboard/post/create.html', context)


@login_required(login_url='dashboard:log_in')
def list_post(request):
    post = models.Post.objects.all()
    return render(request, 'dashboard/post/list.html', {'post':post})


@login_required(login_url='dashboard:log_in')
def update_post(request, id):
    post = models.Post.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        date = request.POST['date']
        banner_img = request.FILES['banner_img']
        post.save()
        context = {
            'title':title,
            'body':body,
            'date':date,
            'banner_img':banner_img,
        }

        return redirect('dashboart:list_post', post.id)
    return render(request, 'dashboard:update_post', context)

@login_required(login_url='dashboard:log_in')
def delete_post(request, id):
    models.Post.objects.get(id=id).delete()
    return redirect('dashboard:list_post')




def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')
    return render(request, 'auth/login.html')


def log_out(request):
    logout(request)
    return redirect('dashboard:index')


   



