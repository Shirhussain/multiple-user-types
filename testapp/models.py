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

    """
    if we don't user TeachreMore() what we should do?
    there is another approach which you can put all the field in the main "User" model
    but there are some challenge is:
        # verbose ---> we have to prefix each field with the name
        # what if you have 20-30 diffrent user Types? 
        # what if you have only five user types but you might have 20-30 each fields? 
            all the saddan you database become huge. 

    """
    # teacher_field_major = 
    # teacher_award = 
    # teacher_experience = 
    # teacher_credit =      

    """
        another approach is JSON fields:
        verbose --> which steak all specific custom user data in to you json field, then you loss 
        constrans of that, it that thing is you don't care about you still have the prefix .
        all of your field with diffrent type of data that it represents and that really slow things down
        just like adding all those other fields.
        # another problem with json is that then we need to write custom handler for forms as well as for serializers
    """
    # more = models.JSONField(encoder="")


    # def get_absolute_url(self):
    #     return reverse("users:detail", kwargs={"username": self.username})


class TeacherManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.TEACHER)


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.STUDENT)


#how you can add  custom data field for each one of this type
# add the ability for teacher to be diffrent type of teacher i.g ' Math , physic, chemmisty'
class TeacherMore(models.Model):
    # you could timestamp if you want 
    # this is a real table which will be in your database
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    field_major = models.CharField(max_length=255)
    award = models.CharField(max_length=255, blank=True)
    experience = models.IntegerField()
    credit = models.IntegerField()


class Teacher(User):
    base_type = User.Types.TEACHER
    objects = TeacherManager()

    # more --> our connvention for callling all of our proxy models
    @property
    def more(self):
        # this gonna reffer back to 'teachermore' which will be the database representation 'TeacherMore' class
        return self.teachermore

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


class StudentMore(models.Model):
    user = model.OneToOneField(User, on_delete=model.CASCADE)
    mark = model.FloatField()


class Student(User):
    base_type = User.Types.STUDENT
    objects = StudentManager()

    @property
    def more(self):
        return self.studentmore 

    class Meta:
        proxy = True

    def homework(self):
        return "Student must do the homework"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Types.STUDENT
        return super().save(*args, **kwargs)


