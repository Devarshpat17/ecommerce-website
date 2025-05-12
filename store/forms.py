from django import forms
from .models import Product, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    stock = forms.IntegerField(min_value=0, required=True)
    image = forms.ImageField(required=False)
    video = forms.FileField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'stock', 'image', 'video']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')

        # Ensure that either image or video is uploaded, but not both
        if not image and not video:
            raise forms.ValidationError('Please upload either an image or a video.')

        return cleaned_data



class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'favorite_categories']
        widgets = {
            'favorite_categories': forms.CheckboxSelectMultiple,
        }
