from django.shortcuts import render

from hra.esi import ESI_REGISTRY


def esi(request, name):
    template = ESI_REGISTRY[name]['template']
    context = ESI_REGISTRY[name]['get_context']()
    return render(request, template, context)
