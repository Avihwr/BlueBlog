from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from blog.models import Blog, Contact, BlogComment, Profile, Excerpt
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from .forms import *


# Create your views here.


def home(request):
    index = Blog.objects.all().order_by('-views')[0:5]
    context = {'index': index}
    return render(request, 'index.html', context)


def posts_list(request):
    blogs = Blog.objects.all().order_by('-time')
    post_list = Blog.objects.filter(username=request.user)
    context = {'posts': post_list, 'Blogs': blogs}
    return render(request, 'post_list.html', context)


def blog(request):
    blogs = Blog.objects.all().order_by('-time')
    blog1 = Blog.objects.all().order_by('-time')[0:4]
    blog2 = Blog.objects.all().order_by('-time')[4:]
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    pagy = paginator.get_page(page_number)
    context = {'Blogs': blogs, 'page': pagy, 'blog': blog1, 'blog1': blog2}
    return render(request, 'bloghome.html', context)


def post_upload(request):
    username = request.POST.get('username')
    content = request.POST.get('content')
    slug = request.POST.get('slug')
    title = request.POST.get('title')
    image = request.FILES.get('image')
    if request.method == 'POST':
        post_form = PostUpload(request.POST or None, request.FILES, instance=request.user)
        if post_form.is_valid():
            post_form = Blog.objects.create(username=username, content=content, slug=slug, title=title, image=image)
            post_form.save()
            messages.success(request, 'Your Post has been successfully posted')
            return HttpResponseRedirect(reverse('post_upload'))
    else:
        post_form = PostUpload(instance=request.user)
    context = {'post_form': post_form}
    return render(request, 'post_upload.html', context)


def excerpt(request):
    if request.method == 'POST':
        tag_form = ExcerptForm(request.POST or None)
        if tag_form.is_valid():
            tag_form.save()
            messages.success(request, 'Your Excerpt has been submitted successfully')
            return HttpResponseRedirect(reverse('excerpt'))
    else:
        tag_form = ExcerptForm()
    context = {'tag_form': tag_form}
    return render(request, 'excerpt.html', context)


def post_delete(request, slug):
    post = Blog.objects.filter(slug=slug).first()
    post.delete()
    messages.success(request, "Your post has been deleted successfully")
    return HttpResponseRedirect(reverse('post_list'))


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    user = request.user
    if request.method == 'POST':
        edit_form = PostEdit(request.POST or None, request.FILES, instance=post)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Your Post has been updated successfully')
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        edit_form = PostEdit(instance=post)
    context = {'edit_form': edit_form, 'post': post, 'user': user}
    return render(request, 'post_edit.html', context)


# def pagination(request):
#     post = Blog.objects.all()
#     paginator = Paginator(post, 1)
#     page_number = request.GET.get['page']
#     blogs = paginator.get_page(page_number)
#     context = {'blogs': blogs}
#     return render(request, 'bloghome.html', context)


def posts(request, slug):
    post = Blog.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)
    user = request.user
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = request.POST.get('comment')
            parentSno = request.POST.get('parentSno')
            if parentSno == " ":
                ins = BlogComment.objects.create(post=post, user=user, comment=comment)
                ins.save()
            else:
                parent = BlogComment.objects.get(sno=parentSno)
                ins = BlogComment.objects.create(post=post, user=user, comment=comment, parent=parent)

            ins.save()
            messages.success(request, 'Your comment has been successfully posted')
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    context = {'Blog': post, 'comments': comments, 'user': user, 'form': comment_form}
    return render(request, 'blogposts.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')

        if len(name) < 2:
            messages.warning(request, "Please enter a valid name")
        elif len(email) < 3:
            messages.warning(request, 'Please enter a valid email address')
        elif len(desc) < 4:
            messages.warning(request, 'Please elaborate your concern')
        else:
            ins = Contact(name=name, email=email, desc=desc)
            ins.save()
    return render(request, 'contact.html')


def login(request):
    if request.method == 'POST':
        loginname = request.POST.get('loginname')
        loginpass = request.POST.get('loginpass')

        user = authenticate(username=loginname, password=loginpass)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials, Login Failed!")
            return redirect("/")

    return redirect("error")


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('profile_edit'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {'user_form': user_form, "profile_form": profile_form}
    return render(request, 'profile.html', context)


def logout(request):
    auth_logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect("/")


def search(request):
    query = request.GET['query']
    if len(query) > 80:
        queryposts = Blog.objects.none()
    else:
        querypostsTitle = Blog.objects.filter(title__icontains=query)
        querypostsContent = Blog.objects.filter(content__icontains=query)
        querypostsTC = querypostsTitle.union(querypostsContent)
        querypostsAuthor = Blog.objects.filter(username__icontains=query)
        querypostsExcerpt = Blog.objects.filter(excerpt_type__excerpt__icontains=query)
        queryposts1 = querypostsAuthor.union(querypostsTC)
        queryposts = queryposts1.union(querypostsExcerpt)

    if queryposts.count() == 0:
        messages.warning(request, "No Search Results Found. Please Refine Your Query")
    context = {'QueryPosts': queryposts, 'query': query}
    return render(request, 'search.html', context)


def error(request):
    return render(request, 'error.html')
