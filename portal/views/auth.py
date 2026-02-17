from django.shortcuts import redirect
from django.views.generic import FormView
from django.contrib.auth import login
from django.urls import reverse_lazy
from ..forms import PortalLoginForm


class LoginView(FormView):
    template_name = 'portal/login.html'
    form_class = PortalLoginForm
    success_url = reverse_lazy('portal:dashboard')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('portal:dashboard')


def login_view(request):
    return LoginView.as_view()(request)


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('public:portal_login')
