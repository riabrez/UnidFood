from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from unidfood.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required

def home(request):
    return HttpResponse("Rango says hey there partner!")

def signup(request):
	registered = False

	if request.method == 'POST' :
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			profile.save()

			registered = True
		else:
			print(user_form.errors, profile_form.errors)

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'unidfood/signup.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return redirect(reverse('unidfood:home'))
			else:
				return HttpResponse("Your UnidFood account is disabled.")
		else:
			print(f"Invalid login details: {username}, {password}")
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'unidfood/login.html')
	
@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('unidfood:home'))