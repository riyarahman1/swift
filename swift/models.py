from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
import os
from phonenumber_field.modelfields import PhoneNumberField
from swift.validators import validate_possible_number
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


def ImagePreSave(sender, instance, *args, **kwargs):
    try:
        instance_old = sender.objects.get(pk=instance.id)
        if instance.image != None and instance_old.image.name != instance.image.name:
            if os.path.exists(instance_old.image.path):
                os.remove(instance_old.image.path)
    except Exception as e:
        pass
    try:
        if (
            instance.bg_image != None
            and instance_old.bg_image.name != instance.bg_image.name
        ):
            if os.path.exists(instance_old.bg_image.path):
                os.remove(instance_old.bg_image.path)
    except:
        pass


def ImagePostDelete(sender, instance, *args, **kwargs):
    try:
        if instance.image != None and instance.image.name != "":
            if os.path.exists(instance.image.path):
                os.remove(instance.image.path)
    except:
        pass
    try:
        if instance.bg_image != None and instance.bg_image.name != "":
            if os.path.exists(instance.bg_image.path):
                os.remove(instance.bg_image.path)
    except:
        pass


class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_number]


#### Get last insance pk
def GetLastPK(instance):
    instance_id = 1
    if instance.pk is None:
        instance_last = instance.__class__.objects.last()
        if instance_last != None:
            instance_id = instance_last.pk + 1
    else:
        instance_id = instance.pk
    return instance_id


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


USER_STATUS = (
    (1, "pending"),
    (2, "active"),
    (3, "blocked"),
    (4, "deleted"),
)


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    mobile = PossiblePhoneNumberField(blank=True, default="", db_index=True)
    profile_pic = models.ImageField(upload_to="profile", blank=True, null=True)
    address = models.CharField(max_length=225, blank=True)
    email_stat = models.BooleanField(default=False)
    mobile_stat = models.BooleanField(default=False)
    status = models.PositiveIntegerField(
        choices=USER_STATUS, null=False, blank=False, default=1
    )
    is_active = models.BooleanField(default=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email + " - " + self.first_name + " " + self.last_name


pre_save.connect(ImagePreSave, sender=User)
post_delete.connect(ImagePostDelete, sender=User)


class EmailTemplate(models.Model):
    name = models.CharField("Template Name", max_length=255, blank=True)
    content = models.TextField("Content source code", blank=True)
    order = models.PositiveIntegerField(
        default=0, blank=False, null=False, editable=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    is_active = models.BooleanField("Active", default=True)

    class Meta:
        verbose_name = "Email Template"
        verbose_name_plural = "Email Template"

    def __str__(self):
        return self.name


CREATE, READ, UPDATE, DELETE = "Create", "Read", "Update", "Delete"
LOGIN, LOGOUT, LOGIN_FAILED = "Login", "Logout", "Login Failed"
SUCCESS, FAILED = "Success", "Failed"
ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]
ACTION_TYPES = [
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
    (LOGIN, LOGIN),
    (LOGOUT, LOGOUT),
    (LOGIN_FAILED, LOGIN_FAILED),
]


class ActivityLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    action_type = models.CharField(choices=ACTION_TYPES, max_length=15)
    action_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(choices=ACTION_STATUS, max_length=7, default=SUCCESS)
    data = models.JSONField(default=dict)
    app_visibility = models.BooleanField(default=False)
    web_visibility = models.BooleanField(default=False)
    activity_mode = models.CharField(
        max_length=10, null=True, blank=True, default="Web"
    )
    module_name = models.CharField(max_length=50, null=True, blank=True)
    error_msg = models.TextField(blank=True, null=True)
    path_info = models.JSONField(default=dict)
    fwd_link = models.CharField(max_length=100, null=True, blank=True)

    # for generic relations
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return f"{self.action_type} by {self.actor} on {self.action_time}"


class Curriculum(models.Model):
    COUNTRY_CHOICES = [
        ("UK", "UK"),
        ("International", "International"),
    ]

    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField("Active", default=True)
    country = models.CharField(max_length=100, choices=COUNTRY_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100, blank=True)
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="curriculum_courses",
    )
    is_active = models.BooleanField("Active", default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100, blank=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="course_subjects",
    )
    is_active = models.BooleanField("Active", default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=100, blank=True)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subject_topics",
    )
    is_active = models.BooleanField("Active", default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name


class SubTopic(models.Model):
    name = models.CharField(max_length=100, blank=True)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, null=True, blank=True, related_name="subtopics"
    )
    lessons = models.TextField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    is_active = models.BooleanField("Active", default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name
