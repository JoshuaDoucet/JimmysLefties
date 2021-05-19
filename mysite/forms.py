from django import forms
from django.utils.safestring import mark_safe

class ShoeSearchForm(forms.Form):
  phrase = forms.CharField(label="Search Phrase", max_length=200, required=False)
  size = forms.FloatField(label=mark_safe("<br>Shoe Size"), required=False)
  