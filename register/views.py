from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from blog.models import Profile
# Help from TECH WITH TIM


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, "Your BlueBlog Account Has Been Successfully Created, You Can Now Log In")

        return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})
