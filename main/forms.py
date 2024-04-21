from django import forms
from django.forms.fields import BooleanField
from main.models import Sending, Message, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class SendingForm(StyleFormMixin, forms.ModelForm):
    # Наследуемся от специального класса форм, который предоставляет
    # весь необходимый функционал, который нужно настроить
    class Meta:
        model = Sending
        exclude = ('sent_at', 'status', 'owner', )


class MessageForm(StyleFormMixin, forms.ModelForm):
    # Наследуемся от специального класса форм, который предоставляет
    # весь необходимый функционал, который нужно настроить
    class Meta:
        model = Message
        exclude = ('owner', )

    def clean_theme(self):
        cleaned_data = self.cleaned_data.get('theme')
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in words:
            if word in cleaned_data:
                raise forms.ValidationError('Ошибка в теме письма')

        return cleaned_data

    def clean_text(self):
        cleaned_data = self.cleaned_data.get('text')
        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in words:
            if word in cleaned_data:
                raise forms.ValidationError('Ошибка в тексте письма')

        return cleaned_data


class ClientForm(StyleFormMixin, forms.ModelForm):
    # Наследуемся от специального класса форм, который предоставляет
    # весь необходимый функционал, который нужно настроить
    class Meta:
        model = Client
        exclude = ('owner', )
