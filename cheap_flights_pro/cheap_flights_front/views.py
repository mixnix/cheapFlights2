from django.views.generic import TemplateView
from django.template import loader
from django.http import HttpResponse

from .forms import CreateReviewForm
from outer_libraries.cheapFlightsFinder import get_cheap_flights_for_given_city

class CheapFlightsForm(TemplateView):
    template_name = "cheap_flights_form.html"


def CheapFlightsSearch(request):
    if request.method == 'POST':
        template = loader.get_template("cheap_flights_results.html")
        cheap_flights, cheap_flights_short = get_cheap_flights_for_given_city()
        context = {'cheap_flights_short': cheap_flights_short}
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("cheap_flights_form.html")
        context = {}
        return HttpResponse(template.render(context, request))

