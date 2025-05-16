from django import forms
from .models import Patients, Nodes

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
        allowed_values = [0, 1]
        self.fields['kelamin'].choices = [
            choice for choice in self.fields['kelamin'].choices if choice[0] in allowed_values
        ]

# class NodeForm(forms.ModelForm):
#     class Meta:
#         model = Nodes
#         fields = ['status', 'tanggal_lahir', 'kelamin', 'phone_number', 'alamat']
