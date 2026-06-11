from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User

from .models import Course, Lesson, Resource


def index_view(request):
    print(request)
    return render(request, "index.html")


def courses_view(request):
    courses = Course.objects.all().order_by("-created_at")

    subject_filter = request.GET.get("subject")
    if subject_filter:
        courses = courses.filter(subject__iexact=subject_filter)

    subjects = Course.objects.values_list("subject", flat=True).distinct()

    context = {
        "courses": courses,
        "subjects": subjects,
        "active_subject": subject_filter,
    }
    return render(request, "courses.html", context)


def course_view(request, pk: int):
    course = get_object_or_404(Course, pk=pk)

    lessons = Lesson.objects.filter(course=course).order_by("id")

    lessons_count = lessons.count()

    context = {
        "course": course,
        "lessons": lessons,
        "lessons_count": lessons_count,
    }
    return render(request, "course.html", context)


def lesson_view(request, pk: int):
    lesson = get_object_or_404(Lesson, pk=pk)

    course_lessons = Lesson.objects.filter(course=lesson.course)

    next_lesson = lesson.get_next_lesson()
    prev_lesson = lesson.get_previous_lesson()

    # Resurslarni olish
    resources = Resource.objects.filter(lesson=lesson)

    context = {
        "lesson": lesson,
        "course_lessons": course_lessons,
        "next_lesson": next_lesson,
        "prev_lesson": prev_lesson,
        "resources": resources,
    }
    return render(request, "lesson.html", context)


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get("next", "index")
            return redirect(next_url)
        else:
            messages.error(request, "Foydalanuvchi nomi yoki kalit so'z noto'g'ri.")

    return render(request, "login.html")


def signup_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Bu username band. Boshqasini tanlang.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Bu email orqali allaqachon ro'yxatdan o'tilgan.")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)
            user.save(update_fields=["password"])

            login(request, user)

            return redirect("index")

    return render(request, "signup.html")
