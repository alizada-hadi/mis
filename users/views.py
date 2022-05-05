from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .decorators import allowed_groups
from django.contrib.auth.decorators import login_required
# register new user


# user list and other functionality
@login_required(login_url="login")
@allowed_groups(groups=["admin"])
def user_list_view(request):
    users = User.objects.exclude(username="admin")

    context = {
        "users" : users
    }    
    return render(request, "users/list.html", context)


@login_required(login_url="login")
@allowed_groups(groups=["admin"])
def delete_user_view(request):
    if request.method == "POST":
        user = User.objects.get(id=request.POST.get("user"))
        try:
            user.delete()
            return redirect("user-list")
        except:
            return redirect("user-list")        



@allowed_groups(groups=["superadmin", "admin"])
@login_required(login_url="login")
def user_register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        password1 = request.POST.get("password")
        password2 = request.POST.get("reapte_password")
        group = Group.objects.get(name=request.POST.get("group"))

        user =  User.objects.create(
            email=email, 
            username=username,  
            first_name=first_name, 
            last_name=last_name, 
            password=make_password(password1)
        )

        if user:
            user.groups.add(group)
            user.save()
    groups = Group.objects.all()

    context = {
        "groups" : groups
    }

    return render(request, "users/register.html", context)



# login view
def user_login_view(request):
    if request.method == "POST":
        username =  request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            for group in user.groups.all():
                if group.name == "manager":
                    return redirect("manager-dashboard")
                else:
                    return redirect("/")
        else:
            return redirect("login")
    return render(request, "users/login.html")


def user_logout_view(request):
    logout(request)
    return redirect("login")



def unauthorize_view(request):

    return render(request, "pages/unauthorize.html")

