from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.sign_up, name = 'signup'),
    path('signin', views.sign_in, name = 'signin'),
    path('logout', views.logout_user, name = 'logout'),
    path('profile/<str:username>', views.profile, name = 'profile'),
    path('post/<str:pk>' ,views.post, name = 'post'),
    path('follow', views.follow, name = 'follow'),
    path('delete-post/<str:pk>', views.delete_post, name = 'delete-post'),
    path('comment/<str:pk>', views.comment, name = 'comment'),
    path('like', views.like, name = 'like'),
    path('profile-settings', views.profile_settings, name = 'profile-settings'),
    path('search', views.search, name = 'search'),
    path('', views.index, name = 'index'),
    # path('email-verification/<uidb64>/<token>', views.email_verification, name = 'email-verification'),
    # path('forgot-password', views.forgot_password, name = 'forgot-password'),
    # path('change-password/<uidb64>/<token>', views.change_password, name = 'change-password'),
]