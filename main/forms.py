from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['first_name', 'last_name', 'text', 'rating']   

    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], label="Rating (1-5)")
