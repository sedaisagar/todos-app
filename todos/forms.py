from django import forms

class ReviewForm(forms.Form):
    name = forms.CharField(max_length=45,)
    position = forms.CharField(max_length=10)
    review = forms.CharField(widget=forms.Textarea)
    rating = forms.IntegerField(min_value=0, max_value=5)
