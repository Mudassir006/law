from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import ClientSignUpForm, LawyerSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Lawyer


def register(request):
    return render(request, '../templates/register.html')


def base(request):
    return render(request, 'base.html')


def main(request):
    return render(request, 'lawyerhome.html')


class client_register(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = '../templates/client_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('clienthome')


class lawyer_register(CreateView):
    model = User
    form_class = LawyerSignUpForm
    template_name = '../templates/lawyer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('lawhome')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_lawyer:
                login(request, user)
                return redirect('lawhome')
            elif user is not None and user.is_client:
                login(request, user)
                return redirect('clienthome')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, '../templates/login.html',
                  context={'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')


def clienthome(request):
    lawyers = Lawyer.objects.all()

    context = {'lawyers': lawyers}

    return render(request, 'clienthome.html', context)


def LawyerDetail(request, pk):
    lawyer = Lawyer.objects.get(id=pk)

    return render(request, 'lawyerdetail.html', context={"lawyer", lawyer})
