from django import forms
from .models import Fundraiser, FundraiserMsgUpdate, FundraiserDonation  # FundraiserImage


class FundraiserForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ('title', 'body', 'amount_needed')


class FundraiserMsgUpdateForm(forms.ModelForm):
    class Meta:
        model = FundraiserMsgUpdate
        fields = ('title', 'body',)


class FundraiserDonationForm(forms.ModelForm):
    # The top 4 are not saved in our Django database.
    ccNumber = forms.CharField(label='Card number', widget=forms.TextInput(attrs={'required': True, 'class': 'form-control pt-encrypt', 'id': 'ccNumber', 'placeholder': 'Use a cc number above'}))
    ccCSC = forms.CharField(label='Card Security Code', widget=forms.TextInput(attrs={'required': True, 'class': 'form-control pt-encrypt', 'id': 'ccCSC', 'placeholder': 'Use the csc # above'}))
    expiration_month = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'placeholder': 'Must be 12'}))
    expiration_year = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'placeholder': 'Must be 2020'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'placeholder': '8320 your_choice st'}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'required': True, 'placeholder': 'Must be 85284'}))

    class Meta:
        model = FundraiserDonation
        fields = ('amount', 'ccNumber', 'ccCSC', 'expiration_year', 'expiration_month', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city')


# class FundraiserImageForm(forms.ModelForm):
#     class Meta:
#         model = FundraiserImage
#         fields = ('image',)
