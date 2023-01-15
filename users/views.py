from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserForm, UserProfileForm
from .models import EmailVerifyRecord, UserProfile
from utils.email_send import send_register_email

# Create your views here.


# 邮箱登陆注册
class MyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # 加密明文密码
                return user
        except Exception as e:
            return None


# 修改用户状态，比对验证码
def active_user(request, active_captcha):
    all_records = EmailVerifyRecord.objects.filter(captcha=active_captcha)  # 通过验证码查询
    if all_records:
        for record in all_records:
            email = record.email
            user = User.objects.get(email=email)
            user.is_staff = True
            user.save()
    else:
        return HttpResponse('Wrong activation link!')
    return redirect('users:login')  # 登陆成功，跳转


def login_view(request):
    if request.method != 'POST':
        form = LoginForm()  # 不是post请求就显示空表单
    else:
        form = LoginForm(request.POST)
        if form.is_valid(): # 验证获取数据的类型是否正确
            username = form.cleaned_data['username']    # 表单的数据都存在cleaned_data这个字典中
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # 登陆成功跳转到个人中心
                return redirect('users:user_profile')
                # return HttpResponse('successful login!')
            else:
                return HttpResponse('wrong username or password, failed login!')

    context = {'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)  # 把数据暂存，生成一个数据对象
            new_user.set_password(form.cleaned_data.get('password'))    # 把password取出来，转换为哈希值
            new_user.username = form.cleaned_data.get('email')
            # 发送邮件
            send_status = send_register_email(form.cleaned_data.get('email'), 'register')
            if send_status:
                new_user.save()
                return HttpResponse('Successful Registration!')
            else:
                return HttpResponse('Verification Email Sending Failure!')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def forget_pwd(request):
    if request.method == 'GET':
        form = ForgetPwdForm()
    elif request.method == 'POST':
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            exists = User.objects.filter(email=email).exists()
            if exists:
                # 发送邮件
                send_register_email(email, 'forget')
                return HttpResponse('A email has been sent to your mailbox！')
            else:
                return HttpResponse('This email has not been registered！')

    return render(request, 'users/forget_pwd.html', {'form': form})


def forget_pwd_url(request, active_captcha):
    if request.method != 'POST':
        form = ModifyPwdForm()
    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(captcha=active_captcha)
            email = record.email
            user = User.objects.get(email=email)
            user.username = email
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            return HttpResponse('Modification succeeded!')
        else:
            return HttpResponse('Modification failed!')

    return render(request, 'users/reset_pwd.html', {'form': form})


@login_required(login_url='users:login')
def user_profile(request):
    user = User.objects.get(username=request.user)
    return render(request, 'users/user_profile.html', {'user': user})


def logout_view(request):
    ''' 登出 '''
    logout(request)
    return redirect('users:login')


# @login_required(login_url='users:login')   # 登录之后允许访问
# def editor_users(request):
#     """ 编辑用户信息 """
#     user = User.objects.get(id=request.user.id)
#     if request.method == "POST":
#         try:
#             userprofile = user.userprofile
#             form = UserForm(request.POST, instance=user)
#
#             # user和userprofile是一对一的关系，默认注册时候是没有数据的，注册成功之后才会个人中心重新设置信息
#             # 第一次登陆是空表单，以后编辑是修改，默认显示原有的数据
#             user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
#             # 向表单填充默认数据，如果这里数据不存在就会引发一个错误
#
#             if form.is_valid() and user_profile_form.is_valid():
#                 form.save()
#                 user_profile_form.save()
#                 print('55555')
#                 return redirect('users:user_profile')
#         except UserProfile.DoesNotExist:   # 这里发生错误说明userprofile无数据
#             form = UserForm(request.POST, instance=user)       # 填充默认数据 当前用户
#             user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user)  # 空表单，直接获取空表单的数据保存
#             if form.is_valid() and user_profile_form.is_valid():
#                 form.save()
#                 # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据
#                 new_user_profile = user_profile_form.save(commit=False)
#                 new_user_profile.owner = request.user
#                 new_user_profile.save()
#                 print('66666')
#                 return redirect('users:user_profile')
#     else:
#         print('77777')
#         try:
#             userprofile = user.userprofile
#             form = UserForm(instance=user)
#             user_profile_form = UserProfileForm(instance=userprofile)
#         except UserProfile.DoesNotExist:
#             form = UserForm(instance=user)
#             user_profile_form = UserProfileForm()  # 显示空表单
#     return render(request, 'users/editor_users.html', locals())


@login_required(login_url='users:login')   # 登录之后允许访问
def editor_users(request):
    """ 编辑用户信息 """
    user = User.objects.get(id=request.user.id)
    if request.method != 'POST':
        try:
            userprofile = user.userprofile
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm(instance=userprofile)
        except UserProfile.DoesNotExist:
            form = UserForm(instance=user)
            user_profile_form = UserProfileForm()  # 显示空表单
    else:
        try:
            userprofile = user.userprofile
            form = UserForm(request.POST, instance=user)
            user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)  # 向表单填充默认数据
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                user_profile_form.save()
                return redirect('users:user_profile')
        except UserProfile.DoesNotExist:   # 这里发生错误说明userprofile无数据
            form = UserForm(request.POST, instance=user)       # 填充默认数据 当前用户
            user_profile_form = UserProfileForm(request.POST, request.FILES)  # 空表单，直接获取空表单的数据保存
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()

                return redirect('users:user_profile')
    return render(request, 'users/editor_users.html', locals())

# from django.shortcuts import render, HttpResponse, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.contrib.auth.backends import ModelBackend
# from django.db.models import Q
# from django.contrib.auth.hashers import make_password
# # Create your views here.
# from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserForm, UserProfileForm
# from .models import EmailVerifyRecord, UserProfile
# from utils.email_send import send_register_email
# from django.contrib.auth.decorators import login_required
#
#
# class MyBackend(ModelBackend):
#     """ 邮箱登录注册 """
#
#     def authenticate(self, request, username=None, password=None, ):
#         try:
#             user = User.objects.get(Q(username=username) | Q(email=username))
#             if user.check_password(password):  # 加密明文密码
#                 return user
#         except Exception as e:
#             return None
#
#
# def active_user(request, active_code):
#     """ 修改用户状态，比对链接验证码 """
#     all_records = EmailVerifyRecord.objects.filter(code=active_code)
#     if all_records:
#         for recod in all_records:
#             email = recod.email
#             user = User.objects.get(email=email)
#             user.is_staff = True
#             user.save
#     else:
#         return HttpResponse('链接有误')
#     return redirect('users:login')
#
#
# def login_view(request):
#     """登录功能"""
#     if request.method != 'POST':
#         form = LoginForm()
#     else:
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 # 登录成功之后跳转到个人中心
#                 return redirect('users:user_profile')
#             else:
#                 return HttpResponse('登陆失败')
#
#     context = {'form': form}
#     return render(request, 'users/login.html', context)
#
#
# def register(request):
#     """ 注册视图 """
#     if request.method != 'POST':
#         form = RegisterForm()
#     else:
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.set_password(form.cleaned_data.get('password'))
#             new_user.username = form.cleaned_data.get('email')
#             new_user.save()
#
#             # 发送邮件
#             send_register_email(form.cleaned_data.get('email'), 'register')
#             return HttpResponse('注册成功')
#
#     context = {'form': form}
#     return render(request, 'users/register.html', context)
#
#
# def forget_pwd(request):
#     """ 填写邮箱地址发送邮件表单页面 """
#     if request.method == 'GET':
#         form = ForgetPwdForm()
#     elif request.method == 'POST':
#         form = ForgetPwdForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             exists = User.objects.filter(email=email).exists()
#             if exists:
#                 send_register_email(email, 'forget')
#                 return HttpResponse('邮件已经发送请查收！')
#             else:
#                 return HttpResponse('邮箱还未注册，请前往注册！')
#
#     return render(request, 'users/forget_pwd.html', {'form': form})
#
#
# def forget_pwd_url(request, active_code):
#     """ 发送邮箱链接视图，并修改密码 """
#     if request.method != 'POST':
#         form = ModifyPwdForm()
#     else:
#         form = ModifyPwdForm(request.POST)
#         if form.is_valid():
#             record = EmailVerifyRecord.objects.get(code=active_code)
#             email = record.email
#             user = User.objects.get(email=email)
#             user.username = email
#             user.password = make_password(form.cleaned_data.get('password'))
#             user.save()
#             return HttpResponse('修改成功')
#         else:
#             return HttpResponse('修改失败')
#
#     return render(request, 'users/reset_pwd.html', {'form': form})
#
#
# @login_required(login_url='users:login')
# def user_profile(request):
#     ''' 用户中心 '''
#     user = User.objects.get(username=request.user)
#     return render(request, 'users/user_profile.html', {'user': user})
#
#
# def logout_view(request):
#     ''' 登出 '''
#     logout(request)
#     return redirect('users:login')
#
#
# @login_required(login_url='users:login')  # 登录之后允许访问
# def editor_users(request):
#     """ 编辑用户信息 """
#     user = User.objects.get(id=request.user.id)
#     if request.method == "POST":
#         try:
#             userprofile = user.userprofile
#             form = UserForm(request.POST, instance=user)
#             user_profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)  # 向表单填充默认数据
#             print('8888')
#             form.is_valid()
#             print(form.errors)
#             if form.is_valid() and user_profile_form.is_valid():
#                 form.save()
#                 user_profile_form.save()
#                 print('01010101')
#                 return redirect('users:user_profile')
#         except UserProfile.DoesNotExist:  # 这里发生错误说明userprofile无数据
#             form = UserForm(request.POST, instance=user)  # 填充默认数据 当前用户
#             user_profile_form = UserProfileForm(request.POST, request.FILES)  # 空表单，直接获取空表单的数据保存
#             print('123123')
#             if form.is_valid() and user_profile_form.is_valid():
#                 form.save()
#                 # commit=False 先不保存，先把数据放在内存中，然后再重新给指定的字段赋值添加进去，提交保存新的数据
#                 new_user_profile = user_profile_form.save(commit=False)
#                 new_user_profile.owner = request.user
#                 new_user_profile.save()
#                 print('6786978')
#                 return redirect('users:user_profile')
#     else:
#         print('999')
#         try:
#             userprofile = user.userprofile
#             form = UserForm(instance=user)
#             user_profile_form = UserProfileForm(instance=userprofile)
#         except UserProfile.DoesNotExist:
#             form = UserForm(instance=user)
#             user_profile_form = UserProfileForm()  # 显示空表单
#     print('654321')
#     return render(request, 'users/editor_users.html', locals())