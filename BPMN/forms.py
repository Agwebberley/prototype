from django import forms

class HelloForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
