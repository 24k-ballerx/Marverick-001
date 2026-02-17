from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from portal.models import NewsArticle, AdmissionApplication
from portal.forms import ContactForm
from django.contrib import messages


def home(request):
    return render(request, 'public/home.html')


def about(request):
    return render(request, 'public/about.html')


def academics(request):
    return render(request, 'public/academics.html')


def admissions(request):
    return render(request, 'public/admissions.html')


def online_application(request):
    from django import forms
    from portal.models import Class
    class ApplicationForm(forms.Form):
        first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
        phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
        applying_class = forms.ModelChoiceField(queryset=Class.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
        guardian_name = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
        guardian_contact = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
        notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            AdmissionApplication.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                applying_class=form.cleaned_data.get('applying_class'),
                guardian_name=form.cleaned_data.get('guardian_name', ''),
                guardian_contact=form.cleaned_data.get('guardian_contact', ''),
                notes=form.cleaned_data.get('notes', ''),
            )
            messages.success(request, 'Application submitted. We will contact you after review.')
            return redirect('public:admissions')
    else:
        form = ApplicationForm()
    return render(request, 'public/online_application.html', {'form': form})


class NewsListView(ListView):
    model = NewsArticle
    template_name = 'public/news_list.html'
    context_object_name = 'articles'
    paginate_by = 9


def news_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug)
    return render(request, 'public/news_detail.html', {'article': article})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent. We will get back to you soon.')
            return redirect('public:contact')
    else:
        form = ContactForm()
    return render(request, 'public/contact.html', {'form': form})


def portal_login(request):
    if request.user.is_authenticated:
        return redirect('portal:dashboard')
    return redirect('portal:login')
