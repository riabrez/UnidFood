from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images", blank=True)

    def __str__(self):
        return self.user.username

class Place(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=40)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name
    
class Deal(models.Model):
    place = models.ForeignKey(Place)
    percent_discount = models.IntegerField()
    valid_intil = models.DateTimeField()
    details = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.place} {self.percent_discount}% discount until {self.valid_intil}"

class Review(models.Model):
    user = models.ForeignKey(User)
    place = models.ForeignKey(Place)
    rating = models.SmallIntegerField()
    content = models.CharField(max_length=300)
    time = models.DateTimeField()
    image = models.ImageField()

    def __str__(self):
        return f"{self.place} review by {self.user}"

class Meetup(models.Model):
    user = models.ForeignKey(User)
    place = models.ForeignKey(Place)
    time = models.DateTimeField()
    details = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.place} at {self.time}"

class Invitation(models.Model):
    recipient = models.ForeignKey(User)
    meetup = models.ForeignKey(Meetup)

    def __str__(self):
        return f"{self.meetup} invitation to {self.recipient}"