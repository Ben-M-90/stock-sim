from .models import CustomUser, Stock

def stocks(request):
	stocks = Stock.objects.all()
	return {"stocks": stocks}
