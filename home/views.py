from plotly.offline import plot
import plotly.graph_objects as go

from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

import stripe
import json
from home.models import Product # ? do I need to create the model
import djstripe
from django.http import HttpResponse
# Create your views here.

def home(request):
    def scatter():
        x1 = [1,2,3,4]
        y1 = [30, 35, 25, 45]

        trace = go.Scatter(
            x=x1,
            y = y1
        )
        layout = dict(
            title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis = dict(range=[min(y1), max(y1)])
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context ={
        'plot1': scatter()
    }

    return render(request, 'home/welcome.html', context)

@login_required
def checkout(request):
	products = Product.objects.all()
	return render(request,"checkout.html",{"products": products})


@login_required
def create_sub(request):
	if request.method == 'POST':
	    # Reads application/json and returns a response
	    data = json.loads(request.body)
	    payment_method = data['payment_method']
	    stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

	    payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
	    djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

	    try:
	        # This creates a new Customer and attaches the PaymentMethod in one API call.
	        customer = stripe.Customer.create(
	            payment_method=payment_method,
	            email=request.user.email,
	            invoice_settings={
	                'default_payment_method': payment_method
	            }
	        )

	        djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
	        request.user.customer = djstripe_customer

	        # At this point, associate the ID of the Customer object with your
	        # own internal representation of a customer, if you have one.
	        # print(customer)

	        # Subscribe the user to the subscription created
	        subscription = stripe.Subscription.create(
	            customer=customer.id,
	            items=[
	                {
	                    "price": data["price_id"],
	                },
	            ],
	            expand=["latest_invoice.payment_intent"]
	        )

	        djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

	        request.user.subscription = djstripe_subscription
	        request.user.save()

	        return JsonResponse(subscription)
	    except Exception as e:
	        return JsonResponse({'error': (e.args[0])}, status =403)
	else:
		return HttpResponse('requet method not allowed')


def complete(request):
    return render(request, "complete.html")