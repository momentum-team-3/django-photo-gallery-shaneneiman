from allauth.account.forms import SignupForm
from django import forms
from .models import User

class CustomSignUpForm(SignupForm):
    bio = forms.CharField(max_length=200, label="Bio", required=False)
    profile_photo = forms.ImageField(required=False)
    def save(self, request):
        user = super().save(request)
        user.bio = self.cleaned_data["bio"]
        user.profile_photo = self.cleaned_data["profile_photo"]
        user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "profile_photo",
            "bio",
        ]