from django.shortcuts import render


def list(request):
    return render(request, 'feeds/list.html')
