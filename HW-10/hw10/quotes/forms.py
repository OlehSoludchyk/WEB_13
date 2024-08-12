# quotes/forms.py
from django import forms

class QuoteForm(forms.Form):
    quote = forms.CharField(widget=forms.Textarea)
    author = forms.CharField()