from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from .models import UserProfile, EmailVerifyRecord

from django.contrib.auth.admin import UserAdmin

# 取消关联注册User
admin.site.unregister(User)


# 定义关联对象的样式，StackedInline为纵向排列每一行，TabularInline为并排排列
class UserProfileInline(admin.StackedInline):
    model = UserProfile # 关联的模型


# 关联字段在User之内编辑，关联进来
class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]


# 重新注册User
admin.site.register(User, UserProfileAdmin)


# Admin View for EamilVerifyRecord
@admin.register(EmailVerifyRecord)
class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ('captcha',)
