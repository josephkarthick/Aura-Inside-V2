
from django.shortcuts import render

from .services.IT_dashboard import get_it_dashboard_data


def IT_Dashboard(request):

    context = get_it_dashboard_data()

    return render(
        request,
        "IT_Dashboard/index.html",
        context
    )
