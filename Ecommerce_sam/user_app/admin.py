from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import SiteUser


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = SiteUser
        fields = ('email', 'mobile', 'first_name', 'last_name')

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = SiteUser
        fields = ('email', 'password', 'mobile', 'first_name', 'last_name', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'mobile', 'first_name', 'last_name', 'is_admin', 'is_staff', 'is_active')
    list_filter = ('is_admin',)

    fieldsets = (
        ('Login Credentials', {'fields': ('mobile', 'password','password_text')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
        ('Seen', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'email', 'first_name', 'last_name', 'password')}
         ),
    )
    search_fields = ('mobile', 'first_name')
    ordering = ('id',)
    filter_horizontal = ()



admin.site.site_header = "E-Commerce"
admin.site.register(SiteUser, UserAdmin)
admin.site.unregister(Group)






