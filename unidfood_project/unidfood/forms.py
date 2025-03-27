from django import forms
from django.contrib.auth.models import User
from unidfood.models import UserProfile, Review, Place
from unidfood.models import UserProfile

class UserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control w-10'}),
        help_text="Rate the place from 1 (worst) to 5 (best).",
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review here', 'class': 'form-control'}),
        help_text="Share your thoughts about the place.",
    )
    image = forms.ImageField(
        required=False,
        help_text="Upload an image (optional).",
    )

    class Meta:
        model = Review
        fields = ['rating', 'content', 'image']
        
        def __init__(self, *args, **kwargs):
            print("CONST")
            self.user = kwargs.pop('user', None)
            self.place = kwargs.pop('place', None)
            super().__init__(*args, **kwargs)

    def clean(self):
        print("cleaning")
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        print(cleaned_data)

        if rating is not None and (rating < 1 or rating > 5):
            self.add_error('rating', "Rating must be between 1 and 5.")

        return cleaned_data
    
    # def save(self, commit=True):
    #     print("HERE")
    #     review = super().save(commit=False)
    #     review.user = self.user
    #     review.place = self.place
    #     if commit:
    #         Review.objects.update_or_create(
    #             user=self.user,
    #             place=self.place,
    #             defaults={'rating': review.rating, 'comment': review.comment}
    #         )
    #     return review