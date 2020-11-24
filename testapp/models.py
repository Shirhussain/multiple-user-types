from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import  reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    class Types(models.TextChoices):
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    # what type of User are we?
    type = models.CharField(_('Type'), max_length=50, choices=Types.choices, default=Types.STUDENT)
    # First name and last name do not cover Name Patterns
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class TeacherManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.TEACHER)


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.STUDENT)

class Teacher(User):
    objects = TeacherManager()

    class Meta:
        # They way proxy work is that it doesn't create new table 
        # Which means that it's retrally the same table as use it means that it use 'User'
        proxy = True

    def teach(self):
        return "Teacher is Teaching some good things"
    
    def save(self, *args, **kwargs):
        # if the record doesn't exists then the TEACHER type attach to them.
        if not self.pk:
            self.type = User.Types.TEACHER
        return super().save(*args, **kwargs)

class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def homework(self):
        return "Student must do the homework"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STUDENT
        return super().save(*args, **kwargs)

