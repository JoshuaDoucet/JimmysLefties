# users/forms.py

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.safestring import mark_safe

SHOE_WIDTHS = [
    ("AAA", "AAA"),
    ("AA", "AA"),
    ("A", "A"),
    ("B", "B"),
    ("C", "C (Narrow)"),
    ("D", "D (Medium)"),
    ("E", "E (Wide)"),
    ("EE", "EE"),
    ("EEE", "EEE"),
    ("?", "Unknown")
]

#The sex the shoe is designed for
SEX = [
  ('M', 'Man'),
  ('W', 'Woman'),
  ("NA", "Other")
] 

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=mark_safe("<br>Email Address"), required=True)
    
    leftSize = forms.FloatField(label=mark_safe("<br>Left Shoe Size"), required=False)
    
    rightSize = forms.FloatField(label=mark_safe("<br>Right Shoe Size"), required=False)

    firstname = forms.CharField(max_length=50, label=mark_safe("<br>First Name"))

    lastname = forms.CharField(max_length=50, label=mark_safe("<br>Last Name"))

    leftWidth = forms.CharField(max_length=10, widget=forms.Select(choices=SHOE_WIDTHS), label=mark_safe("<br>Left Shoe Width"))

    rightWidth = forms.CharField(max_length=10, widget=forms.Select(choices=SHOE_WIDTHS), label=mark_safe("<br>Right Shoe Width"))

    sex = forms.CharField(max_length=10, widget=forms.Select(choices=SEX), label=mark_safe("<br>Prefered Shoe Gender"))

 