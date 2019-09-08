from django.views.generic import TemplateView
from django.template import loader
from django.http import HttpResponse

from .forms import CreateReviewForm

class CheapFlightsForm(TemplateView):
    template_name = "cheap_flights_form.html"


def CheapFlightsSearch(request):
    if request.method == 'POST':
        template = loader.get_template("cheap_flights_results.html")
        context = {'form': "tu będzie form"}
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template("cheap_flights_form.html")
        context = {}
        return HttpResponse(template.render(context, request))

