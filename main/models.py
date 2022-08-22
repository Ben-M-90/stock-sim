from ast import Try
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.shortcuts import get_object_or_404
import os
import pytz
from django.core.validators import MinValueValidator
from decimal import Decimal


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = ['email']
    ojects = CustomUserManager()

    @property
    def get_portfolios(self):
        portfolios = StockPortfolio.objects.filter(user = self)
        return portfolios


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    profile_picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    cover_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    tagline = models.CharField(max_length=30, null=True)
    about_me = models.TextField(max_length=1000, null=True)

    timezone_choices = [(x, x) for x in pytz.common_timezones]
    user_timezone = models.CharField(max_length=35, choices=timezone_choices, default="UTC")

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


@receiver(pre_save, sender=UserProfile)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        existing_image = UserProfile.objects.get(pk=instance.pk)
        if existing_image.profile_picture != instance.profile_picture:
            try:
                os.remove(existing_image.profile_picture.path)
            except:
                pass
        if existing_image.cover_image != instance.cover_image:
            try:
                os.remove(existing_image.cover_image.path)
            except:
                pass


class Stock(models.Model):
    ticker = models.CharField(max_length=5, primary_key=True)
    long_name = models.TextField(null=True)
    _business_summary = models.TextField(null=True)
    _city = models.CharField(max_length=100, null=True)
    _state_location = models.CharField(max_length=100, null=True)
    _country = models.CharField(max_length=60, null=True)
    website = models.TextField(null=True)
    logo_url = models.TextField(null=True)
    _industry = models.CharField(max_length=30, null=True)
    _currency_unit = models.CharField(max_length=5, null=True)
    regular_market_price = models.DecimalField(max_digits=19, decimal_places=8, null=True)
    regular_market_open = models.DecimalField(max_digits=19, decimal_places=8, null=True)
    regular_market_day_high = models.DecimalField(max_digits=19, decimal_places=8, null=True)
    regular_market_previous_close = models.DecimalField(max_digits=19, decimal_places=8, null=True)
    pre_market_price = models.DecimalField(max_digits=19, decimal_places=8, null=True)
    day_low = models.DecimalField(max_digits=19, decimal_places=8, null=True)
    _fifty_day_average = models.DecimalField(max_digits=19, decimal_places=8, null=True)
    _two_hundred_day_average = models.DecimalField(max_digits=19, decimal_places=8, null=True)
    history_data = models.TextField(null=True)
    last_daily_update = models.DateTimeField(null=True)
    last_price_update = models.DateTimeField(null=True)

    @property
    def daily_data(self):
        import datetime
        if (self.last_daily_update is None 
            or self.last_daily_update < datetime.datetime.now(datetime.timezone.utc) 
            - datetime.timedelta(hours = 1)):
            self.get_data()

        data_dict = {"long_name": self.long_name,
                          "business_summary": self._business_summary,
                          "city": self._city,
                          "state_location": self._state_location,
                          "country": self._country,
                          "website": self.website,
                          "logo_url": self.logo_url,
                          "industry": self._industry,
                          "currency_unit": self._currency_unit,
                          "fifty_day_average": self._fifty_day_average,
                          "two_hundred_day_average": self._two_hundred_day_average}
        return data_dict

    def get_data(self):
        import yfinance as yf
        import datetime
        from finance_data_manager import stock_manager

        yfticker = yf.Ticker(self.ticker)
        data_dict = stock_manager.ticker_to_dict(yfticker)

        self.__dict__.update(**data_dict)
        self.last_daily_update = datetime.datetime.now(datetime.timezone.utc)
        self.save()

    def get_price(self):
        from finance_data_manager import stock_manager
        import datetime

        price = stock_manager.get_price(self.ticker)

        self.regular_market_price = price
        self.last_price_update = datetime.datetime.now(datetime.timezone.utc)

        self.save()
        return price

    def buy_stock(self, buy_stock_form, request):
        buy_stock_form.full_clean()
        buy_stock = buy_stock_form.save(commit=False)
        portfolio = get_object_or_404(StockPortfolio, pk=request.POST['portfolio'])
        quantity = Decimal(request.POST['quantity'])
        self.get_price
        purchase_price = self.regular_market_price
        if portfolio.balance < (quantity * Decimal(purchase_price)):
            raise ValueError()
        buy_stock.user = request.user
        buy_stock.stock = self
        buy_stock.purchase_price = purchase_price
        buy_stock.save()
        buy_stock.portfolio.balance = (buy_stock.portfolio.balance
                                       - (buy_stock.quantity * Decimal(buy_stock.purchase_price)))
        buy_stock.portfolio.save()


class StockPortfolio(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=19, decimal_places=8, null=False)
    start_balance = models.DecimalField(max_digits=19, decimal_places=8, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        unique_together = 'user', 'name'

    def save(self, *args, **kwargs):
        if self.balance is None:
            self.balance = self.start_balance
        super().save(*args, **kwargs)

    def __str__(self):
        descriptive_name = self.name + " - USD " + str(round(self.balance, 2))
        return descriptive_name
    
    @property
    def get_trades(self):
        trades = Trade.objects.filter(user = self.user, portfolio = self)
        return trades

    def get_shares_of_stock(self, ticker):
        shares = Trade.objects.filter(user = self.user, 
                                      portfolio = self, 
                                      stock=get_object_or_404(Stock, ticker=ticker))
        return shares

    def get_total_quantity_of_shares(self, ticker):
        shares = self.get_shares_of_stock(ticker)
        quantity = 0
        for share in shares:
            quantity += share.quantity

        return quantity

class PortfolioHistory(models.Model):
    portfolioid = models.ForeignKey(StockPortfolio, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False)
    balance = models.DecimalField(max_digits=19, decimal_places=8, null=False)


class Trade(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(StockPortfolio, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, null=False, validators=[MinValueValidator(round(Decimal(0.001), 3))])
    purchase_price = models.DecimalField(max_digits=19, decimal_places=8, null=False)
    created_date = models.DateTimeField(auto_now_add=True)

    @property
    def get_gain_loss(self):
        self.stock.get_price
        stock_current_price = self.stock.regular_market_price
        return (stock_current_price - self.purchase_price)*self.quantity

    def sell_stock(self, sell_quantity, commit=True):
        if sell_quantity > self.quantity or sell_quantity <= 0:
            raise ValueError()
        elif sell_quantity == self.quantity:
            portfolio_balance_init = self.portfolio.balance
            self.stock.get_price()
            stock_price = Decimal(self.stock.regular_market_price)
            self.portfolio.balance = portfolio_balance_init + stock_price * sell_quantity
            self.portfolio.save()
            self.delete()
        else:
            portfolio_balance_init = self.portfolio.balance
            self.stock.get_price()
            stock_price = Decimal(self.stock.regular_market_price)
            self.portfolio.balance = portfolio_balance_init + stock_price * sell_quantity
            self.quantity = self.quantity - sell_quantity
            self.portfolio.save()
            self.save()