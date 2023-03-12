from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from loginsystem.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    username = forms.CharField(label='username', widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'is_active', 'is_admin')


# --------------------------------------------------------
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.EmailInput())  # attrs={'autofocus':True}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None or password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise ValidationError("email or password is incorrect", code="login-failed")

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class SignupForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ('email','username', 'password1', 'password2')


#
class UserUpdateForm(forms.ModelForm):
    # email = forms.EmailField(disabled=True)
    class Meta:
        model = User
        fields = ('email', 'fullname', 'phone_number', 'username', 'image')
        # fields = ('email', 'fullname', 'phone_number', 'username')



    def clean_email(self):
        # if self.is_valid():
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already exist')
            # try:  # check email exist or not
            #     user = User.objects.exclude(pk=self.instance.pk).get(email=email)
            # except User.DoesNotExist:
            #     return email
            # raise forms.ValidationError('Email is already exist' % user)
        return email

    def clean_username(self):
        # if self.is_valid():
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username is already exist')
        return username
        # try:
        #     user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        # except User.DoesNotExist:
        #     return username
        # raise forms.ValidationError('username is already exist' % user)

    # def save(self, commit=True):
    #      user = super(UserUpdateForm, self).save(commit=False)
    # # #     user.username = self.cleaned_data['username']
    # # #     user.email = self.cleaned_data['email']
    #      self.image = self.cleaned_data['image']
    # # #     user.fullname = self.cleaned_data['fullname']
    # # #     user.phone_number = self.cleaned_data['phone_number']
    #
    #      if commit:
    #          user.save()
    #      return user
