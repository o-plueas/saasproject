from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from .models import CustomUser 

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required= True, 
                             widget = forms.EmailInput(attrs={
                                 'class': 'form-control'
                             }))
    username = forms.CharField(widget = forms.TextInput(attrs={
                                 'class': 'form-control'
                             }))
    
    password1 = forms.CharField(widget = forms.PasswordInput(attrs={
                                 'class': 'form-control'
                             }))
    password2= forms.CharField(widget = forms.PasswordInput(attrs={
                                 'class': 'form-control'
                             }))
    
    role= forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget = forms.Select(attrs={
                                'class': 'form-control'
                            }))
    avatar= forms.ImageField(widget = forms.FileInput(attrs={
                                'class': 'form-control'
                            }))
    phone= forms.CharField(widget = forms.TextInput(attrs={
                                 'class': 'form-control'
                             }))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'avatar', 'phone']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


        
    