from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User


def CheapFlightsSearch(request):
    if request.method == 'POST':
        template = loader.get_template("cheap_flights_results.html")
        # cheap_flights, cheap_flights_short = get_cheap_flights_for_given_city()
        # context = {'cheap_flights_short': cheap_flights_short}
        context = {}
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("cheap_flights_form.html")
        context = {}
        return HttpResponse(template.render(context, request))
