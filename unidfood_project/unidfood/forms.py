from django import forms
from django.contrib.auth.models import User
from unidfood.models import UserProfile, Review, Place
from unidfood.models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image', 'bio', 'course')

class ReviewForm(forms.ModelForm):
    place = forms.ModelChoiceField(
        queryset=Place.objects.all(),
        empty_label="Select a place",
        help_text="Choose the place you want to review."
    )
    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5}),
        help_text="Rate the place from 1 (worst) to 5 (best)."
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here'}),
        help_text="Share your thoughts about the place."
    )
    image = forms.ImageField(
        required=False,
        help_text="Upload an image (optional)."
    )

    class Meta:
        model = Review
        exclude = ['user', 'time'] 

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')

        if rating is not None and (rating < 1 or rating > 5):
            self.add_error('rating', "Rating must be between 1 and 5.")

        return cleaned_data

