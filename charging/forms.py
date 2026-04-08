
from django import forms

class AdminLoginForm(forms.Form):
    uname = forms.CharField(label="Admin Username", max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class StationLoginForm(forms.Form):
    uname = forms.CharField(label="Station Username", max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class StationRegisterForm(forms.Form):
    station_id = forms.CharField(label="Station Username", max_length=20)
    station_name = forms.CharField(label="Station Name", max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    location = forms.CharField(label="Area", max_length=30)
    city = forms.CharField(label="City", max_length=30)
    email = forms.EmailField(label="Email")
    mobile_number = forms.CharField(label="Mobile Number", max_length=15)
    landmark = forms.CharField(label="Landmark", max_length=30)
    station_type = forms.CharField(label="Station Type", max_length=20)
    total_slots = forms.IntegerField(label="Number of Chargers")
    amount_per_unit = forms.FloatField(label="Amount/Unit (Tariff)")

class UserLoginForm(forms.Form):
    uname = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class UserRegisterForm(forms.Form):
    name = forms.CharField(label="Name", max_length=20)
    address = forms.CharField(label="Address", max_length=40)
    mobile = forms.CharField(label="Mobile", max_length=10)
    email = forms.EmailField(label="Email")
    uname = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class SlotBookingForm(forms.Form):
    sid = forms.CharField(widget=forms.HiddenInput)
    slot_num = forms.IntegerField(widget=forms.HiddenInput)
    carno = forms.CharField(label="Vehicle Number", max_length=20)
    tariff = forms.FloatField(label="Tariff", required=False)
    plan = forms.IntegerField(label="Charging Plan", required=False)
