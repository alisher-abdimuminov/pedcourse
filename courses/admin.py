from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.models import Group

from .models import Course, Lesson, Resource


admin.register(Group)


@admin.register(Course)
class CourseModelAdmin(ModelAdmin):
    list_display = ["name", "price", "subject"]
    search_fields = ["name"]


@admin.register(Lesson)
class LessonModelAdmin(ModelAdmin):
    list_display = ["name", "course"]
    search_fields = ["name"]


@admin.register(Resource)
class ResourceModelAdmin(ModelAdmin):
    list_display = ["name", "lesson"]
    search_fields = ["name"]
