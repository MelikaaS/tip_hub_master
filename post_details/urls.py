from django.urls import path
from . import views
# from .views import PostDetailView

urlpatterns = [
    path('post/<slug:slug>', views.post_details_view, name='post_details'),
    # path('post/<int:pk>', PostDetailView.as_view(), name='post_details'),
    path('like/<slug:slug>/<int:pk>', views.like, name='like')

]
