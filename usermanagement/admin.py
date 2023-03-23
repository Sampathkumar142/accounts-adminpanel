from django.contrib import admin
from usermanagement.models import User,Customer
from django.db.models import Count,When,F,Q,Case,Sum,ExpressionWrapper,IntegerField
from django.utils.html import format_html,urlencode
from django.urls import reverse
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone','first_name','last_name']
    ordering = ['first_name','last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith','last_name__istartswith','phone']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    icon_name = "streetview"
    list_display = ['phone','name','email','gender','Total_purchase']
    ordering =  ['name']
    list_filter = ['gender']
    list_per_page = 10
    search_fields = ['name__icontains','phone','email__icontains']

    # def total_due(self,Customer):
    #     due = 0
    #     print(Customer.total_actionprice)
    #     print(Customer.Total_payable)
    #     print(Customer.total_paid)
    #     if Customer.Total_payable is not None and Customer.total_paid is not None:
    #         due = Customer.Total_payable - Customer.total_paid
    #     elif Customer.Total_payable is not None and Customer.total_paid is None:
    #         due = Customer.Total_payable
    #     return due

    def Total_purchase(self,Customer):
        url = (reverse('admin:management_purchasebook_changelist') + '?' + urlencode({
            'customer_id' : str(Customer.id)
        }))
        return format_html('<a href="{}">{}</a>',url,Customer.Total_purchase)
    def  get_queryset(self, request) :
        return super().get_queryset(request).annotate(Total_purchase = Count('purchases'))
        # .annotate(Total_payable = Sum(F('purchases__fixed_cost'))).annotate(total_actionprice = Sum(F('purchases__action_price'))).annotate(total_paid = Sum('purchases__records__amount'))