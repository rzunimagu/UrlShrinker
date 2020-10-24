from django import forms

from .models import UrlRedirect


class UrlRedirectForm(forms.ModelForm):
    EDIT_NEW_CHOICS = (
        ("auto", "Автоматически"),
        ("manual", "Вручную")
    )
    edit_new = forms.ChoiceField(
        label='Задать короткую ссылку',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial="auto",
        choices=EDIT_NEW_CHOICS,
    )

    class Meta:
        model = UrlRedirect
        fields = ('url_original', 'edit_new', 'url_new')

        widgets = {
            'url_original': forms.TextInput(attrs={'class': 'form-control'}),
            'url_new': forms.TextInput(attrs={'class': 'form-control'}),
        }
