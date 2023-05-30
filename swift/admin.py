from django.contrib import admin
from .models import Course,Subject,Topic,SubTopic
# Register your models here.

admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(SubTopic)

