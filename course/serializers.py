from .models import *
from Teacher.serializers import TeacherSerializer
from rest_framework import serializers
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseCategory
        fields='__all__'
class CourseRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields='__all__'
class CourseLectureVideoSerializer(serializers.ModelSerializer):
    full_video_url = serializers.SerializerMethodField()
    class Meta:
        model=LectureVideo
        fields='__all__'
    
    def get_full_video_url(self, obj):
        if obj.video:
            url, options = cloudinary_url(obj.video.public_id, resource_type='video')
            return url
        return None

class CourseTopicsSerializer(serializers.ModelSerializer):
    videos = CourseLectureVideoSerializer(many=True, read_only=True)
    
    class Meta:
        model=Topic
        fields='__all__'

class CourseAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=['teacher','category','learning_outcomes','thumbnail']
# class CourseRemoveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Course
#         fields=['id']
class CategoryAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseCategory
        fields='__all__'


class CourseSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer()
    teacher = TeacherSerializer(many=True)
    rating= CourseRatingSerializer()
    topics=CourseTopicsSerializer(many=True)
    class Meta:
        model = Course
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
  
class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()  # Nested Course Details
    student=StudentSerializer()
    class Meta:
        model = Student_enrollment
        fields = ['course', 'status','grade','student']

class CartSerializer(serializers.ModelSerializer):
    student=StudentSerializer()
    course=CourseSerializer()
    class Meta:
        model = Cart
        fields = '__all__'
        extra_kwargs = {
        'student': {'read_only': True},
        'course': {'read_only': True}
    }


class CartAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        extra_kwargs = {
        'student': {'write_only': True},
        'course': {'write_only': True}
    }

    def create(self, validated_data):
        student = self.context.get('student')
        course = self.context.get('course')

        # Create Cart with actual objects
        cart = Cart.objects.create(
            student=student,
            course=course
            
        )
        print(cart)
        return cart
class CartRemoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = []
    
    def remove(self,validated_data):
        student = self.context.get('student')
        course = self.context.get('course')
        cart= Cart.objects.filter(course=course,student=student).delete()
        return cart

# class AssignmentSerializer(serializers.ModelSerializer):
#     student= StudentSerializer()
#     course=CourseSerializer()
#     class Meta:
#         model = Assignment
#         fields = '__all__'
        
