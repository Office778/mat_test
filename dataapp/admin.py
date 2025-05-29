from django.contrib import admin
from .models import Customers, Options, Blog, Plan, HistoryTran, HistoryUnlock

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('cus_id', 'cus_name', 'cus_mobile', 'cus_email', 'cus_credits', 'trust_mark')
    search_fields = ('cus_name', 'cus_mobile', 'cus_email')
    list_filter = ('gender', 'religion', 'caste', 'marital_status')

@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    search_fields = ('category', 'name')

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan', 'amt', 'credit')

@admin.register(HistoryTran)
class HistoryTranAdmin(admin.ModelAdmin):
    list_display = ('date', 'cus_id', 'tran_no', 'plan', 'amt', 'credit', 'emp_id')
    search_fields = ('cus_id', 'tran_no', 'plan')
    list_filter = ('date', 'plan')
    ordering = ('-date',)

@admin.register(HistoryUnlock)
class HistoryUnlockAdmin(admin.ModelAdmin):
    list_display = ('date', 'cus_id', 'cus_unlock_ids')
    list_filter = ('date', 'cus_id')
    search_fields = ('cus_id', 'cus_unlock_ids')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'date')
    search_fields = ('name', 'title', 'des')
    list_filter = ('date',)
    readonly_fields = ('id',)
