from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    course = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class PlaceCategory(models.Model):
    name = models.CharField(max_length=40, unique=True)
    plural_name = models.CharField(max_length=40)
    
    class Meta:
        verbose_name_plural = "Place categories"
    
    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(PlaceCategory, on_delete=models.PROTECT)
    address = models.CharField(max_length=300)
    longitude = models.DecimalField(max_digits=8, decimal_places=3)
    latitude = models.DecimalField(max_digits=8, decimal_places=3)
    description = models.CharField(max_length=300, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def update_rating(self):
        reviews = Review.objects.filter(place=self)
        score = 0
        for review in reviews:
            score += review.rating

        self.rating = score / len(reviews)
        self.save()
    
class Deal(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    percent_discount = models.IntegerField()
    valid_until = models.DateTimeField()
    details = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.place} {self.percent_discount}% discount until {self.valid_until}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.CharField(max_length=300, blank=True)
    image = models.ImageField(blank=True, null=True)
    
    class Meta:
        unique_together = ["user", "place"]

    def __str__(self):
        return f"{self.place} review by {self.user}"

class Meetup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    time = models.DateTimeField()
    details = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.place} at {self.time}"

class Invitation(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ["recipient", "meetup"]

    def __str__(self):
        return f"{self.meetup} invitation to {self.recipient}"