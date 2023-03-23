from django.db import models
from usermanagement.models import Customer
from .sms import send_details



class PayMode(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title 





class Category(models.Model):
    title = models.CharField(max_length=50)
    cost = models.IntegerField()
    
    def __str__(self) -> str:
        return self.title + "  -  ₹" +  str(self.cost)

    class Meta:
        verbose_name = ("category")
        verbose_name_plural = ("categories")



class PurchaseBook(models.Model):
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name='purchases')
    customer = models.ForeignKey(Customer,on_delete = models.PROTECT,related_name='purchases')
    description = models.TextField(null=True,blank = True)
    fixed_cost = models.PositiveIntegerField(editable=False)
    action_price = models.IntegerField()
    date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self) -> str:
        return self.category.title + " - " + self.customer.phone

    def save(self,force_insert=False, force_update=False, using=None,*args, **kwargs):
        self.description = self.category.title +" - " + self.description
        self.fixed_cost = self.category.cost
        super(PurchaseBook, self).save(*args, **kwargs)




class Transaction(models.Model):
    purchase = models.ForeignKey(PurchaseBook,on_delete=models.CASCADE,related_name='records')
    amount = models.IntegerField()
    paymode = models.ForeignKey(PayMode,on_delete=models.PROTECT,related_name='transactions')
    date = models.DateTimeField(auto_now_add = True)

    def save(self,force_insert=False, force_update=False, using=None,*args, **kwargs):

        customer_id = self.purchase.customer.pk
        obj = PurchaseBook.objects.filter(customer_id = customer_id).values('id')
        k = Transaction.objects.filter(purchase_id__in = obj).values('amount')
        paid = sum([item['amount'] for item in k])
        fixedamount= PurchaseBook.objects.filter(customer_id =customer_id ).values('fixed_cost')
        actionprice = PurchaseBook.objects.filter(customer_id = customer_id).values('action_price')
        sumoffixedamount = sum(item['fixed_cost'] for item in fixedamount)
        sumofactionprice = sum(item['action_price'] for item in actionprice)
        due = sumoffixedamount +sumofactionprice - paid - self.amount
        send_details(self.purchase.customer.phone,self.purchase.customer.name,due,self.paymode,self.amount)
        # obj = Transaction.objects.filter(_id = self.purchase_id).values('amount')
        # paid = sum(obj)
        # due = self.purchase.fixed_cost + self.purchase.action_price  - paid
        # if self.amount > due:
        #     print(f'the amount you entered is greater than remaining due amount, remaining due - {due}')
        super(Transaction, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return "transaction"