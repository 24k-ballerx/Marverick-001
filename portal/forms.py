from django import forms
from django.contrib.auth import authenticate
from .models import Announcement, Result, AdmissionApplication, ContactMessage
from django.contrib.auth import get_user_model

User = get_user_model()


class PortalLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean(self):
        data = super().clean()
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is None:
            raise forms.ValidationError('Invalid username or password.')
        self._user = user
        return data

    def get_user(self):
        return getattr(self, '_user', None)


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'date', 'scope', 'target_class']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'scope': forms.Select(attrs={'class': 'form-select'}),
            'target_class': forms.Select(attrs={'class': 'form-select'}),
        }


class ResultUploadForm(forms.Form):
    """Bulk or single result upload - simplified; actual implementation can use model forms."""
    student = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-select'}))
    subject = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-select'}))
    score = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))

    def __init__(self, *args, **kwargs):
        from .models import Student, Subject
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.select_related('user').all()
        self.fields['subject'].queryset = Subject.objects.all()


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
