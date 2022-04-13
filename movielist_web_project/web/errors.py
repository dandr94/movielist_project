from django.shortcuts import render


def handle_404_not_found(request, exception):
    return render(request, 'main/404.html')