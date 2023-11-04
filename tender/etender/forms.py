from django import forms

class TenderForm(forms.Form):
    purchase_name = forms.CharField(label='Наименование закупки', max_length=100)
    purchase_method = forms.CharField(label='Метод закупки', max_length=100)
    purchase_number = forms.CharField(label='Номер закупки', max_length=100)
    purchase_type = forms.CharField(label='Вид закупок', max_length=100)
    organization_name = forms.CharField(label='Наименование организации', max_length=100)
    planned_amount = forms.DecimalField(label='Планируемая сумма', max_digits=10, decimal_places=2)
    publication_date = forms.DateTimeField(label='Дата опубликования', widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    proposal_deadline = forms.DateTimeField(label='Срок подачи предложений поставщиков', widget=forms.TextInput(attrs={'type': 'datetime-local'}))
