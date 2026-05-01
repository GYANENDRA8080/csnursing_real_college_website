from django import forms
from .models import Admission


class AdmissionForm(forms.ModelForm):
    # Additional fields not in model
    father_name = forms.CharField(max_length=200, required=True)
    mother_name = forms.CharField(max_length=200, required=False)
    father_occupation = forms.CharField(max_length=200, required=False)
    mother_occupation = forms.CharField(max_length=200, required=False)
    address_line1 = forms.CharField(max_length=500, required=True)
    address_line2 = forms.CharField(max_length=500, required=False)
    city = forms.CharField(max_length=100, required=True)
    pincode = forms.CharField(max_length=6, required=True)
    date_of_birth = forms.DateField(
        required=True, widget=forms.DateInput(attrs={"type": "date"})
    )
    height = forms.CharField(max_length=10, required=False)
    weight = forms.IntegerField(required=False)
    sex = forms.ChoiceField(
        choices=[("male", "Male"), ("female", "Female")], required=True
    )
    caste = forms.CharField(max_length=100, required=False)
    nationality = forms.CharField(max_length=100, initial="Indian", required=True)
    religion = forms.CharField(max_length=100, required=False)
    language = forms.CharField(max_length=100, required=False)
    category = forms.ChoiceField(
        choices=[("GENERAL", "General"), ("SC", "SC"), ("ST", "ST"), ("OBC", "OBC")],
        required=True,
    )
    marital_status = forms.ChoiceField(
        choices=[("unmarried", "Unmarried"), ("married", "Married")], required=False
    )

    class Meta:
        model = Admission
        fields = ["name", "email", "phone", "course", "documents"]
        widgets = {"documents": forms.FileInput(attrs={"accept": "image/*,.pdf"})}
