from django import forms
from .models import UserProfile

INTEREST_CHOICES = [
    ('jobs', 'Jobs'),
    ('education', 'Education'),
    ('tax', 'Tax Updates'),
    ('schemes', 'Govt Schemes'),
    ('sports', 'Sports Opportunities'),
    ('news', 'Govt News'),
    ('feedback', 'Feedback'),
]

class UserProfileForm(forms.ModelForm):
    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = UserProfile
        fields = ['gender', 'dob', 'income', 'interests', 'location']
