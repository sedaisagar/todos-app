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
    
    print(f"""
    =================================================
                        {request.method}
    =================================================
    """)

    todos = Todos.objects.all().annotate(
        dueDate = F("due_date"),
        addedDate = F("added_date")
    ).values("id", "text", "completed", "dueDate", "addedDate")
    # breakpoint()
    # .values("due_date", "text")
    # .values("id", "text", "completed", "due_date", "added_date")
    response = JsonResponse({"data":list(todos)},safe=False)
    return response



def add_todo(request):
    print(f"""
    =================================================
                        {request.method}
    =================================================
    """)

    if request.method == "POST":
        # Represents post request
        keys = ["text","completed","due_date"]

        data = {}
        for i in keys:
            if i == "due_date":
                data[i] = request.POST["dueDate"] or None
            elif i == "completed":
                data[i] = request.POST[i] == "true"
            else:
                data[i] = request.POST[i]
        
        # Data Is Ok
        # Performing the insertion operation

        Todos.objects.create(**data)

        response = JsonResponse({"message":"Todo added successfully!"})
    else:
        # GET REQUEST
        response = JsonResponse({"message":"Method not allowed!"})
        response.status_code = 405

    return response

def edit_todo(request, id):
    print(f"""
    =================================================
                        {request.method}
    =================================================
    """)

    if request.method == "POST":
        # Represents post request
        
        data = {}

        data["text"] = request.POST["text"]
        
        # Data Is Ok
        # Performing the insertion operation

        Todos.objects.filter(pk=id).update(**data) # ORM

        response = JsonResponse({"message":"Todo updated successfully!"})
    else:
        # GET REQUEST
        response = JsonResponse({"message":"Method not allowed!"})
        response.status_code = 405

    return response


def remove_todo(request, pk):
    # GET method

    # todos = Todos.objects.filter(pk=pk) # Does not Throw exception 
    try:
        todo = Todos.objects.get(pk=pk) # Throws exception 
        todo.delete() # Removes object from database
        response = JsonResponse({"message":"Todo deleted successfully!"})
    except Exception as e:
        print(f"""
        =====================================
        {e.args}
        =====================================
        """)
        response = JsonResponse({"message":"Todo not deleted successfully!"})
        response.status_code = 400
    
    return response

