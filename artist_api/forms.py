
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Artist, Work

class ArtistRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name']

    def save(self, commit=True):
        user = super(ArtistRegistrationForm, self).save(commit=False)
        user.save()
        artist = Artist.objects.create(user=user, name=self.cleaned_data['name'])
        return user

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['link', 'work_type']
