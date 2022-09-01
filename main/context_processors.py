from .models import Stock

def stocks(request):
	stocks = Stock.objects.all()
	return {"stocks": stocks}
