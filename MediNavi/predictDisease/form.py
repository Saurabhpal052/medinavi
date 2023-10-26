from django import forms

class DiseaseInfoForm(forms.Form):
    disease = forms.CharField(label='Disease')
    chances = forms.FloatField(label='Chances')

    def __init__(self, doctors_data, *args, **kwargs):
        super(DiseaseInfoForm, self).__init__(*args, **kwargs)
        doctor_forms = forms.formset_factory(DoctorForm)
        self.doctors = doctor_forms(initial=doctors_data)

class DoctorForm(forms.Form):
    name = forms.CharField(label='Doctor Name')
    specialist = forms.CharField(label='Specialist')
