from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from hitcount.views import HitCountDetailView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from post_details.models import Post, Like, Comment,Teacher
from ipware import get_client_ip

from persiantools import digits



def get_client_ip_address(request):
    client_ip, is_routable = get_client_ip(request)
    return client_ip



def post_details_view(request, slug):
    context = {}
    post = get_object_or_404(Post, slug=slug)
    teacher=Teacher.objects.all()
    if request.user.is_authenticated:
        if request.user.likes.filter(post__slug=slug, user_id=request.user.id):
            context['is_liked'] = True
        else:
            context['is_liked'] = False
    else:
        return redirect('login')
    context['post'] = post
    context['teacher'] = teacher
    # ---------------------------
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    # __________________________________
    # --------comments
    if request.POST:
        body=request.POST.get('body')
        parent_id=request.POST.get('parent_id')
        Comment.objects.create(body=body, post=post, user=request.user, parent_id=parent_id)
        comment_count=Comment.objects.filter(post=post).count()

        context['comment_count'] =comment_count

    return render(request, 'post_details/video_details.html', context)



def like(request, slug, pk):
    try:
        like = Like.objects.get(post__slug=slug, user_id=request.user.id)
        like.delete()
        return JsonResponse({'response':'unliked'})
    except:
        Like.objects.create(post_id=pk, user_id=request.user.id)
        return JsonResponse({'response': 'liked'})

    # return redirect('post_details', slug)


