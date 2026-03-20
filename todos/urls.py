from django.urls import path, include

from todos.views import add_todo, edit_todo, home_page, list_todos, remove_todo, review_create_page, review_delete_page, review_edit_page, reviews_page, todos_page

urlpatterns = [
    path("", home_page),
    path("todos/", todos_page),
    path("reviews/", include([
        path("", reviews_page, name="reviews-page"),
        path("create/", review_create_page, name="reviews-create-page"),
        path("edit/<str:pk>", review_edit_page, name="reviews-edit-page"),
        path("delete/<str:pk>", review_delete_page, name="reviews-delete-page"),
    ])),
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