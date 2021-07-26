from celery import shared_task
from .models import ShopCart, ShopCurrency, Заказ

from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
import pytz



headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}
url = "https://www.google.com/search?q=usd+to+uah&rlz=1C1SQJL_ruUA959UA959&ei=TUzgYOroGJiGwPAP2sy_qAU&oq=us&gs_lcp=Cgdnd3Mtd2l6EAMYADIHCAAQsQMQQzIECAAQQzIECAAQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIHCAAQsQMQQzoHCC4QsQMQQzoICC4QxwEQowI6BAguEEM6CwguELEDEMcBEK8BOgIILjoCCAA6CAguEMcBEK8BOgoILhDHARCvARAKOgQIABAKOgYIABAKECo6BAguEApKBAhBGABQsx1YmD1g2kRoA3ACeACAAeQGiAHdF5IBCTAuMS4yLjYtM5gBAKABAaoBB2d3cy13aXrAAQE&sclient=gws-wiz"


    
def parse(url):
    full_page = requests.get(url, headers=headers)
    soup = bs(full_page.content, "html.parser")
    convert = soup.findAll(
        "span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2}
    )
    
    return convert[0].text

@shared_task
def add_currency():
    result = parse(url)
    new_object = ShopCurrency.objects.create(usd_to_uah=result, date=datetime.now())
    return new_object.usd_to_uah
@shared_task
def check_confirmation():
    orders = Заказ.objects.all()
    for order in orders:
        creationTime = order.дата_заказа
            #print(creationTime)
            #print(datetime.now(pytz.timezone('Europe/Kiev')))
        difference = datetime.now(pytz.timezone('Europe/Kiev')) - creationTime
        res = list(str(difference))
        if str(res[0]) != '0' and order.confirm != 'c':
            order.delete()
            print('something deleted')
    