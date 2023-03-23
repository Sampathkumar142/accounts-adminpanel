
from django import forms
from management.models import Transaction,PurchaseBook
from django.core.exceptions import ValidationError


class TransactionForm(forms.ModelForm):
    def clean(self):
        print(self.cleaned_data)
        purchase= self.cleaned_data['purchase']
        print(purchase)
        obj = Transaction.objects.filter(purchase = purchase).values('amount')
        paid = sum(obj)
        due = self.purchase.fixed_cost + self.purchase.action_price  - paid
        if self.amount > due:
             raise ValidationError(f'the amount you entered is greater than remaining due amount, remaining due - {due}')
