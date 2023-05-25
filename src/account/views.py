from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from account.forms import RegistrationForm



class Registration(CreateView):
    template_name = "registration/registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("account:list-users")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user=user, backend="django.contrib.auth.backends.ModelBackend")
        return HttpResponseRedirect(reverse_lazy("account:list-users"))


class Login(LoginView):
    template_name = "registration/login.html"
    next_page = reverse_lazy("account:list-users")
    success_url = reverse_lazy("account:list-users")

class Logout(LogoutView):
    next_page = reverse_lazy("account:login")