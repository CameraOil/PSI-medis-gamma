from django import forms
from .models import Patients

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = ['name', 'tanggal_lahir', 'kelamin', 'phone_number', 'alamat']
        widgets = {
            'name' : forms.TextInput(attrs={
                'placeholder': "Patient's name"
            }),
            'tanggal_lahir' : forms.DateInput(attrs={
                'placeholder' : "YYYY-MM-DD"
            }),
            'kelamin': forms.RadioSelect(attrs={
                 'class' : 'radio-group'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': "Example: 08XX XXXX XXXX"
            }),
            'alamat' : forms.TextInput(attrs={
                'placeholder': "Home Address"
            })
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the empty "-----" choice
        self.fields['kelamin'].choices = [
            choice for choice in self.fields['kelamin'].choices if choice[0] != ''
        ]

