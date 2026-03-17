from django.shortcuts import render

from todos import models
from todos.models import Todos

# Any Request, Template Response
def home_page(request):
    return render(request=request,template_name="home.html", context={})


def todos_page(request):
    return render(request=request,template_name="todos.html", context={})

# Any DATA REQ and RESP JSON

from django.http import JsonResponse
from django.db.models import F

def list_todos(request):
    # todos = [
    #         { "id": 1, "text": 'Buy groceries for next week', "completed": True, "dueDate": '', "addedDate": '2020-06-28' },
    #         { "id": 2, "text": 'Renew car insurance', "completed": False, "dueDate": '2020-06-28', "addedDate": '2020-06-28' },
    #         { "id": 3, "text": 'Sign up for online course', "completed": False, "dueDate": '', "addedDate": '2020-06-28' },
    #     ]

    todos = Todos.objects.all().annotate(
        dueDate = F("due_date"),
        addedDate = F("added_date")
    ).values("id", "text", "completed", "dueDate", "addedDate")
    # breakpoint()
    # .values("due_date", "text")
    # .values("id", "text", "completed", "due_date", "added_date")
    response = JsonResponse({"data":list(todos)},safe=False)
    return response

