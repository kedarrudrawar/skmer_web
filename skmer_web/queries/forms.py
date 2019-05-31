from django import forms

from .models import Query


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = [
            'fileName',
            'queryFile'
        ]


class RawQueryForm(forms.Form):
    fileName = forms.CharField(max_length=100)