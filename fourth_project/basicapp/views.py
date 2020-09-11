from django.shortcuts import render
from basicapp.forms import UserForm, UserProfileForm,Login_Form

from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
def index(request):
    return render(request,'basicapp/index.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'basicapp/registration.html',{'user_form' : user_form,
                                                        'profile_form':profile_form,
                                                        'registered':registered })
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse('Logged In')

def user_login(request):
    form = Login_Form(data = request.POST)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request,user)
                return special(request)

            else:
                return HttpResponse("ACCOUNT IS NOT ACTIVE")

        else:
            print('someone tried to login and failed')
            print('{} {}'.format(username,password))
            return HttpResponse("Invalid Credentials")
    else:
        return render(request, 'basicapp/login.html', {'form' : form})
