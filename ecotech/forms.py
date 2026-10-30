from django import forms

from .models import ContactMessage
from .models import Employee, Project


class ContactMessageForm(forms.ModelForm):
	class Meta:
		model = ContactMessage
		fields = ['name', 'email', 'message']
		widgets = {
			'name': forms.TextInput(attrs={'placeholder': '¿Cómo te llamas?', 'autocomplete': 'name'}),
			'email': forms.EmailInput(attrs={'placeholder': 'nombre@empresa.com', 'autocomplete': 'email'}),
			'message': forms.Textarea(attrs={'placeholder': '¿Qué quieres transformar?', 'rows': 4}),
		}

	def clean_name(self):
		return self.cleaned_data['name'].strip()

	def clean_message(self):
		message = self.cleaned_data['message'].strip()
		if len(message) < 10:
			raise forms.ValidationError('Cuéntanos un poco más sobre tu proyecto.')
		return message


class ReportFilterForm(forms.Form):
	employee = forms.ModelChoiceField(queryset=Employee.objects.none(), required=False, label='Empleado')
	project = forms.ModelChoiceField(queryset=Project.objects.none(), required=False, label='Proyecto')
	start_date = forms.DateField(required=False, label='Desde', widget=forms.DateInput(attrs={'type': 'date'}))
	end_date = forms.DateField(required=False, label='Hasta', widget=forms.DateInput(attrs={'type': 'date'}))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['employee'].queryset = Employee.objects.filter(is_active=True)
		self.fields['project'].queryset = Project.objects.all()
