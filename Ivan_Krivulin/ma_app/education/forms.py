from django.contrib.auth.forms import UserCreationForm
from .models import CustomerUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomerUser
        fields = ('username', 'password1', 'password2')
