from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name = "register" ),
    path('login/',views.login,name = "login"),
    path('activate/<uidb64>/<token>/',views.activate,name = "activate"),
    path('logout/',views.logout,name = "logout"),
    path('user/<username>/',views.profile,name = "profile"),
    path('dashboard/', views.dashboard,name = "dashboard"),
    path('change-password/',views.change_password, name = "change_password"),
    path('reset_password/',views.reset_password, name = "reset_password"),
    path('resetPasswordValidate/<uidb64>/<token>/' , views.reset_password_validate, name = "reset_password_validate"),
    path('forgot_password/',views.forgot_password,name = "forgot_password"),
    path('login_otp/',views.login_otp,name = "login_otp"),
    path('otp_verify/',views.otp_verify,name = "otp_verify"),
    path('farmers/',views.farmers , name = "farmers"),
    path('merchants/' , views.merchants , name = "merchants"),
    path('view_profile/<int:id>/', views.view_profile,name = "view_profile"),
    path('get_farmer_profile/<fob>/', views.get_farmer_profile,name = "get_farmer_profile")


]
