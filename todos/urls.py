from django.urls import path

from todos.views import home_page, todos_page

urlpatterns = [
    path("", home_page),
    path("todos/", todos_page),
]