from django.db import models


class Todos(models.Model):
    text = models.CharField(max_length=255)
    completed = models.BooleanField()
    due_date = models.DateField(null=True, blank=True)
    
    # At the time of object creation the date is auto captured
    added_date = models.DateField(auto_now_add=True) 


    class Meta:
        db_table = "todos"


    def __str__(self):
        return self.text

class Reviews(models.Model):
    name = models.CharField(max_length=255) 	
    position = models.CharField(max_length=255) 	
    review = models.TextField() 	
    rating = models.PositiveIntegerField(default=0)


    class Meta:
        db_table = "reviews"

    def __str__(self):
        return self.name  	