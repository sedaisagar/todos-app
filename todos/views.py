from django.shortcuts import render, redirect

from todos import models
from todos.forms import ReviewForm
from todos.models import Reviews, Todos

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


# ===================================================
#                   REVIEWS
# ===================================================



def reviews_page(request):
    object_list = Reviews.objects.all()
    return render(
        request=request,
        template_name="reviews.html", 
        context={"reviews":object_list}
    )


def review_create_page(request):
    if request.method == "GET":
        form = ReviewForm()

        return render(
            request,
            template_name="common-form.html",
            context={"form":form},
        )
    else:
        # POST

        data = request.POST

        form = ReviewForm(data=data) 

        if form.is_valid():
            super_cleaned_data = form.cleaned_data
            review = Reviews.objects.create(**super_cleaned_data)
            print(f"Review added >>>>>>>>> {review}")
            return redirect("reviews-page") # This points redirection to url specified by reverse name 'reviews-page'


def review_edit_page(request, pk):
    try:
        review = Reviews.objects.get(pk=pk) # Throws exception 
    except Exception as e:
        print(e.args)
        return redirect("reviews-page")

    if request.method == "GET":
        data = dict(
            name = review.name,
            position = review.position,
            review = review.review,
            rating = review.rating,
        )

        form = ReviewForm(initial=data)

        return render(
            request,
            template_name="common-form.html",
            context={"form":form},
        )
    else:
        # POST

        data = request.POST

        form = ReviewForm(data=data) 

        if form.is_valid():
            super_cleaned_data = form.cleaned_data
            # review = Reviews.objects.create(**super_cleaned_data)
            
            review.name = super_cleaned_data.get("name") or review.name
            review.position = super_cleaned_data.get("position") or review.position
            review.review = super_cleaned_data.get("review") or review.review
            review.rating = super_cleaned_data.get("rating") or review.rating

            review.save()

            print(f"Review Updated ")
            return redirect("reviews-page") # This points redirection to url specified by reverse name 'reviews-page'


def review_delete_page(request, pk):
    try:
        review = Reviews.objects.get(pk=pk) # Throws exception 
        review.delete()
        return redirect("reviews-page")

    except Exception as e:
        print(e.args)
        return redirect("reviews-page")
