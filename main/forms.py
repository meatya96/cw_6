from django import forms
from main.models import NewsLetter, Client, Message


class NewsLetterForm(forms.ModelForm):
    message_text = forms.CharField(widget=forms.Textarea, required=False, label='Текст сообщения')

    class Meta:
        model = NewsLetter
        exclude = ('user', 'status', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message_text'].initial = self.instance.message.body if self.instance and self.instance.message else ''

    def save(self, commit=True):
        instance = super().save(commit=False)
        message_text = self.cleaned_data.get('message_text', '')
        if instance.message:
            instance.message.body = message_text
        else:
            instance.message = Message.objects.create(body=message_text)
        if commit:
            instance.save()
        return instance

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'message', 'user']