# main/views.py
import re
from typing import Type
from .forms import CustomUserCreationForm, CustomPasswordResetForm, EditProfileForm, \
	EditUserForm, CustomPasswordChangeForm, ProfilePictureForm, NewPortfolioForm, \
	PortfolioForm, BuyStockForm, SellStockForm
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Stock, StockPortfolio, Trade
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from finance_data_manager import stock_manager
import yfinance as yf
import datetime
import decimal


def homepage(request):
	return render(request=request, template_name='main/home.html')


def error_404_view(request, exception):
	return render(request, "main/errors/404.html")


def register_request(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(request, 
                       "Unsuccessful registration. Invalid information.")
    form = CustomUserCreationForm()
    return render (request=request, 
                   template_name="main/register.html", 
                   context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("main:homepage")


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = CustomPasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = CustomUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					messages.success(request, f"Reset password e-mail has successfully been sent.")
					return redirect ("/password_reset/done/")
			else:
				messages.error(request, "Invalid username or email.")
		else:
			messages.error(request, "Invalid username or email.")
	password_reset_form = CustomPasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})


def profile(request, username):	
	user = CustomUser.objects.get(username = username)
	portfolios = StockPortfolio.objects.select_related().filter(user = user.id)
	return render (request=request, template_name="main/profile/profile.html", context={'user': user,
																					 'portfolios': portfolios })


@login_required
def profile_settings(request):
	user = CustomUser.objects.get(pk=request.user.id)
	portfolios = StockPortfolio.objects.select_related().filter(user = user.id)
	password_form = CustomPasswordChangeForm(request.user)
	update_account_form = EditUserForm(instance=user)
	update_profile_form = EditProfileForm(instance=user.userprofile)
	update_profile_pic_form = ProfilePictureForm(instance=user.userprofile)
	new_portfolio_form = NewPortfolioForm()
	portfolio_formset = modelformset_factory(StockPortfolio,
										  can_delete=True,
										  form=PortfolioForm,
										  extra=0)
	portfolio_formset_obj = portfolio_formset(queryset=portfolios)

	if request.method == "POST":
		if 'change_password' in request.POST:
			password_form = CustomPasswordChangeForm(request.user, request.POST)
			if password_form.is_valid():
				password_form.save()
				update_session_auth_hash(request, request.user)
				messages.success(request,('Your password was successfully updated.'))
				return redirect("main:login")
			else:
				messages.error(request,('Could not update password.'))
		if 'update_account' in request.POST:
			update_account_form = EditUserForm(request.POST, instance=user)
			if update_account_form.is_valid():
				update_account_form.save()
				messages.success(request,('Your account was successfully updated.'))
				return redirect("main:profile_settings")
			else:
				messages.error(request,('Could not update account information.'))
		if 'update_profile_name' in request.POST:
			update_profile_form = EditProfileForm(request.POST, instance=user.userprofile)
			if update_profile_form.is_valid():
				update_profile = update_profile_form.save(commit=False)
				update_profile.user = request.user
				update_profile.save()
				messages.success(request,('Your profile was successfully updated.'))
				return redirect("main:profile_settings")
			else:
				messages.error(request,('Could not update profile.'))
		if 'update_profile_pic' in request.POST:
			update_profile_pic_form = ProfilePictureForm(request.POST, request.FILES, instance=user.userprofile)
			if update_profile_pic_form.is_valid():
				profile_pic = update_profile_pic_form.save(commit=False)
				profile_pic.user = request.user
				profile_pic.user.userprofile = request.user.userprofile
				profile_pic.save()
				messages.success(request,('Profile image updated.'))
				return redirect("main:profile_settings")
			else:
				messages.error(request,('Could not update profile image.'))
		if 'new_stock_portfolio' in request.POST:
			new_portfolio_form = NewPortfolioForm(request.POST, request.user)
			if new_portfolio_form.is_valid():
				new_portfolio = new_portfolio_form.save(commit=False)
				new_portfolio.user = request.user
				new_portfolio.save()
				messages.success(request,('New portfolio created.'))
				return redirect("main:profile_settings")
		if 'portfolio_formset' in request.POST:
			portfolio_formset_obj = portfolio_formset(request.POST, queryset=portfolios)
			if portfolio_formset_obj.is_valid():
				portfolio_formset_obj.save()
				return redirect("main:profile_settings")
		else:
			messages.error(request,('Something went wrong. Please try again.'))


	return render(request=request, template_name='main/profile/profile_settings.html', 
			   context={"user": request.user, 
				"password_form": password_form, 
				"user_form": update_account_form, 
				"profile_form": update_profile_form,
				"profile_picture_form": update_profile_pic_form,
				"new_portfolio_form": new_portfolio_form,
				"portfolios": portfolios,
				"portfolio_formset": portfolio_formset_obj})


def stock_details(request, ticker):
	stock = get_object_or_404(Stock, pk=ticker)
	daily_data = stock.daily_data
	buy_stock_form = BuyStockForm()
	sell_stock_formset = modelformset_factory(Trade, 
										   can_delete=False, 
										   form=SellStockForm, 
										   extra=0)
	trades = Trade.objects.select_related().filter(user = request.user.id, stock=stock)
	sell_stock_formset_obj = sell_stock_formset(queryset=trades)

	if request.method == "POST":
		if 'buy_stock' in request.POST:
			buy_stock_form = BuyStockForm(request.POST, request.user)
			if buy_stock_form.is_valid():
				try:
					stock.buy_stock(buy_stock_form, request)
					messages.success(request,('Stock purchased.'))
				except ValueError:
					messages.error(request,('Not enough balance in this portfolio.'))
				return redirect("main:stock_details", ticker=ticker)
		if 'sell_stock' in request.POST:
			sell_stock_formset_obj = sell_stock_formset(request.POST, queryset=trades)
			if sell_stock_formset_obj.is_valid():
				for form in sell_stock_formset_obj.forms:
					try:
						form.cleaned_data['id'].sell_stock(sell_quantity=form.cleaned_data['sell_quantity'])
						messages.success(request,('Stock sold.'))
					except ValueError:
						messages.error(request,('Incorrect quantity entered to sell. Not enough balance in trade lot, attempted to sell 0 quantity, or value unrecognized.'))
				
				return redirect("main:stock_details", ticker=ticker)

	return render(request=request, template_name='main/content/stock_details.html', 
			   context={'stock': stock, 
			   'daily_data': daily_data, 
			   'buy_stock_form': buy_stock_form,
			   'sell_stock_formset': sell_stock_formset_obj})


def stock_stream(request):
	import json
	if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
		ticker = request.POST.get('ticker',None)

		stock_obj = get_object_or_404(Stock, pk=ticker)
		stock_obj.get_price()

		serialized_instance = serializers.serialize('json', [ stock_obj, ])

		return JsonResponse({"instance": serialized_instance}, status=200)

	return JsonResponse({"error": ""}, status=400)