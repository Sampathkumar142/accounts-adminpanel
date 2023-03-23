from django.contrib import admin
from management.models import PayMode,Category,PurchaseBook,Transaction
from django.db.models import Count,When,F,Q,Case,Sum,FloatField,IntegerField
from django.utils.html import format_html,urlencode
from django.urls import reverse
# from .forms import TransactionForm
# Register your models here.



@admin.register(PayMode)
class PayModeAdmin(admin.ModelAdmin):
    icon_name = "subtitles"
    list_display = ['title','Total_transactions']
    search_fields = ['title']

    def Total_transactions(self,PayMode):
        url = (reverse('admin:management_transaction_changelist') + '?' + urlencode({
            'paymode_id' : str(PayMode.id)
        }))
        return format_html('<a href="{}">{}</a>',url,PayMode.Total_transactions)
    def  get_queryset(self, request) :
        return super().get_queryset(request).annotate(Total_transactions = Count('transactions') )



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    icon_name = "apps"
    list_display = ['title','cost','Total_purchases']
    ordering = ['title']
    search_fields = ['title']
    list_per_page = 10

    def Total_purchases(self,Category):
        url = (reverse('admin:management_purchasebook_changelist') + '?' + urlencode({
            'category_id' : str(Category.id)
        }))
        return format_html('<a href="{}">{}</a>',url,Category.Total_purchases)
    def  get_queryset(self, request) :
        return super().get_queryset(request).annotate(Total_purchases = Count('purchases') )


class TransactionInline(admin.StackedInline):
    model = Transaction
    max_num=15
    extra=0



@admin.register(PurchaseBook)
class PurchaseBookAdmin(admin.ModelAdmin):
    icon_name = "store"
    list_display = ['id','customer','action_price','fixed_cost','total_payable','Due','date','description']
    fields = ['category','customer','action_price','description']
    readonly_fields =['fixed_cost']
    list_filter =['date']
    ordering = ['-date']
    inlines = [TransactionInline]
    autocomplete_fields = ['category','customer']
    search_fields = ['customer__phone__icontains','category__title__icontains','description__icontains']
    list_per_page = 10
    list_editable = ['action_price']

    def total_payable(self,PurchaseBook):
        total_payable = PurchaseBook.fixed_cost + PurchaseBook.action_price
        return total_payable

    def Due(self,PurchaseBook):
        total_payable = PurchaseBook.fixed_cost + PurchaseBook.action_price
        total_due = total_payable
        if PurchaseBook.paid is not None:
            total_due = total_payable - PurchaseBook.paid

        url = (reverse('admin:management_transaction_changelist') + '?' + urlencode({
            'purchase_id' : str(PurchaseBook.id)
        }))
        return format_html('<a href="{}">{}</a>',url,total_due)

    def  get_queryset(self, request) :
        return super().get_queryset(request).annotate(paid = Sum('records__amount') )
    




@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    icon_name = "monetization_on"
    # form = TransactionForm
    list_display = ['purchase','amount','paymode','date']
    autocomplete_fields = ['purchase']
    ordering = ['-date']
    list_filter=['paymode','date']
    search_fields = ['purchase__category__title__icontains','purchase__customer__phone__icontains']
    list_per_page = 10
    list_editable = ['amount']

    

