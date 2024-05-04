from django.urls import path
from . import views

urlpatterns = [
    path('writer-dashboard', views.writer_dashboard, name='writer-dashboard'),
    path('create-article', views.create_articles, name='create-article'),
    path('my-article', views.my_article, name='my-article'),
    path('update-article/<str:pk>', views.update_article, name='update-article'),
    path('delete-article/<str:pk>', views.delete_article, name='delete-article'),
    path('account-setting', views.account_management, name='account-setting'),
    path('account-delete', views.delete_account, name='account-delete'),
]
