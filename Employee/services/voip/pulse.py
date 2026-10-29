from django.http import HttpResponse


def initiate(voip_record):
    return HttpResponse(
        "PULSE calling is not implemented yet.",
        status=501
    )