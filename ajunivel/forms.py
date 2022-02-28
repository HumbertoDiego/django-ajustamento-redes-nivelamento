from django import forms

class AjustamentoForm(forms.Form):
    arquivo = forms.FileField(max_length=1048576)
    dp = forms.FloatField(initial=2.0)
    automatico = forms.BooleanField(initial=True)
    dpinformado = forms.BooleanField(initial=False)

class AjustamentoCustomForm(AjustamentoForm):
    def __init__(self, *args, **kwargs):
        super(AjustamentoCustomForm, self).__init__(*args, **kwargs)
        self.fields['dpinformado'].required = False
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'