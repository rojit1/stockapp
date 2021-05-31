from django.contrib import admin
from .models import Company, CompanyData

class CompanyAdmin(admin.ModelAdmin):
    list_display = 'stock_name', 'stock_symbol', 'sector', 'symbol_no'

class CompanyDataAdmin(admin.ModelAdmin):
    list_display = 'company', 'open_price', 'high_price', 'low_price', 'close_price'

admin.site.register(Company,CompanyAdmin)
admin.site.register(CompanyData,CompanyDataAdmin)

