from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from unidfood.forms import UserForm, UserProfileForm, ReviewForm
from unidfood.models import Review, Meetup, Invitation, Deal, Place, PlaceCategory
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    return render(request, 'unidfood/home.html')

def register(request):
	registered = False

	if request.method == 'POST' :
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit=False)

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

	return render(request, 'unidfood/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect(request.GET.get('next') or 'unidfood:home')
            else:
                messages.error(request, "Your account is disabled.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'unidfood/login.html')

@login_required
def user_logout(request):
	logout(request)
	return redirect(reverse('unidfood:home'))

@login_required
def add_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  
            review.save()
            return redirect('unidfood:home')  
        else:
            return HttpResponse("Invalid form submission.")
    else:
        form = ReviewForm()
    
    return render(request, 'unidfood/add_review.html', {'form': form})

@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'unidfood/my_reviews.html', {'reviews': reviews})

@login_required
def my_meetups(request):
    meetups = Meetup.objects.filter(user=request.user) 
    invitations = Invitation.objects.filter(recipient=request.user) 

    if request.method == 'POST':
        invitation_id = request.POST.get('invitation_id')
        action = request.POST.get('action') 

        try:
            invitation = Invitation.objects.get(id=invitation_id, recipient=request.user)
            if action == 'accept':
                Meetup.objects.create(
                    user=request.user,
                    place=invitation.meetup.place,
                    time=invitation.meetup.time,
                    details=invitation.meetup.details
                )

                invitation.delete()

            elif action == 'decline':
                invitation.delete()

        except Invitation.DoesNotExist:
            pass 

        return redirect('unidfood:my_meetups')

    return render(request, 'unidfood/my_meetups.html', {'meetups': meetups, 'invitations': invitations})

def deals(request):
    deals = Deal.objects.filter(valid_until__gte=now())
    return render(request, 'unidfood/deals.html', {'deals': deals})

def places(request):
    restaurant_cat = PlaceCategory.objects.get(name='Restaurant')
    bar_cat = PlaceCategory.objects.get(name='Bar')
    cafe_cat = PlaceCategory.objects.get(name='Cafe')

    restaurants = Place.objects.filter(category=restaurant_cat)[:3]
    bars = Place.objects.filter(category=bar_cat)[:3]
    cafes = Place.objects.filter(category=cafe_cat)[:3]

    return render(request, 'unidfood/places.html', {'restaurants': restaurants, 'bars': bars, 'cafes': cafes, })

def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    return render(request, 'unidfood/place.html', {'place': place})

def nearby(request):
    return HttpResponse("TODO: nearby view")

def search(request):
    return HttpResponse("TODO: search view")
@login_required
def profile(request):
    user_profile = request.user.userprofile

    return render(request, 'account/profile.html', {
        'user_profile': user_profile,
    })


@login_required
def edit_profile(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('account:profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'account/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('unidfood:goodbye')
    return render(request, 'account/delete_account.html')
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, "Your password has been changed successfully.")
            return redirect('account:profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'account/change_password.html', {'form': form})
def goodbye(request):
    return render(request, 'account/goodbye.html')
