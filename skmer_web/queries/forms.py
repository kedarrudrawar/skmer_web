from django import forms
from .models import Query, Queries


class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = [
            'fileName',
            'queryFile',
        ]


class MultipleQueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = [
            'queryFile',
        ]
        widgets = {
            'queryFile': forms.ClearableFileInput(attrs={'multiple': True})
        }


class RawQueryForm(forms.Form):
    fileName = forms.CharField(max_length=100)


class QueryCollectionForm(forms.ModelForm):
    class Meta:
        model = Queries
        fields = ['collection_name']


# class QueriesFilesForm(forms.ModelForm):
#     class Meta:
#         model = QueriesFiles
#         fields = ['queryFile']
#         widgets = {
#             'queryFile': forms.ClearableFileInput(attrs={'multiple': True}),
#         }