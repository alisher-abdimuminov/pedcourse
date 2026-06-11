from django.urls import path

from .views import (
    index_view,
    courses_view,
    course_view,
    lesson_view,
    login_view,
    signup_view,
)


urlpatterns = [
    path("", index_view, name="index"),
    path("courses/", courses_view, name="courses"),
    path("courses/<int:pk>/", course_view, name="course"),
    path("lessons/<int:pk>/", lesson_view, name="lesson"),
    path("auth/login/", login_view, name="login"),
    path("auth/signup/", signup_view, name="signup"),
]
