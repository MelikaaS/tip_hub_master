from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import View, TemplateView

from loginsystem.forms import UserLoginForm, SignupForm, UserUpdateForm

# login
from loginsystem.models import User

from django.core import files


class LoginFormView(View):
    template_name = 'loginsystem/login.html'
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Login failed!'
        return render(request, self.template_name, context={'form': form, 'message': message})


# Forgot password
class ForgotPassword(PasswordResetView):
    template_name = 'loginsystem/forgotpassword.html'
    email_template_name = 'loginsystem/password_reset_email.html'

    success_url = reverse_lazy('home')


# user panel
# class UserPanel(TemplateView):
#     template_name = 'loginsystem/user-panel.html'
def userpanel_view(request, *args,**kwargs):
    if not request.user.is_authenticated:
        return redirect('login')

    user_id = kwargs.get("user_id")
    user = User.objects.get(pk=user_id)
    return render(request,'loginsystem/user-panel.html')

# signUp or register
# class SignUp(View):
class SignUp(SuccessMessageMixin,CreateView):
    template_name = 'loginsystem/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')
    success_message = "Your profile was created successfully"

    # def get(self, request):
    #     form = self.form_class()
    #     message = ''
    #     return render(request, self.template_name, context={'form': form, 'message': message})
    #
    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     message = ''
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')
    #     else:
    #         form = SignupForm()
    #     return render(request, self.template_name, context={'form': form, 'message': message})




def edit_userpanel_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')

    user_id = kwargs.get("user_id")
    user = User.objects.get(pk=user_id)
    if user.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}

    if request.POST: # request.POST or None
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully')

            # print("CHECK VALIDATION")
            # img_obj = form.instance
            # context['img_obj'] = img_obj
            return redirect('user_panel', user_id=user.pk)

    else:
        form = UserUpdateForm(instance=request.user,initial={
            "email": user.email,
            "image": user.image})


        context['user_form'] = form

    return render(request, 'loginsystem/edit_userpanel.html', context)
# return render(request,'loginsystem/update_userpanel.html',context)


def update_userpanel_view(request,*args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('login')

    user_id = kwargs.get("user_id")
    user = User.objects.get(pk=user_id)
    if user.pk != request.user.pk:
        return HttpResponse("You cannot edit someone elses profile.")
    context = {}

    if request.POST:
        form=UserUpdateForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            print("FORM IS VALID")

            # check file exist and then save it in images/
            if len(request.FILES) != 0:
                print('IMAGE UPLOADED')
                # 26 Azar

                user.image = request.FILES['image']
                user.save()
            form.save()

            return redirect('user_panel', user_id=user.pk)
        else:
            form = UserUpdateForm(request.POST, instance=request.user, initial={
                "id": user.pk,
                "image" : user.image
            })
            context['user_form'] = form
            messages.warning(request, "please Enter valid value")
    else:
        # form=UserUpdateForm(instance=request.user)

        #new13Azar
        form = UserUpdateForm(initial={
            "id": user.pk,
            "image" : user.image
        })


        context['user_form']=form
    return render(request,'loginsystem/update_userpanel.html',context)

