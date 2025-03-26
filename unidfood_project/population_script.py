import os
from datetime import datetime, timezone, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unidfood_project.settings')

import django
django.setup()
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from unidfood.models import UserProfile, PlaceCategory, Place, Review, Deal, Meetup, Invitation

def populate():
    users = {
        "user1": add_user(
            username = "user1",
            email    = "user1@gmail.com",
            password = "password123"
        ),
        "user2": add_user(
            username = "user2",
            email    = "user2@outlook.com",
            password = "123456"
        ),
        "user3": add_user(
            username = "user3",
            email    = "user3@hotmail.com",
            password = "f3q2odhi9x"
        ),
    }
    
    categories = {
        "Restaurant": add_category("Restaurant"),
        "Cafe": add_category("Cafe"),
        "Bar": add_category("Bar"),
    }
    
    places = [
        add_place(
            category    = categories["Restaurant"],
            name        = "Restaurant 1",
            address     = "Address 1",
            description = ""
        ),
        add_place(
            category    = categories["Restaurant"],
            name        = "Restaurant 2",
            address     = "Address 2",
            description = ""
        ),
        add_place(
            category    = categories["Cafe"],
            name        = "Cafe 1",
            address     = "Address 3",
            description = ""
        ),
        add_place(
            category    = categories["Bar"],
            name        = "Cafe 2",
            address     = "Address 4",
            description = ""
        ),
        add_place(
            category    = categories["Bar"],
            name        = "Bar 1",
            address     = "Address 5",
            description = ""
        ),
        add_place(
            category    = categories["Bar"],
            name        = "Bar 2",
            address     = "Address 6",
            description = ""
        ),
    ]
    
    now = datetime.now(tz=timezone.utc)
    
    reviews = [
        add_review(
            user    = users["user1"],
            place   = places[1],
            rating  = 5,
            time    = now,
            content = ""
        ),
        add_review(
            user    = users["user2"],
            place   = places[3],
            rating  = 3,
            time    = now - timedelta(days=3, hours=6),
            content = ""
        ),
        add_review(
            user    = users["user3"],
            place   = places[5],
            rating  = 1,
            time    = now - timedelta(days=400, hours=20, minutes=25),
            content = ""
        ),
    ]
    
    deals = [
        add_deal(
            place       = places[0],
            discount    = 25,
            valid_until = now + timedelta(days=3),
            details     = f"25% off ... at ... until ..."
        ),
        add_deal(
            place       = places[1],
            discount    = 10,
            valid_until = now + timedelta(hours=2),
            details     = f"10% off ... at ... until ..."
        ),
        add_deal(
            place       = places[2],
            discount    = 20,
            valid_until = now - timedelta(days=2, hours=5),
            details     = f"20% off ... at ... until ..."
        ),
    ]
    
    meetups = [
        add_meetup(
            user    = users["user1"],
            place   = places[2],
            time    = now + timedelta(days=7),
            details = ""
        ),
        add_meetup(
            user    = users["user2"],
            place   = places[1],
            time    = now + timedelta(days=2, hours=-3),
            details = ""
        ),
        add_meetup(
            user    = users["user3"],
            place   = places[4],
            time    = now + timedelta(minutes=47),
            details = ""
        ),
    ]
    
    invitations = [
        add_invitation(
            user   = users["user2"],
            meetup = meetups[0]),
        add_invitation(
            user   = users["user3"],
            meetup = meetups[2]),
    ]


def add_user(username, email, password):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password)
        print("Created user", username)
    return user

def add_user_profile(user, image):        
    profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        profile.image = image
        profile.save()
        print("Created user profile for", user.name)
    return profile

def add_category(name):
    category, created = PlaceCategory.objects.get_or_create(name=name)
    if created:
        print("Created category", name)
    return category
    
def add_place(category, name, address, description):
    place, created = Place.objects.get_or_create(
        name=name,
        category=category,
        address=address)
    if created:
        place.description = description
        place.save()
        print("Created place", name)
    return place
    
def add_review(user, place, rating, time, content):
    review, created = Review.objects.get_or_create(
        user=user,
        place=place,
        defaults={
            "rating":rating,
            "time":time,
            "content":content
        }
    )
    if created:
        print(f"Created", review)
    return review

def add_deal(place, discount, valid_until, details):
    deal = Deal.objects.create(
        place=place,
        percent_discount=discount,    
        valid_until=valid_until,
        details=details
    )
    print("Created deal", deal)
    return deal
    
def add_meetup(user, place, time, details):
    meetup = Meetup.objects.create(
        user=user,
        place=place,
        time=time,
        details=details)
    print("Created meetup", meetup)
    return meetup
    
def add_invitation(user, meetup):
    invitation = Invitation.objects.create(
        recipient=user,
        meetup=meetup
    )
    return invitation

if __name__ == "__main__":
    print("Starting UnidFood population script")
    populate()
    print("Done!")