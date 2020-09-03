from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('edit/', views.EditView.as_view(), name='edit'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>/',
         views.ActivateView.as_view(), name='activate'),
]
