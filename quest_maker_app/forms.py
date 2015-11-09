import re
from django import forms
from django.contrib.auth.models import User
from quest_maker_app.models import DailyDistance
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget


class RegistrationForm(forms.Form):

    first_name = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        label=_("First name"),
        error_messages={ 'invalid': ("This field may contain only letters,"
            "numbers and underscores.")
        })
    last_name = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        label=_("Last name"),
        error_messages={ 'invalid': ("This field may contain only letters,"
            "numbers and underscores.")
        })
    username = forms.RegexField(
        regex=r'^\w+$',
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        label=_("Username"),
        error_messages={ 'invalid': ("This field may contain only letters,"
            "numbers and underscores.")
        })
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
        label=_("Email address")
        )
    # Prompt for password twice:
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs=dict(required=True, max_length=30, render_value=False)
        ),
        label=_("Password"))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs=dict(required=True, max_length=30, render_value=False)),
        label=_("Password (again)")
        )

    def clean_username(self):
        try:
            user = User.objects.get(
                username__iexact=self.cleaned_data['username']
            )
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists."
            "Please try another one."))

    def clean(self):
        cd = self.cleaned_data
        if 'password1' in cd and 'password2' in cd:
            if cd['password1'] != cd['password2']:
                raise forms.ValidationError(_("Passwords do not match."))
        return cd


class DailyDistanceFormDefaultDay(forms.ModelForm):
    class Meta:
        model = DailyDistance
        fields = ('miles', 'day')
        widgets = {'day': forms.HiddenInput()}


class DailyDistanceForm(forms.ModelForm):
    class Meta:
        model = DailyDistance
        fields = ('miles', 'day')
        widgets = {'day': SelectDateWidget()}
