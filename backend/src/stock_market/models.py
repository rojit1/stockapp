from django.db import models

class Company(models.Model):
    stock_name = models.CharField(max_length=200)
    stock_symbol = models.CharField(max_length=50)
    sector = models.CharField(max_length=100)
    symbol_no = models.IntegerField()

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self):
        return self.stock_name

class CompanyData(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    business_date = models.DateField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    previous_day_close_price = models.FloatField()
    fifty_tow_week_high = models.FloatField()
    last_traded_price = models.FloatField()
    total_traded_quantity = models.FloatField()
    close_price = models.FloatField()


    def __str__(self):
        return self.company.stock_name

