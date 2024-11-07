from django import forms
from django.contrib.auth.models import User
from .models import Comment

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","username","password"]

        widgets = {
                'password': forms.PasswordInput(),
            }
        help_texts = {
            'username': '',  # This hides the default help text for username
        }
        labels = {
            'first_name': 'Ism',   # Change "first_name" label to "Ism"
            'last_name': 'Familiya', # Change "last_name" label to "Familiya"
            'email': 'Elektron pochta',  # Change "email" label
            'username': 'Taxallus',  
            'password': 'Sirli so\'z', 
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text","stars"]
        labels = {
            "text":"Fikrlaringiz:",
            "stars":"Necha baho berasiz"
        }