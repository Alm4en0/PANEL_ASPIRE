import paypalrestsdk
from django.conf import settings

# Configurar PayPal SDK
paypalrestsdk.configure({
    'mode': settings.PAYPAL_MODE,
    'client_id': settings.PAYPAL_CLIENT_ID,
    'client_secret': settings.PAYPAL_CLIENT_SECRET
})

def create_payment(total, currency, return_url, cancel_url):
    payment = paypalrestsdk.Payment({
        'intent': 'sale',
        'payer': {'payment_method': 'paypal'},
        'transactions': [{
            'amount': {'total': total, 'currency': currency},
            'description': 'Compra de cursos'
        }],
        'redirect_urls': {
            'return_url': return_url,
            'cancel_url': cancel_url
        }
    })
    return payment.create(), payment

def execute_payment(payment_id, payer_id):
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({'payer_id': payer_id}):
        return True, payment
    else:
        return False, payment.error