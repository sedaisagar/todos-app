from django.urls import path, include

from todos.views import add_todo, edit_todo, home_page, list_todos, remove_todo, todos_page

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
                path("todos/update/<str:id>", edit_todo),
                path("todos/remove/<str:pk>", remove_todo),
            ]
        )
    ),
]