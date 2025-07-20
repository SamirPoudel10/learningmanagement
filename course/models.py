from django.db import models
from Student.models import *
from Student.serializers import *
from Teacher.models import *

# Create your models here.
class CourseCategory(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    duration=models.IntegerField(default=1)
    price=models.FloatField(default=0.00)
    class Meta:
        verbose_name_plural='1. Course Categories'
    def __str__(self):
        return self.title
class Rating(models.Model):
    rating=models.IntegerField(default=0)
    number=models.IntegerField(default=0)
    def __str__(self):
        return str(self.rating)
    class Meta:

        verbose_name_plural='2.Rating '
    
class Course(models.Model):
    category=models.ForeignKey(CourseCategory,on_delete=models.CASCADE)
    teacher=models.ManyToManyField(Teacher)
    rating=models.ForeignKey(Rating,on_delete=models.CASCADE,default=1)
    enrolled=models.IntegerField(default=0)
    updated_at = models.DateField(auto_now_add=True)
    learning_outcomes = models.JSONField()
    thumbnail=models.ImageField(upload_to='course_images/')
    class Meta:

        verbose_name_plural='3. Course '
        
    def __str__(self):
        return self.category.title      



class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    class Meta:

        verbose_name_plural='4.Topics '

class LectureVideo(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100)
    video = CloudinaryField( resource_type='video')  
    video_length=models.TimeField(default='00:00:00')# or FileField if storing locally
    thumbnail=models.ImageField(upload_to='videos/thumbnail/')

    def __str__(self):
        return self.title
    class Meta:

        verbose_name_plural='5.Lecture Videos '

class Student_enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ], default='active')
    grade = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course') 
        verbose_name_plural='7. Student Enrollment' 
    def __str__(self):
        return f"{self.student.full_name} enrolled in {self.course.category.title}"


class Cart(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'course')  
    def __str__(self):
        return f'{self.course} added to cart Successsfully'
    class Meta:

        verbose_name_plural='6. Cart '

