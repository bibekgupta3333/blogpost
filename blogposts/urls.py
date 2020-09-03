from django.urls import path
from . import views

app_name = 'blogposts'

urlpatterns = [
    path('create/', views.CreatePostView.as_view(), name='create'),
    path('', views.ListPostView.as_view(), name='list'),
    path('list/<str:author>/<int:author_id>/<slug:slug>/',
         views.DetailPostView.as_view(), name='detail'),
    path('<str:author>/<int:author_id>/',
         views.UserDetailListPostView.as_view(), name='user_post_list'),
    path('update/<str:author>/<int:author_id>/<slug:slug>/',
         views.UpdatePostView.as_view(), name='update'),
    path('delete/<int:author_id>/<slug:slug>/',
         views.DeletePostView.as_view(), name='delete'),
]
