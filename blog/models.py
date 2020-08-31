from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse


# Create your models here.


class Excerpt(models.Model):
    excerpt = models.CharField(max_length=40)

    def __str__(self):
        return self.excerpt


class Blog(models.Model):
    sno = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, default="")
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    views = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True, default="/static/img/900x300.png")
    slug = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    excerpt_type = models.ForeignKey(Excerpt, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title + ' by ' + self.username

    def get_absolute_url(self):
        return reverse("posts:posts", args=[str(self.slug)])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    desc = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name="replies")
    time = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.comment[0:12] + '... ' + " by " + self.user.username
