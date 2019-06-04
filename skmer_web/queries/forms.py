from django import forms
from .models import Query, Queries


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = [
            'fileName',
            'queryFile',
        ]
        widgets = {
        	'fileName': forms.TextInput(attrs={'class': 'box'}),

        }


class MultipleQueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['queryFile']
        widgets = {
            'queryFile': forms.ClearableFileInput(attrs={'multiple': True})
        }


class QueryCollectionForm(forms.ModelForm):
    class Meta:
        model = Queries
        fields = ['collection_name']

# class DoubleWidget(forms.MultiWidget):
