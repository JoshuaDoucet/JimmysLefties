# users/views.py

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
from shoes.models import SiteUser, SearchRequest

# Create your views here.

def allSearches(request):
    searches = SearchRequest.objects.all().order_by('-createdOn')
    return render(request, "users/searches.html", {'searches': searches})

def dashboard(request):
    return render(request, "users/dashboard.html")

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # save auth Django user
            user = form.save()
            # get info for sub SiteUser model object
            firstName = request.POST.get('firstname')
            lastName = request.POST.get('lastname')
            username = request.POST.get('username')
            leftSize = request.POST.get('leftSize')
            rightSize = request.POST.get('rightSize')
            leftWidth = request.POST.get('leftWidth')
            rightWidth = request.POST.get('rightWidth')
            sex = request.POST.get('sex')
            email = request.POST.get('email')
            # Add new SiteUser to database table SiteUser
            siteUser = SiteUser(firstname=firstName, lastname=lastName, email=email, username=username, leftSize=leftSize, rightSize=rightSize, sex=sex, leftWidth=leftWidth, rightWidth=rightWidth, authUser=user)
            siteUser.save()

            login(request, user)
            return redirect(reverse("home"))