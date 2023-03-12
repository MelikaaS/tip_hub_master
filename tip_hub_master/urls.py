"""tip_hub_master URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('home.urls')),
                  path('', include('loginsystem.urls')),
                  path('', include('post_details.urls')),
                  # ---------------
                  path('accounts/', include('allauth.urls')),  # new
                  # ---------------

                  path('password_reset_confirm/<uidb64>/<token>/',
                       auth_views.PasswordResetConfirmView.as_view(
                           template_name='loginsystem/password_reset_confirm.html'),
                       name='password_reset_confirm'),

                  path('password_reset_complete',
                       auth_views.PasswordResetCompleteView.as_view(
                           template_name='loginsystem/password_reset_complete.html'),
                       name='password_reset_complete')

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
