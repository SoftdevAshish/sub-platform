from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account.models import CustomUser
from .forms import ArticleForm, UpdateUserForm
from .models import Article


def check_writer(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        if user.is_writer is True:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('client-dashboard')

    return wrapped_view


# check_is_writer = CustomUser.objects.get(id=user.id)
# if check_is_writer.is_writer is False:
#     return redirect('client-dashboard')


# Create your views here.
@login_required(login_url='login')
@check_writer
def writer_dashboard(request):
    return render(request, 'writer/writer-dashboard.html')


@login_required(login_url='login')
@check_writer
def create_articles(request):
    form = ArticleForm()
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('my-article')

    context = {'CreateArticleForm': form}
    return render(request, 'writer/create-article.html', context)


@login_required(login_url='login')
@check_writer
def my_article(request):
    articles = Article.objects.all().filter(user=request.user.id)
    context = {'AllArticles': articles}
    return render(request, 'writer/my-article.html', context)


@login_required(login_url='login')
@check_writer
def update_article(request, pk):
    try:
        article = Article.objects.get(id=pk, user=request.user)
    except Article.DoesNotExist:
        return redirect('my-article')
    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect('my-article')
    form = ArticleForm(instance=article)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('my-article')

    context = {'UpdateArticleForm': form}
    return render(request, 'writer/update-article.html', context)


@login_required(login_url='login')
@check_writer
def delete_article(request, pk):
    try:
        article = Article.objects.get(id=pk, user=request.user)
    except Article.DoesNotExist:
        return redirect('my-article')
    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect('my-article')
    if request.method == 'POST':
        article.delete()
        return redirect('my-article')
    return redirect('my-article')


@login_required(login_url='login')
@check_writer
def account_management(request):
    form = UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('writer-dashboard')
    context = {'UpdateUserForm': form}
    return render(request, 'writer/account-management.html', context)


@login_required(login_url='login')
@check_writer
def delete_account(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        user.delete()
        return redirect('login')
    return redirect('login')

