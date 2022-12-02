from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


# Full example from django documentation//
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#a-full-example
# (Oday) main issue why the view wasn't working on normal users, is that the admin panel does not
# use CustomUserManager, thus not hashing the password, but when you use `python manage.py createsuperuser`
# it does hash the password using CustomUserManager which allows smooth sign in
# Code below is unnecessary for the final product, it's here just to make the api more coherent


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("code",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            "code",
            "password",
            "name",
            "picture",
            "latitude",
            "longitude",
            "date_joined",
        )


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ("code",)
    list_filter = ("is_staff",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "code",
                    "password",
                    "name",
                    "picture",
                    "latitude",
                    "longitude",
                    "date_joined",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("code", "password1", "password2")}),
    )
    search_fields = ("code",)
    ordering = ("code",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
