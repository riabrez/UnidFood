from django.contrib import admin
from unidfood.models import UserProfile, PlaceCategory, Place, Deal, Review, Meetup, Invitation

admin.site.register(UserProfile)
admin.site.register(PlaceCategory)
admin.site.register(Place)
admin.site.register(Review)
admin.site.register(Deal)
admin.site.register(Meetup)
admin.site.register(Invitation)