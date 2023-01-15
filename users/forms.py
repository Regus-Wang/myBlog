from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(label='Username/Email', max_length=32, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': 'Enter username/email'
    }))
    password = forms.CharField(label='Password', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': 'Enter password'
    }))
    # 隐藏输入的内容

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username == password:
            raise forms.ValidationError('Username and password cannot be the same!')
        return password


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email', max_length=32, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': 'Enter email'}))
    password = forms.CharField(label='Password', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': 'Enter password'}))
    password1 = forms.CharField(label='Password', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': 'Re-enter password'}))

    class Meta:
        model = User
        fields = ('email', 'password')   # 允许哪些字段被编辑就写哪些

    # 验证用户是否存在
    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()    # 查询username是否在数据库之中
        if exists:
            raise forms.ValidationError('Existing username!')
        return email

    # 验证两次输入密码是否一致
    def clean_password1(self):
        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('Two passwords are matched!')
        else:
            return self.cleaned_data['password']


# 填写邮件，发送修改密码的邮件
class ForgetPwdForm(forms.Form):
    email = forms.EmailField(label='Please enter your email address', min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': 'Username/Email'}))


# 修改密码表单
class ModifyPwdForm(forms.Form):
    """Form definition for UserProfile."""
    password = forms.CharField(label='Password', min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Enter new password'}))


class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input', 'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = ('email', )


class UserProfileForm(forms.ModelForm):
    """Form definition for UserInfo."""

    class Meta:
        """Meta definition for UserInfoform."""

        model = UserProfile
        fields = ('nick_name', 'description', 'motto', 'birthday', 'gender', 'address', 'image')








