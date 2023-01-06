from django.forms import ModelForm
from .models import Room

class createRoom(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']