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
            username   = "brendanh",
            email      = "brendan.hodge1@gmail.com",
            password   = "password123",
            first_name = "Brendan",
            last_name  = "Hodge",
        ),
        "user2": add_user(
            username   = "hannaburgess",
            email      = "hburgess05@outlook.com",
            password   = "123456",
            first_name = "Hanna",
            last_name  = "Burgess",
        ),
        "user3": add_user(
            username   = "valfernandez",
            email      = "valerafernandez3@gmail.com",
            password   = "amenity-lake-tinfoil",
            first_name = "Valero",
            last_name  = "Fernández",
        ),
        "user4": add_user(
            username   = "lixao",
            email      = "lixao214@hotmail.com",
            password   = "f3q2odhi9x",
            first_name = "Li",
            last_name  = "Xao",
        ),
        "user5": add_user(
            username   = "nicholeward",
            email      = "nicholewardd@gmail.com",
            password   = "letmein",
            first_name = "Nichole",
            last_name  = "Ward",
        ),
        "user6": add_user(
            username   = "michaelahomann",
            email      = "michaelahomann@icloud.com",
            password   = "tropical-enlighten-uncoiled-cruelness",
            first_name = "Michaela",
            last_name  = "Homann",
        ),
        "user7": add_user(
            username   = "stefakselsen",
            email      = "stefakselsen@gmail.com",
            password   = "rW0HsrhiVu",
            first_name = "Stefan",
            last_name  = "Akselsen"
        ),
    }
    
    categories = {
        "Restaurant": add_category("Restaurant", "Restaurants"),
        "Cafe": add_category("Cafe", "Cafes"),
        "Bar": add_category("Bar", "Bars"),
    }
    
    places = [
        add_place(
            category    = categories["Restaurant"],
            name        = "Marino's",
            address     = "23 Calderwood Road, Glasgow G43 2RP",
            description = "Authentic Italian pizza from the Marino family. Family friendly atmosphere with something for everyone."),
        
        add_place(
            category    = categories["Restaurant"],
            name        = "The Brass Juniper",
            address     = "187 Langside Road, Glasgow G42 7BX",
            description = "A stylish brasserie serving hearty dishes like braised lamb shank and gin-infused desserts.",),

        add_place(
            category    = categories["Restaurant"],
            name        = "La Luna Tacos",
            address     = "9 Broomhill Road, Glasgow G11 7QA",
            description = "A lively taqueria serving authentic Mexican street food.",),

        add_place(
            category    = categories["Restaurant"],
            name        = "The Jade Pagoda",
            address     = "112 Pollokshaws Road, Glasgow G41 1PX",
            description = "An elegant spot offering dim sum and Cantonese classics in a zen setting.",),

        add_place(
            category    = categories["Cafe"],
            name        = "Copper Kettle Café",
            address     = "45 Drumchapel Road, Glasgow G15 6PL",
            description = "A cozy nook with steampunk flair, serving bold espresso and scones.",),

        add_place(
            category    = categories["Cafe"],
            name        = "Frosted Petals",
            address     = "3 Nitshill Road, Glasgow G53 5QD",
            description = "A whimsical bakery-café with floral teas and intricate pastries.",),
        
        add_place(
            category    = categories["Bar"],
            name        = "The Iron Stag",
            address     = "14 Brick Lane, London E1 6RF",
            description = "A snug bar with a wall of whiskies, live folk music, and a warm, local feel.",),

        add_place(
            category    = categories["Bar"],
            name        = "The Thistle & Crown",
            address     = "27 Govan Road, Glasgow G51 1HJ",
            description = "A cosy Scottish bar with a tartan-clad interior, serving single malts and haggis bites.",),
    ]
    
    now = datetime.now(tz=timezone.utc)
    
    reviews = [
        add_review(
            user    = users["user1"],
            place   = places[0],
            rating  = 5,
            time    = now,
            content = "Best pizza I've ever had 5/5"
        ),
        add_review(
            user    = users["user3"],
            place   = places[0],
            rating  = 4,
            time    = now - timedelta(days=1, hours=6, minutes=7, seconds=49),
            content = "Good food though service could be better"
        ),
        add_review(
            user    = users["user2"],
            place   = places[3],
            rating  = 3,
            time    = now - timedelta(days=3, hours=6),
            content = "My food arrived cold"
        ),
        add_review(
            user    = users["user3"],
            place   = places[5],
            rating  = 1,
            time    = now - timedelta(days=400, hours=20, minutes=25),
            content = "Never going back, rude staff and overpriced"
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


def add_user(username, email, password, first_name, last_name):
    user = User.objects.get_or_create(username=username, defaults={
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
    })[0]
    
    add_user_profile(user)
    
    return user

def add_user_profile(user, image=None):        
    profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        profile.image = image
        profile.save()
        print("Created user profile for", user.username)
    return profile

def add_category(name, plural_name):
    category, created = PlaceCategory.objects.get_or_create(name=name, defaults={"plural_name": plural_name})
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