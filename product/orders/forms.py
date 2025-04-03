import re

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

    # пользовательские валидаторы, идут после джанговских
    def clean_phone_number(self):
        """
        Валидация номера телефона.

        Raises:
            ValidationError при неверном формате номера.

        Returns:
            data: Корректный номер телефона.
        """
        data = self.cleaned_data["phone_number"]
        if not data.isdigit():
            raise forms.ValidationError("В номере телефона могут быть только цифры")

        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера телефона")

        return data
