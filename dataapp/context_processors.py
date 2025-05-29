from .models import Customers

def customer_name(request):
    customer = None
    customer_name = None

    if request.session.get('customer_id'):
        try:
            customer = Customers.objects.get(id=request.session['customer_id'])
            customer_name = customer.cus_name
        except Customers.DoesNotExist:
            customer = None
            customer_name = None

    return {
        'customer_name': customer_name
    }
