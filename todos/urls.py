from django.urls import path, include

from todos.views import add_todo, home_page, list_todos, todos_page

urlpatterns = [
    path("", home_page),
    path("todos/", todos_page),
    # 
    path(
        "api/", 
        include(
            [
                path("todos/", list_todos),
                path("todos/add", add_todo),
            ]
        )
    ),
]