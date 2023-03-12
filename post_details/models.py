from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from hitcount.models import HitCount

from loginsystem.models import User

from persiantools import digits


# --درباره استاد----
class Teacher(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'is_admin': True},related_name='teacher',default=True)
    # post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='teacher',default=True)
    about_me=models.TextField(max_length=250)
    # image=models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.author.username



class Category(models.Model):
    categories = (
        ('سفر', 'travel'),
        ('رویدادها', 'event')

    )
    # category= models.IntegerField(choices=categories, default=True)
    title = models.CharField(max_length=50, choices=categories, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    # def __int__(self):
    #     return self.category
    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE, name='author',
                               default=True)  # , limit_choices_to={'is_staff': True})

    category = models.ManyToManyField(Category, related_name='cat')
    video = models.FileField(upload_to='videos/', validators=[FileExtensionValidator(['mp4'])])
    headline = models.CharField(max_length=100)
    text = models.TextField(max_length=250, default=True)
    published = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True)  #null=True,
    image= models.ImageField(upload_to='images/', blank=True, default="codingwithmelika/default_video_image.jpg")
    # ___hit counting___
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.headline

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.headline)
        super(Post, self).save()

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    post=models.ForeignKey(Post, on_delete= models.CASCADE, related_name='likes')
    #
    class Meta:
        verbose_name="لایک",
        verbose_name_plural='لایک ها'

    def __str__(self):
        return f'{self.user.username}-{self.post.headline}'


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name= 'comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='Comments'

    def __str__(self):
        return self.body[:50]




