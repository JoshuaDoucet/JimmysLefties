from django.shortcuts import render
from django.shortcuts import redirect
from shoes.models import SiteUser
from .forms import ShoeSearchForm


# Create your views here.
def profile(request):
  if request.user.is_authenticated:
    if request.user.is_superuser:
      # admin profile shows all use info
      siteUsers = SiteUser.objects.all()  
    else:
      siteUsers = SiteUser.objects.filter(authUser=request.user)   
    return render(request, 'profile.html', {'siteUsers': siteUsers})
  else:
    return render(request, 'profile.html', )


def home(request):
  # if this is a POST request we need to process the form data
  if request.method == 'POST':
      # create a form instance and populate it with data from the request:
      form = ShoeSearchForm(request.POST)
      # check whether it's valid:
      if form.is_valid():
          # process the data in form.cleaned_data as required
          # ...
          # redirect to a new URL:
          # return HttpResponseRedirect('/thanks/')
          phrase = form.cleaned_data['phrase']
          size = form.cleaned_data['size']
          # add form values to session
          request.session['form'] = {"phrase": phrase, "size": size}
          return redirect("shoes")
      else:
        print("User shoe search form is NOT VALID")

  # if a GET (or any other method) we'll create a blank form
  else:
      form = ShoeSearchForm()

  return render(request, 'index.html', {'form': form})

  # Get shoes

