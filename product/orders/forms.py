from django import forms


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    # choices обязательно прописывать
    requires_delivery = forms.ChoiceField(choices=[("0", False), ("1", True)])
    # не обязательно для заполнения
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=[("0", 'False'), ("1", 'True')])
