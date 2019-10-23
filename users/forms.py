from django import forms

import users.models

# class OTPForm(forms.ModelForm):
#     referral_code = forms.CharField(required=False)
#
#     class Meta:
#         model = users.models.User
#         fields = ('mobile',)

class OTPForm(forms.Form):
    referral_code = forms.CharField(required=False)
    mobile = forms.IntegerField()

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        return mobile


class TokenForm(forms.ModelForm):
    class Meta:
        model = users.models.Tokens
        fields = ('user', 'token', 'token_type')