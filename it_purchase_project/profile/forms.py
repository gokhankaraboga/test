from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Profile
        fields = '__all__'
