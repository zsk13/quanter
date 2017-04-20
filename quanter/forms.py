from django import forms

class Mybook(forms.Form):
    # title = forms.CharField()
	name = forms.CharField()
	author = forms.CharField()
	date = forms.CharField()