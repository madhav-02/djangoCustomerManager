from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from .models import Profile, Customer
from django.http import HttpResponse

def home(request):
    user = request.user
    userProfile = Profile.objects.get(user = user)
    #print(type(userProfile.values()))
    # newcustomer = Customer.objects.create(name='ran',id=377)
    # userProfile.customers.add(newcustomer)
    # userProfile.save()
    # print(userProfile.values())
    # newcustomer.save()
    # userProfile.customers.add(newcustomer)
    # userProfile.customers.add(newcustomer)
    # print(userProfile.objects.all())
    allcustomers = userProfile.customers.all()
    # print(allcustomers)
    return render(request, 'users/home.html', {'customers' : allcustomers})


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        self.request.session.set_expiry(0)
        self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def addCustomer(request):
    
    if request.method == 'POST':
        allcustomers={}
        print("hee")
        customerName = request.POST['customername']
        customerId = request.POST['customerid']
        print(customerName, customerId)
        user = request.user
        userProfile = Profile.objects.get(user = user)
        newcustomer = Customer.objects.create(name=customerName,id=customerId)
        userProfile.customers.add(newcustomer)
        userProfile.save()
        allcustomers = userProfile.customers.all()
        return render(request, 'users/home.html', {'customers' : allcustomers})
    else:
        return render(request, 'users/addcustomer.html')
    

