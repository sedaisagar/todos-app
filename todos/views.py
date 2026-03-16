from django.shortcuts import render

def home_page(request):
    return render(request=request,template_name="home.html", context={})


def todos_page(request):
    return render(request=request,template_name="todos.html", context={})