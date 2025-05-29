"""
URL configuration for mydata project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from dataapp import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),  # Home redirects to login
    path('signup/', views.signup_view, name='signup'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),  # Separate OTP verification if using Firebase
    path('home/', views.home, name='home'),  # Show home
    path('logout/', views.logout_view, name='logout'),  # Optional logout
    path('update-profile/', views.user_update_profile, name='user_update_profile'),
    path('customers/', views.customer_list, name='customer_list'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('upload-cropped-image/', views.upload_cropped_image, name='upload_cropped_image'),
    path('plans/', views.plans_view, name='plans'), 
    path('customers/', views.customer_list, name='customer_list'),
    path('profile/<str:encoded_id>/', views.customer_detail, name='customer-detail'),
    path('near-me/', views.near_me_profiles, name='near_me_profiles'),
    path('profile/<str:cus_id>/', views.profile_detail, name='profile_detail'),
    path('myplan/', views.my_plan, name='myplan'),
    path('profile/<str:encoded_id>/', views.customer_detail, name='customer_detail'),
    path('people-unlock/', views.people_unlock, name='people-unlock'),
    path('watchlist/', views.watchlist_view, name='watchlist'),
    path('toggle-switch-2/', views.toggle_switch_2, name='toggle_switch_2'),
    path('blog/', views.blog_list, name='blog_list'),  # Shows all blogs
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('insufficient-credits/', views.insufficient_credits_view, name='insufficient_credits'),

    # -----------------------------------------------------------------------------

    # path('email-form', views.email_form, name='home'),  # your main form page
    path('success/', views.success, name='success'),  # <-- Add this!
    path('paymentsuccess/', views.payment_success, name='payment-success'),

    path('upload-horoscope/', views.upload_horoscope, name='upload_horoscope'),
    path('upload-success/', views.upload_success, name='upload_success'),

    path('upload-trustmark/', views.upload_trustmark, name='upload_trustmark'),
    path('trustmark-success/', views.upload_trust_success, name='upload_trust_success'),
    

    # ----------------------------------------------------------------------------

    path('login-with-otp/', views.login_with_otp, name='login_with_otp'),
    path('verify-otp-login/', views.verify_otp_login, name='verify_otp_login'),
    path('check-mobile-existence/', views.check_mobile_existence, name='check_mobile_existence'),
    
    # ------------------------------------------------------------------------
    path('password_reset/', views.custom_password_reset, name='password_reset'),
    path('reset_verify_otp_login/', views.reset_verify_otp_login, name='reset_verify_otp_login'),
    path('reset_password_otp/', views.reset_password_otp, name='reset_password_otp'),
    
    # -------------------------------------------------------------------------
    path('payment/<int:plan_id>/', views.payment_page, name='payment_page')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)