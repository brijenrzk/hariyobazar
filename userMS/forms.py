from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer
from .validators import file_size


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'username', 'password1', 'password2']


class CreateUserForm2(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['dob', 'gender']


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UpdateUserForm2(forms.ModelForm):

    contact = forms.DecimalField(required=False)
    address = forms.CharField(required=False)
    photo = forms.ImageField(required=False, validators=[file_size])

    class Meta:
        model = Customer
        fields = ['photo', 'contact', 'address', 'dob', 'gender']
