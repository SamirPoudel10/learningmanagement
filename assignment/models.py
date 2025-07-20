from django.db import models
from Student.models import Student
from Teacher.models import Teacher
from course.models import Course
# Create your models here.

class Assignment(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    due_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" assigned an assignment of {self.course}"