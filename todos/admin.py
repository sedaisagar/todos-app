from django.contrib import admin

from todos.models import Todos, Reviews

# Register your models here.

admin.site.register([Todos, Reviews])