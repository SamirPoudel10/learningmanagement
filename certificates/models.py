from django.db import models

# Create your models here.


class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class LectureVideo(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=100)
    video = CloudinaryField( resource_type='video')  
    video_length=models.DurationField(default='00:00:00')# or FileField if storing locally
    thumbnail=models.ImageField(upload_to='videos/thumbnail/')

    def __str__(self):
        return self.title


class Student(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        related_name='student_set',
        blank=True,
        help_text='Groups for the student',
        related_query_name='student',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='student_permissions',
        blank=True,
        help_text='Permissions for the student',
        related_query_name='student',
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    qualification = models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=100)
    address = models.TextField()
    interested_categories = models.TextField()
    is_active = models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    objects = StudentManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

