from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from .models import FundraiserCategory, Fundraiser, FundraiserMsgUpdate
from .forms import FundraiserForm, FundraiserMsgUpdateForm, FundraiserDonationForm
from .serializers import payment_credentials, authorization_headers
from .utilities import minus_10_second_buffer
import requests
import json
from decimal import Decimal


def home(request):  # show all categories
    categories = FundraiserCategory.objects.all()
    return render(request, 'fundraiser_app/home.html', {'categories': categories})


def fundraiser_category_list(request, category_slug):
    fundraisers = Fundraiser.objects.filter(category__slug=category_slug).filter(ends_on__gt=timezone.now())
    return render(request, 'fundraiser_app/category_list.html', {'fundraisers': fundraisers, 'category_slug': category_slug})


@login_required(login_url='/accounts/login')
def create(request, category_slug):
    category = FundraiserCategory.objects.get(slug=category_slug)
    form = FundraiserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_fundraiser = form.save(commit=False)
            new_fundraiser.slug = slugify(request.POST['title'])
            new_fundraiser.user = request.user
            new_fundraiser.category = category
            new_fundraiser.save()
            return redirect(reverse('fundraiser_app:detail', args=[new_fundraiser.category.slug, new_fundraiser.id, new_fundraiser.created.year, new_fundraiser.created.month, new_fundraiser.created.day, new_fundraiser.slug]))
    return render(request, 'fundraiser_app/fundraiser_create.html', {'form': form, 'category_slug': category_slug})


def detail(request, category_slug, fundr_id, year, month, day, slug):  # show detail for Fundraiser, and all FundraiserMsgUpdate's
    # if user owns the fundraiser... show ability to add a message update
    fundraiser = Fundraiser.objects.get(id=fundr_id)
    donation = FundraiserDonationForm()
    if request.user.id == fundraiser.user.id:
        form = FundraiserMsgUpdateForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                msg_update = form.save(commit=False)
                msg_update.user = request.user
                msg_update.fundraiser = fundraiser
                msg_update.updated = minus_10_second_buffer()
                msg_update.save()
                return redirect(reverse('fundraiser_app:detail', args=[category_slug, fundraiser.id, fundraiser.created.year, fundraiser.created.month, fundraiser.created.day, fundraiser.slug]))
        return render(request, 'fundraiser_app/fundraiser_detail.html', {'fundraiser': fundraiser, 'form': form})  # let user add an update
    return render(request, 'fundraiser_app/fundraiser_detail.html', {'fundraiser': fundraiser, 'donation': donation})


def edit_fundraiser_detail(request, category_slug, fundr_id, year, month, day, slug):
    fundraiser = Fundraiser.objects.get(id=fundr_id)
    if request.user.id == fundraiser.user.id:
        form = FundraiserForm(request.POST or None, instance=fundraiser)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect(reverse('fundraiser_app:detail', args=[category_slug, fundraiser.id, fundraiser.created.year, fundraiser.created.month, fundraiser.created.day, fundraiser.slug]))
        return render(request, 'fundraiser_app/fundraiser_detail_edit.html', {'fundraiser': fundraiser, 'form': form})  # let user add an update
    return redirect(reverse('fundraiser_app:detail', args=[category_slug, fundraiser.id, fundraiser.created.year, fundraiser.created.month, fundraiser.created.day, fundraiser.slug]))


def msg_update(request, category_slug, msg_id, slug):  # necessary for complex RSS/Atom feed functionality
    message_update = FundraiserMsgUpdate.objects.get(id=msg_id)
    return render(request, 'fundraiser_app/fundraiser_msg_update.html', {'message_update': message_update})


def edit_msg_update(request, category_slug, msg_id, slug):  # necessary for complex RSS/Atom feed functionality
    message_update = FundraiserMsgUpdate.objects.get(id=msg_id)
    form = FundraiserMsgUpdateForm(request.POST or None, instance=message_update)
    if message_update.user.id == request.user.id:
        if request.method == 'POST':
            msg_update = form.save(commit=False)
            msg_update.updated = minus_10_second_buffer()   # in case of server lag, so messages don't appear updated when not.
            msg_update.save()
            return redirect(reverse('fundraiser_app:detail', args=[category_slug, message_update.fundraiser.id, message_update.fundraiser.created.year, message_update.fundraiser.created.month, message_update.fundraiser.created.day, message_update.fundraiser.slug]))
        return render(request, 'fundraiser_app/fundraiser_msg_update_edit.html', {'message_update': message_update, 'form': form})
    return redirect(reverse('fundraiser_app:detail', args=[category_slug, message_update.fundraiser.id, message_update.fundraiser.created.year, message_update.fundraiser.created.month, message_update.fundraiser.created.day, message_update.fundraiser.slug]))


def delete_msg_update(request, category_slug, msg_id, slug):  # necessary for complex RSS/Atom feed functionality
    message_update = FundraiserMsgUpdate.objects.get(id=msg_id)
    if message_update.user.id == request.user.id:
        if request.method == 'POST':
            message_update.delete()
            # category_slug, fundraiser.id, fundraiser.created.year, fundraiser.created.month, fundraiser.created.day, fundraiser.slug
            # message_update.fundraiser.category.slug message_update.fundraiser.id    message_update.fundraiser.created.year message_update.fundraiser.created.month message_update.fundraiser.created.day message_update.fundraiser.slug
            return redirect(reverse('fundraiser_app:detail', args=[category_slug, message_update.fundraiser.id, message_update.fundraiser.created.year, message_update.fundraiser.created.month, message_update.fundraiser.created.day, message_update.fundraiser.slug]))
        return render(request, 'fundraiser_app/fundraiser_msg_update_delete.html', {'message_update': message_update})
    return redirect(reverse('fundraiser_app:detail', args=[category_slug, message_update.fundraiser.id, message_update.fundraiser.created.year, message_update.fundraiser.created.month, message_update.fundraiser.created.day, message_update.fundraiser.slug]))


def donate(request, category_slug, fundr_id, year, month, day, slug):  # donate to Fundraiser, anyone can pay
    fundraiser = Fundraiser.objects.get(id=fundr_id)
    donation = FundraiserDonationForm(request.POST or None)
    if request.method == 'POST':
        if fundraiser.is_ended():
            return render(request, 'fundraiser_app/ended.html', {'fundraiser': fundraiser})
        if donation.is_valid():
            donation = donation.save(commit=False)
            fundraiser.amount_raised += donation.amount
            fundraiser.my_est_cut += round(donation.amount * Decimal(0.1), 2)
            donation.fundraiser = fundraiser
            # 1. AUTHENTICATION / PERMISSION - Send a POST request with your user credentials to generate bearer access token:   https://developers.paytrace.com/support/home#14000041395
            # NOT USING OAUTH 2.0, response is always json
            access_token = requests.post('https://api.paytrace.com/oauth/token', data=settings.PAYTRACE_NEW_ACCESS_TOKEN_CREDENTIALS, headers=settings.PAYTRACE_NEW_ACCESS_TOKEN_HEADERS)
            json_access_token = json.loads(access_token.text)
            # 2. MAKE PAYMENT - once web token is returned to browser... Send token back as https POST request with json and headers
            make_payment = requests.post('https://api.paytrace.com/v1/transactions/sale/keyed', json=payment_credentials(request, donation), headers=authorization_headers(json_access_token))
            # 3. CHECK RESPONSE ERRORS - For any API errors, Check out PayTrace Virtual Terminal → integration → API log.  Check out API Log for more details.
            payment_response = json.loads(make_payment.text)
            if payment_response['response_code'] != 101:    # 101 is good, anything else is an error, etc
                return render(request, 'fundraiser_app/payment_error.html', {'payment_response': payment_response['response_code'], 'status_message': payment_response['status_message']})
            donation.trans_id = payment_response['transaction_id']
            donation.paid = True
            donation.save()
            fundraiser.save()
            # 4. SHOW RESULT
            return render(request, 'fundraiser_app/thanks.html', {'payment_response': payment_response['response_code'],
                                                                    'status_message': payment_response['status_message'],
                                                                    'trans_id': payment_response['transaction_id'],
                                                                    'masked_card_number': payment_response['masked_card_number']
                                                                    })
    return render(request, 'fundraiser_app/fundraiser_detail.html', {'fundraiser': fundraiser, 'donation': donation})
