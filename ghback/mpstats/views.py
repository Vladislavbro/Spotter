from django.shortcuts import render
from django.http import JsonResponse
from mpstats.api import Mpstats

mpstats = Mpstats()


def categories(request):
    return JsonResponse(mpstats.get_categories(), safe=False)