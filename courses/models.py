from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    description = models.TextField()
    price = models.IntegerField(default=0)
    subject = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="images")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    video = models.FileField(upload_to="videos")
    speech = models.FileField(upload_to="speeches")
    body = models.TextField()

    def __str__(self):
        return self.name

    def get_next_lesson(self):
        return (
            Lesson.objects.filter(course=self.course, id__gt=self.id)
            .order_by("id")
            .first()
        )

    def get_previous_lesson(self):
        return (
            Lesson.objects.filter(course=self.course, id__lt=self.id)
            .order_by("-id")
            .first()
        )


class Resource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    file = models.FileField(upload_to="resources")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
