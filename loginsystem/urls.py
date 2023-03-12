from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('forgotpassword', views.ForgotPassword.as_view(), name='forgotPassword'),
    # path('<user_id>/user-panel', views.UserPanel.as_view(),name='user_panel'),
    path('<user_id>/user-panel/', views.userpanel_view, name='user_panel'),
    path('<user_id>/edit-user-panel/', views.edit_userpanel_view, name='edit_userpanel'),  # name='edit_user_panel'
    path('signup', views.SignUp.as_view(), name='signup'),
    path('<user_id>/update_userpanel/', views.update_userpanel_view, name='update_userpanel')
]
