from django import forms
from .models import LateNotification

class LateNotificationForm(forms.ModelForm):
    custom_time = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=240,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter custom minutes'
        })
    )
    
    class Meta:
        model = LateNotification
        fields = ['delay_time', 'custom_time', 'reason']
        widgets = {
            'delay_time': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional reason (traffic, train delay, etc.)'
            }),
        }