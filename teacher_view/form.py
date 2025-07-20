
from django import forms
from course.models import *
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['category','learning_outcomes','thumbnail']

class CourseCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = '__all__'
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = '__all__'