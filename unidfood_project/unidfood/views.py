from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from unidfood.forms import UserForm, UserProfileForm, ReviewForm
from unidfood.models import UserProfile, Review, Meetup, Invitation, Deal, Place, PlaceCategory
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

def home(request):
    return render(request, 'unidfood/home.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES) 

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

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('unidfood:home'))
            else:
                messages.error(request, "Your UniDFood account is disabled.")
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
    
    if profile:
        profile_form = UserProfileForm(instance=profile)
    else:
        profile_form = UserProfileForm() 
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('unidfood:my_account')

        if 'change_password' in request.POST:
            new_password = request.POST.get('password1')
            confirm_password = request.POST.get('password2')

            if new_password != confirm_password:
                password_errors = "Passwords do not match."
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect('unidfood:my_account')

    return render(request, 'unidfood/my_account.html', {'user_form': user_form, 'profile_form': profile_form, 'password_errors': password_errors if 'password_errors' in locals() else None})

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
    places = Place.objects.all()
    return render(request, 'nearby.html', {'places': places})

def search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Place.objects.filter(name__icontains=query)

    return render(request, 'unidfood/search_results.html', {'query': query, 'results': results})