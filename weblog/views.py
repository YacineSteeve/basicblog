from django.shortcuts import render


def index(request):
    context = {
        'key': 'value',
    }
    return render(request, 'base.html', context=context)
