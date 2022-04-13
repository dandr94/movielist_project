from django.urls import path

from movielist_web_project.accounts.views import RegisterUserView, LoginUserView, LogoutUserView, \
     ProfileDetailsView, profile_edit, ChangeUserPasswordView

urlpatterns = [path('register/', RegisterUserView.as_view(), name='register user'),
               path('login/', LoginUserView.as_view(), name='login user'),
               path('logout/', LogoutUserView.as_view(), name='logout user'),

               path('profile/details/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
               path('profile/edit/<int:pk>/', profile_edit, name='profile edit'),
               path('profile/change_password/', ChangeUserPasswordView.as_view(), name='profile change password'),
               ]
