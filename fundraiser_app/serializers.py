from django.conf import settings


def authorization_headers(json_access_token):
    result = {
        'Authorization': '{} {}'.format(json_access_token['token_type'], json_access_token['access_token']),
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/json'
    }
    return result


def payment_credentials(request, donation):
    result = {
        'username': settings.PAYTRACE_API_USER_NAME,
        'password': settings.PAYTRACE_API_USER_PASSWORD,
        'integrator_id': settings.PAYTRACE_API_USER_INTEGRATOR_ID,
        'amount': str(donation.amount),
        "credit_card":{
            "encrypted_number": request.POST.get('ccNumber'),
            "expiration_month": request.POST.get('expiration_month'),
            "expiration_year": request.POST.get('expiration_year'),
         },
        "encrypted_csc": request.POST.get('ccCSC'),
        "billing_address": {
            "name": '{} {}'.format(donation.first_name, donation.last_name),
            "street_address": donation.address,
            "city": donation.city,
            # "state":"WA",
            "zip": donation.postal_code
        }
    }
    return result
