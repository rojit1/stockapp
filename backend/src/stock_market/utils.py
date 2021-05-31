from .models import Company, CompanyData
from django.conf import settings
import csv
import requests

# for instance -> run this function from django shell
# from stock_market.utils import insert_all_companies

def insert_all_companies():
    file = settings.BASE_DIR /'companies.csv'
    with open(file) as f:
        datas = csv.reader(f)
        for row in datas:
            Company.objects.create(stock_name=row[0], stock_symbol=row[1], sector=row[2], symbol_no=row[3])


def company_data():
    companies = Company.objects.all()
    for company in companies:
        url = f'https://newweb.nepalstock.com/api/nots/market/graphdata/{company.symbol_no}' # url for all data
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url,headers=headers)
        for obj in response.json():
            c = Company.objects.get(symbol_no=company.symbol_no)
            CompanyData.objects.create(company=c,business_date=obj['businessDate'], open_price = obj['openPrice'], high_price=obj['highPrice'],
                low_price=obj['lowPrice'], previous_day_close_price=obj['previousDayClosePrice'],fifty_tow_week_high=obj['fiftyTwoWeekHigh'],
                last_traded_price=obj['lastTradedPrice'],
                total_traded_quantity=obj['totalTradedQuantity'],close_price=obj['closePrice']
            )
        
        