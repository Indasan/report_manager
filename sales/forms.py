from django import forms

CHART_CHOISES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart'),
)
RESULT_CHOISES = (
    ('#1', 'Transaction'),
    ('#2', 'Sales date'),
)

class SalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOISES)
    results_by = forms.ChoiceField(choices=RESULT_CHOISES)