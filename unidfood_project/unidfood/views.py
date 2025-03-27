from collections import defaultdict

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from unidfood.forms import UserForm, UserProfileForm, ReviewForm
from unidfood.models import UserProfile, Review, Meetup, Invitation, Deal, Place, PlaceCategory
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

        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data['username']

            if User.objects.filter(username=username).exists():
                user_form.add_error('username', 'A user with that username already exists.')

            if not User.objects.filter(username=username).exists():
                user = user_form.save(commit=False)
                password1 = request.POST['password1']
                password2 = request.POST['password2']

                if password1 != password2:
                    user_form.add_error('password2', 'Passwords do not match.')
                else:
                    user.set_password(password1)
                    user.save()

                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
                    
                    user = authenticate(username=user.username, password=password1)
                    if user is not None:
                        login(request, user)

                    registered = True
                    return redirect('unidfood:home')
        else:
            print(user_form.errors, profile_form.errors) 
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'unidfood/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

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
def my_account(request):
    user_form = UserForm(instance=request.user)
    
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None
    
    profile_form = UserProfileForm(instance=profile) if profile else UserProfileForm()

    return render(request, 'unidfood/my_account.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def edit_account(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('unidfood:my_account')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'unidfood/edit_account.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('unidfood:goodbye')
    return render(request, 'unidfood/delete_account.html')
                  
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

@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user)

    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        action = request.POST.get('action')

        review = get_object_or_404(Review, id=review_id, user=request.user)

        if action == 'delete':
            review.delete()
        elif action == 'edit':
            return redirect('unidfood:edit_review', review_id=review.id)

        return redirect('unidfood:my_reviews')

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
                invitation.meetup.attendees.add(request.user)
                invitation.delete()

            elif action == 'decline':
                invitation.delete()

        except Invitation.DoesNotExist:
            pass 

        return redirect('unidfood:my_meetups')

    return render(request, 'unidfood/my_meetups.html', {'meetups': meetups, 'invitations': invitations})

@login_required
def cancel_meetup(request, meetup_id):
    meetup = get_object_or_404(Meetup, id=meetup_id, attendees=request.user)
    meetup.attendees.remove(request.user)

    if meetup.attendees.count() == 0:
        meetup.delete()

    return redirect('unidfood:my_meetups')

@login_required
def delete_review(request, review_id):
    print(review_id)
    review = get_object_or_404(Review, id=review_id)
    place_id = review.place_id
    
    if request.user != review.user:
        return redirect('unidfood:place', place_id)
    
    if request.method == 'POST':
        place_id = review.place_id
        review.delete()    
    
    return redirect('unidfood:place', place_id)

def deals(request):
    deals = Deal.objects.filter(valid_until__gte=now())
    return render(request, 'unidfood/deals.html', {'deals': deals})

def places(request):
    categories = PlaceCategory.objects.all()
    category_places = defaultdict(list)
    for category in categories:
        for place in Place.objects.filter(category=category).order_by('-rating')[:3]:
            category_places[category].append(place)

    return render(request, 'unidfood/places.html', {'category_places': dict(category_places),})

def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    return render(request, 'unidfood/place.html', {'place': place})

def place(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    
    if request.user.is_anonymous:
        existing_review = None
    else:
        existing_review = Review.objects.filter(user=request.user, place=place).first()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=existing_review)
        print(form)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.place = place
            review.save()
            
            return redirect('unidfood:place', place_id=place.id)
    else:
        form = ReviewForm(instance=existing_review)
        
    reviews = Review.objects.filter(place=place)
    for review in reviews:
        review.star_rating = "*" * review.rating + "." * (5 - review.rating)

    return render(request, 'unidfood/place.html', {'place': place, 'existing_review': existing_review, 'form': form, 'reviews': reviews})

def nearby(request):
    places = Place.objects.all()
    return render(request, 'nearby.html', {'places': places})

def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Place.objects.filter(name__icontains=query)

    return render(request, 'unidfood/search_results.html', {'query': query, 'results': results})

def fetch_places(request):
    query = request.GET.get("q", "")

    places = Place.objects.filter(name__icontains=query)[:5] 

    data = [{
        "name": place.name,
        "category": place.category.name,  
        "address": place.address,
    } for place in places
    ]

    return JsonResponse(data, safe=False)

@login_required
def profile(request):
    user_profile = request.user.userprofile

    return render(request, 'account/profile.html', {
        'user_profile': user_profile,
    })
@login_required
def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('unidfood:profile') 
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

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
