from django.shortcuts import render

def landing_page(request):
    return render(request, "index.html")

##kode fungsi landing page untuk nge render index.html